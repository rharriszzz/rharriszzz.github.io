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
        self.assertEqual(cards, [p["slug"] for p in self.data["projects"]])
        self.assertNotIn("{{", self.page)

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
        self.assertIn('role="status"', self.page)
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
        expected |= {p["image"]["path"] for p in self.data["projects"] if "image" in p}
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
