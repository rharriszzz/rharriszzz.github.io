"""Catalog, accessibility basics, and the publication boundary."""
import copy
import importlib.util
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build", ROOT / "scripts/build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class Document(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.elements = []
        self.feed(page)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "projects.json").read_text())
        build.build()
        cls.page = (ROOT / "dist/index.html").read_text()
        cls.doc = Document(cls.page)

    def test_all_reviewed_projects_are_in_static_html(self):
        cards = [a["data-project"] for _, a in self.doc.elements if "data-project" in a]
        self.assertEqual(cards, [p["slug"] for p in self.data["projects"] if p.get("listed", True)])
        self.assertNotIn("{{", self.page)

    def test_one_ordered_project_grid_without_search_or_featured_sections(self):
        listed = [p for p in self.data["projects"] if p.get("listed", True)]
        self.assertIn('<div class="project-grid">', self.page)
        self.assertNotIn('Selected projects', self.page)
        self.assertNotIn('More from the collection', self.page)
        self.assertNotIn('id="filters"', self.page)
        self.assertNotIn('id="search"', self.page)
        self.assertNotIn('app.js', self.page)
        self.assertNotIn('class="secondary-card"', self.page)
        self.assertEqual(sum(1 for tag, attrs in self.doc.elements
                             if tag == "article" and attrs.get("class") == "project-card"), len(listed))
        self.assertEqual(sum(1 for tag, attrs in self.doc.elements if tag == "h3"), len(listed))
        self.assertEqual(listed[0]["slug"], "reversi")
        self.assertEqual(listed[-1]["slug"], "HIS_profile")

    def test_homepage_introduction_is_plain_and_concise(self):
        self.assertIn('<h1 id="title">Projects</h1>', self.page)
        self.assertIn('Links to project websites, documentation, and source code.', self.page)
        self.assertIn('About this index', self.page)
        self.assertNotIn('Projects &amp;<br>', self.page)
        self.assertNotIn('Questions become code', self.page)
        self.assertNotIn('the occasional music-box disc', self.page)

    def test_unlisted_projects_do_not_leak_into_published_site_or_catalog(self):
        unlisted = {p["slug"] for p in self.data["projects"] if not p.get("listed", True)}
        self.assertEqual(unlisted, {"sound", "zos_python", "izODA.github.io", "numpy"})
        published = json.loads((ROOT / "dist/projects.json").read_text())
        self.assertEqual(
            [p["slug"] for p in published["projects"]],
            [p["slug"] for p in self.data["projects"] if p.get("listed", True)],
        )
        for slug in unlisted:
            self.assertNotIn(f'data-project="{slug}"', self.page)
        self.assertIn('data-project="HIS_profile"', self.page)
        self.assertNotIn("python-ibmdb", self.page)
        self.assertNotIn("python-ibmdb", (ROOT / "dist/projects.json").read_text())

    def test_his_profile_uses_authentic_source_image(self):
        his = next(p for p in self.data["projects"] if p["slug"] == "HIS_profile")
        source = "https://raw.githubusercontent.com/rharriszzz/HIS_profile/master/images/Tree.jpg"
        self.assertEqual(his["image"]["url"], source)
        self.assertIn(f'src="{source}"', self.page)
        self.assertNotIn("assets/images/HIS_profile.jpg", self.page)
        data = copy.deepcopy(self.data)
        bad = next(p for p in data["projects"] if p["slug"] == "HIS_profile")
        bad["image"]["url"] = "https://example.com/Tree.jpg"
        with self.assertRaises(ValueError):
            build.validate(data)

    def test_bead_map_uses_approved_photograph_and_mask_figure(self):
        project = next(p for p in self.data["projects"] if p["slug"] == "bead_map")
        expected = "https://raw.githubusercontent.com/rharriszzz/bead_map/main/docs/figures/bead-map-card.png"
        source = "https://github.com/rharriszzz/bead_map/blob/main/docs/figures/bead-map-card.png"
        self.assertEqual(project["image"]["url"], expected)
        self.assertEqual(project["image"]["source"], source)
        self.assertIn("photograph", project["image"]["alt"].lower())
        self.assertIn("color", project["image"]["alt"].lower())
        card = build.render_card(project)
        image_tags = [attrs for tag, attrs in Document(card).elements if tag == "img"]
        self.assertEqual(len(image_tags), 1)
        self.assertEqual(image_tags[0]["src"], expected)
        self.assertEqual(image_tags[0]["alt"], project["image"]["alt"])
        self.assertIn(project["image"]["caption"], card)
        self.assertNotIn("image-placeholder", card)
        published = json.loads((ROOT / "dist/projects.json").read_text())
        listed = next(p for p in published["projects"] if p["slug"] == "bead_map")
        self.assertEqual(listed["image"], project["image"])

    def test_fft_explorer_uses_computed_candidate_five_card(self):
        project = next(p for p in self.data["projects"] if p["slug"] == "fft-image-explorer")
        image = project["image"]
        url = "https://raw.githubusercontent.com/rharriszzz/fft-image-explorer/main/docs/figures/local-fft-card.png"
        source = "https://github.com/rharriszzz/fft-image-explorer/blob/main/docs/figures/local-fft-card.png"
        self.assertEqual(image["url"], url)
        self.assertEqual(image["source"], source)
        self.assertIn("computed", image["alt"].lower())
        self.assertNotIn("screenshot", image["caption"].lower())
        card = build.render_card(project)
        imgs = [attrs for tag, attrs in Document(card).elements if tag == "img"]
        self.assertEqual(len(imgs), 1)
        self.assertEqual(imgs[0]["src"], url)
        self.assertEqual(imgs[0]["alt"], image["alt"])
        self.assertNotIn("image-placeholder", card)
        self.assertIn(image["caption"], card)
        published = json.loads((ROOT / "dist/projects.json").read_text())
        self.assertEqual(next(p for p in published["projects"]
                              if p["slug"] == "fft-image-explorer")["image"], image)

    def test_hosted_image_paths_stay_in_owning_repo(self):
        for bad_url in [
            "https://example.com/rharriszzz/fft-image-explorer/main/docs/figures/local-fft-card.png",
            "https://raw.githubusercontent.com/someone/fft-image-explorer/main/docs/figures/local-fft-card.png",
            "https://raw.githubusercontent.com/rharriszzz/fft-image-explorer/old/docs/figures/local-fft-card.png",
            "https://raw.githubusercontent.com/rharriszzz/fft-image-explorer/main/secrets/image.png",
            "https://raw.githubusercontent.com/rharriszzz/fft-image-explorer/main/docs/figures/../secret.png",
            "https://raw.githubusercontent.com/rharriszzz/fft-image-explorer/main/docs/figures/local-fft-card.png?raw=true",
        ]:
            data = copy.deepcopy(self.data)
            project = next(p for p in data["projects"]
                           if p["slug"] == "fft-image-explorer")
            project["image"]["url"] = bad_url
            with self.subTest(bad_url=bad_url), self.assertRaises(ValueError):
                build.validate(data)

    def test_recipes_displays_reviewed_homepage_screenshot(self):
        recipes = next(p for p in self.data["projects"] if p["slug"] == "recipes")
        image = recipes["image"]
        self.assertEqual(image["url"], "https://raw.githubusercontent.com/rharriszzz/recipes/main/images/homepage-card.png")
        self.assertEqual(image["source"], "https://github.com/rharriszzz/recipes/blob/main/images/homepage-card.png")
        card = build.render_card(recipes)
        images = [attrs for tag, attrs in Document(card).elements if tag == "img"]
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["src"], image["url"])
        self.assertIn("homepage screenshot", images[0]["alt"])
        self.assertIn(image["caption"], card)
        self.assertNotIn("image-placeholder", card)
        published = json.loads((ROOT / "dist/projects.json").read_text())
        self.assertEqual(next(p for p in published["projects"] if p["slug"] == "recipes")["image"], image)

    def test_listed_flag_must_be_boolean(self):
        data = copy.deepcopy(self.data)
        data["projects"][0]["listed"] = "false"
        with self.assertRaises(ValueError):
            build.validate(data)

    def test_private_duplicate_or_unsafe_entries_are_rejected(self):
        for mutation in ("private", "duplicate", "image", "url"):
            data = copy.deepcopy(self.data)
            if mutation == "private":
                data["projects"][0]["repository"]["public"] = False
            elif mutation == "duplicate":
                data["projects"].append(data["projects"][0])
            elif mutation == "image":
                data["projects"][0]["image"]["path"] = "../private.png"
            else:
                data["projects"][0]["site"]["url"] = "javascript:alert(1)"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                build.validate(data)

    def test_all_local_assets_and_anchor_targets_exist(self):
        ids = [a["id"] for _, a in self.doc.elements if "id" in a]
        self.assertEqual(len(ids), len(set(ids)))
        for _, attrs in self.doc.elements:
            for key in ("href", "src"):
                url = attrs.get(key, "")
                if url.startswith("#"):
                    self.assertIn(url[1:], ids)
                elif url and not urlsplit(url).scheme:
                    self.assertTrue((ROOT / "dist" / unquote(url)).exists(), url)

    def test_images_and_links_have_accessible_names(self):
        for tag, attrs in self.doc.elements:
            if tag == "img":
                self.assertTrue(attrs.get("alt"))
                self.assertIn("width", attrs)
                self.assertIn("height", attrs)
        self.assertIn('class="skip-link"', self.page)
        self.assertIn('lang="en"', self.page)
        self.assertIn('name="viewport"', self.page)

    def test_catalog_text_is_escaped(self):
        project = copy.deepcopy(self.data["projects"][0])
        project["title"] = '<script>alert("x")</script>'
        rendered = build.render_card(project)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_publication_contains_only_allowlisted_files(self):
        expected = set(build.STATIC_FILES) | {"index.html", ".nojekyll", "projects.json"}
        expected |= {p["image"]["path"] for p in self.data["projects"] if p.get("listed", True) and "image" in p and "path" in p["image"]}
        actual = {p.relative_to(ROOT / "dist").as_posix() for p in (ROOT / "dist").rglob("*") if p.is_file()}
        self.assertEqual(actual, expected)
        self.assertFalse(any(p.is_symlink() for p in (ROOT / "dist").rglob("*")))

    def test_unreferenced_files_are_never_published(self):
        # A future local screenshot or stray data file must not enter the artifact.
        with tempfile.NamedTemporaryFile(dir=ROOT / "assets", suffix=".txt") as stray:
            stray.write(b"not intended for publication")
            stray.flush()
            build.build()
            self.assertFalse((ROOT / "dist/assets" / Path(stray.name).name).exists())


if __name__ == "__main__":
    unittest.main()
