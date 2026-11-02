#!/usr/bin/env python3
"""Render the reviewed catalog and publish only explicitly referenced files."""
import datetime
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {"games", "tools", "research", "visualization", "craft"}
STATIC_FILES = ("style.css", "app.js", "assets/favicon.svg")


def escape(value):
    return html.escape(str(value), quote=True)


def validate_url(value):
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.netloc or parts.username or parts.password:
        raise ValueError(f"Expected a public HTTPS URL: {value}")


def validate(data, root=ROOT):
    datetime.date.fromisoformat(data["verifiedOn"])
    if data["owner"] != "rharriszzz":
        raise ValueError("This catalog is for rharriszzz’s public repositories")
    seen = set()
    for project in data["projects"]:
        slug = project["slug"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", slug) or slug in seen:
            raise ValueError(f"Invalid or duplicate repository: {slug}")
        seen.add(slug)
        repo = project["repository"]
        if repo["public"] is not True or repo["url"] != f"https://github.com/rharriszzz/{slug}":
            raise ValueError(f"Only verified public owner repositories may be listed: {slug}")
        datetime.date.fromisoformat(repo["lastPushed"])
        if not project["categories"] or not set(project["categories"]) <= CATEGORIES:
            raise ValueError(f"Unknown project category: {slug}")
        for key in ("title", "description", "technology", "kind"):
            if not isinstance(project[key], str) or not project[key].strip():
                raise ValueError(f"Missing {key}: {slug}")
        if (type(project["featured"]) is not bool or type(project["browserApp"]) is not bool
                or type(project.get("listed", True)) is not bool):
            raise ValueError(f"Expected boolean flags: {slug}")
        if "site" in project:
            validate_url(project["site"]["url"])
            if not project["site"]["detail"]:
                raise ValueError(f"Site type and host required: {slug}")
        if "image" in project:
            image = project["image"]
            path = Path(image["path"])
            if not re.fullmatch(r"assets/images/[a-z0-9-]+\.(png|jpg|svg|webp)", path.as_posix()):
                raise ValueError(f"Unexpected image path: {path}")
            candidate = root / path
            if not candidate.is_file() or candidate.is_symlink() or not candidate.resolve().is_relative_to(root.resolve()):
                raise ValueError(f"Missing or unsafe image: {path}")
            if not image["alt"] or not image["caption"]:
                raise ValueError(f"Image alt text and caption required: {slug}")
            validate_url(image["source"])
            if path.suffix == ".svg":
                svg = candidate.read_text()
                if re.search(r"<script|<foreignObject|\bon\w+\s*=|(?:href|src)\s*=\s*['\"](?:https?:|//|data:|javascript:)", svg, re.I):
                    raise ValueError(f"SVG must be a self-contained static image: {path}")


def render_card(project):
    p = project
    search = " ".join([p["slug"], p["title"], p["kind"], p["description"], p["technology"], p.get("note", ""), *p["categories"]])
    attrs = (f'data-project="{escape(p["slug"])}" data-categories="{escape(" ".join(p["categories"]))}" '
             f'data-browser="{str(p["browserApp"]).lower()}" data-search="{escape(search)}"')
    kind = f'<p class="card-kind{" browser" if p["browserApp"] else ""}">{escape(p["kind"])}</p>'
    repo = (f'<a href="{escape(p["repository"]["url"])}" aria-label="{escape(p["title"])} — GitHub Repository">'
            'GitHub Repository <span aria-hidden="true">↗</span></a>')
    title = f'<h4>{escape(p["title"])}</h4>'
    description = f'<p class="card-description">{escape(p["description"])}</p>'
    if not p["featured"]:
        return f'<article class="secondary-card" {attrs}>{kind}{title}{description}{repo}</article>'
    if "image" in p:
        im = p["image"]
        media = (f'<figure><img class="project-image" src="{escape(im["path"])}" alt="{escape(im["alt"])}" '
                 f'width="800" height="500" loading="lazy" decoding="async">'
                 f'<figcaption>{escape(im["caption"])}</figcaption></figure>')
    else:
        media = (f'<div class="image-placeholder" aria-label="No application screenshot available">'
                 f'<span>{escape(p.get("placeholder", p["title"]))}</span><small>{escape(p.get("placeholderDetail", "Local application · source available"))}</small></div>')
    note = f'<p class="card-note">{escape(p["note"])}</p>' if p.get("note") else ""
    live = (f'<a class="live-link" href="{escape(p["site"]["url"])}" aria-label="{escape(p["title"])} — Live Site">'
            'Live Site <span aria-hidden="true">↗</span></a>') if "site" in p else ""
    detail = f'<p class="site-detail">{escape(p["site"]["detail"])}</p>' if "site" in p else ""
    return (f'<article class="project-card" {attrs}>{media}<div class="card-body">{kind}{title}{description}{note}'
            f'<p class="card-tech">{escape(p["technology"])}</p><div class="card-links">{live}{repo}</div>{detail}</div></article>')


def render(data):
    projects = [p for p in data["projects"] if p.get("listed", True)]
    date = datetime.date.fromisoformat(data["verifiedOn"])
    replacements = {
        "PROJECT_COUNT": str(len(projects)),
        "FEATURED_COUNT": str(sum(p["featured"] for p in projects)),
        "FEATURED_PROJECTS": "\n".join(render_card(p) for p in projects if p["featured"]),
        "OTHER_PROJECTS": "\n".join(render_card(p) for p in projects if not p["featured"]),
        "VERIFIED_ON": date.isoformat(),
        "VERIFIED_LABEL": f"{date.strftime('%B')} {date.day}, {date.year}",
    }
    page = (ROOT / "index.template.html").read_text()
    for key, value in replacements.items():
        page = page.replace("{{" + key + "}}", value)
    if "{{" in page:
        raise ValueError("Unresolved template marker")
    return page


def build():
    data = json.loads((ROOT / "projects.json").read_text())
    validate(data)
    listed_projects = [p for p in data["projects"] if p.get("listed", True)]
    output = ROOT / "dist"
    if output.is_symlink():
        raise ValueError("Refusing to replace a symlinked output directory")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    (output / "index.html").write_text(render(data))
    # Keep editorially unlisted entries in source control, not in the published catalog.
    (output / "projects.json").write_text(json.dumps({**data, "projects": listed_projects}, ensure_ascii=False, indent=2) + "\n")
    files = set(STATIC_FILES)
    files |= {p["image"]["path"] for p in listed_projects if "image" in p}
    for name in sorted(files):
        source = ROOT / name
        if source.is_symlink() or not source.resolve().is_relative_to(ROOT):
            raise ValueError(f"Unsafe publication source: {name}")
        dest = output / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    (output / ".nojekyll").touch()
    print(f"Built {len(listed_projects)} projects and {len(files) + 3} public files in dist/")


if __name__ == "__main__":
    build()
