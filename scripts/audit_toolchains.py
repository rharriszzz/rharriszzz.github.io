#!/usr/bin/env python3
"""Read-only, bounded audit of public GitHub repository toolchain versions.

Policy snapshot: 2026-11-07. No code, dependency or GitHub setting is changed.
Historical documentation is not automatically rewritten.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = "rharriszzz"
POLICY_DATE = "2026-11-07"
EXCLUDE = {"HIS_profile"}
SITE_READY = {"github-pages-discovery"}
LATEST_ACTION = {
    "checkout": 7, "setup-python": 7, "setup-node": 7,
    "configure-pages": 6, "upload-pages-artifact": 5,
    "deploy-pages": 5, "upload-artifact": 7, "github-script": 9,
}
ACTION = re.compile(r"actions/([\w-]+)@v(\d+)")
PYTHON = re.compile(r"(?i)\bpython\s*(?:v(?:ersion)?\s*)?(3\.\d{1,2})\b")
PYTHON_COMMAND = re.compile(r"\bpython3\.(\d{1,2})\b")
PYTHON_CI = re.compile(r"python-version:\s*['\"]?(3\.\d{1,2})")
NODE = re.compile(r"(?i)\bnode(?:\.js)?\s*(?:v(?:ersion)?\s*)?(\d{2})\b")
NODE_CI = re.compile(r"node-version:\s*['\"]?(\d{2})")
NODE_ENGINE = re.compile(r'"node"\s*:\s*"[~^><= ]*(\d{2})')
PYTHON_MIN = re.compile(r'requires-python\s*=\s*["\x27][^"\x27]*3\.(\d{1,2})')
SKIP_DIRS = {
    ".git", ".venv", "node_modules", "vendor", "third_party", "fixtures",
    "generated", "archive", "archives", "history", "historical",
    "evidence", "snapshots", "dist", "build",
}


def get(url, structured=False):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "public-toolchain-audit"}
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(url, headers=headers), timeout=20) as response:
        raw = response.read(5_000_000 if structured else 150_001)
    if not structured and len(raw) > 150_000:
        raise ValueError("File too large for safe scanning")
    text = raw.decode("utf-8")
    return json.loads(text) if structured else text


def indexed(include_unlisted=False):
    entries = json.loads((ROOT / "projects.json").read_text())["projects"]
    names = [(p["slug"], bool(p.get("site", {}).get("url"))) for p in entries
             if p["slug"] not in EXCLUDE and p.get("repository", {}).get("public")
             and (include_unlisted or p.get("listed", True))]
    names.extend([(OWNER + ".github.io", True), ("github-pages-discovery", True)])
    return list(dict.fromkeys(names))


def public_repositories():
    names = []
    for page in range(1, 30):
        rows = get("https://api.github.com/users/" + OWNER +
                   "/repos?type=owner&per_page=100&page=" + str(page), True)
        names.extend((r["name"], False) for r in rows
                     if r.get("private") is False and r["name"] not in EXCLUDE)
        if len(rows) < 100:
            break
    return list(dict.fromkeys(names))


def candidate(path):
    parts = path.lower().split("/")
    if any(x in SKIP_DIRS for x in parts[:-1]):
        return False
    name = parts[-1]
    if len(parts) == 1 and (
        name.startswith(("readme", "requirements")) or name in {
            "package.json", "pyproject.toml", ".python-version", ".nvmrc",
            ".node-version", ".tool-versions", "tox.ini", "setup.cfg",
        }
    ):
        return True
    if len(parts) == 3 and parts[:2] == [".github", "workflows"]:
        return name.endswith((".yaml", ".yml"))
    if len(parts) <= 3 and parts[0] in {"docs", "guides"}:
        return name.endswith((".md", ".rst", ".txt")) and any(
            x in name for x in ("readme", "setup", "install", "environment",
                                "development", "python", "toolchain", "testing")
        )
    return False


def analyze(path, line, website):
    issues = []
    def add(kind, level, detail):
        issues.append({"rule": kind, "severity": level, "detail": detail})
    for m in ACTION.finditer(line):
        action, major = m.group(1), int(m.group(2))
        if action in LATEST_ACTION and major < LATEST_ACTION[action]:
            add("older-action", "warning",
                "actions/" + action + "@v" + str(major) +
                ": review current v" + str(LATEST_ACTION[action]))
    python_versions = set()
    for m in PYTHON.finditer(line):
        python_versions.add(int(m.group(1).split(".")[1]))
    for m in PYTHON_COMMAND.finditer(line):
        python_versions.add(int(m.group(1)))
    for m in PYTHON_CI.finditer(line):
        python_versions.add(int(m.group(1).split(".")[1]))
    if path == ".python-version":
        m = re.fullmatch(r"\s*3\.(\d{1,2})\s*", line)
        if m:
            python_versions.add(int(m.group(1)))
    for minor in sorted(python_versions):
        if minor <= 10:
            add("eol-python", "error" if website else "warning",
                "Python 3." + str(minor) + " is end-of-life")
        elif minor <= 13:
            add("security-only-python", "warning",
                "Python 3." + str(minor) + " gets security fixes, not routine bug fixes")
    for m in PYTHON_MIN.finditer(line):
        if int(m.group(1)) <= 13:
            add("minimum-compatibility", "notice",
                "Old minimum supported Python: verify before raising; not a new-setup recommendation")
    node_versions = set()
    for regex in (NODE, NODE_CI, NODE_ENGINE):
        node_versions.update(int(m.group(1)) for m in regex.finditer(line))
    if path in {".nvmrc", ".node-version"}:
        m = re.fullmatch(r"\s*v?(\d{2})\s*", line)
        if m:
            node_versions.add(int(m.group(1)))
    for major in sorted(node_versions):
        if major <= 20:
            add("eol-node", "error" if website else "warning",
                "Node " + str(major) + " is end-of-life; use a maintained LTS release")
        elif major == 22:
            add("maintenance-node", "notice", "Node 22 is maintenance LTS")
    return issues


def inspect_repo(name, declared_site):
    base = "https://api.github.com/repos/" + OWNER + "/" + quote(name)
    info = get(base, True)
    site = declared_site or name in SITE_READY or bool(info.get("has_pages"))
    branch = info["default_branch"]
    listing = get(base + "/git/trees/" + quote(branch) + "?recursive=1", True)
    if listing.get("truncated"):
        raise ValueError("GitHub returned a truncated tree")
    paths = sorted(x["path"] for x in listing["tree"]
                   if x.get("type") == "blob" and candidate(x["path"]))
    issues, skipped = [], []
    for path in paths[:120]:
        url = ("https://raw.githubusercontent.com/" + OWNER + "/" + quote(name) +
               "/" + quote(branch) + "/" + quote(path, safe="/"))
        try:
            body = get(url)
        except Exception as exc:
            skipped.append(path + ": " + type(exc).__name__)
            continue
        for n, line in enumerate(body.splitlines(), 1):
            for finding in analyze(path, line, site):
                issues.append({"file": path, "line": n, **finding,
                               "excerpt": line.strip()[:150]})
    if len(paths) > 120:
        skipped.append(str(len(paths) - 120) + " candidate files exceeded limit")
    return {"repository": name, "branch": branch, "website": site,
            "files_scanned": min(len(paths), 120),
            "findings": issues, "skipped": skipped}


def report(rows):
    lines = ["# Public toolchain audit", "",
             "Policy snapshot: " + POLICY_DATE + ". Read-only, default branches.",
             "HIS_profile excluded (no available test environment).",
             "All findings require review before changes.", "",
             "| Repository | Website | EOL errors | Warnings | Files |",
             "| --- | :---: | ---: | ---: | ---: |"]
    for row in rows:
        errors = sum(x["severity"] == "error" for x in row["findings"])
        warnings = sum(x["severity"] == "warning" for x in row["findings"])
        lines.append("| " + row["repository"] + " | " +
                     ("Yes" if row["website"] else "No") + " | " +
                     str(errors) + " | " + str(warnings) + " | " +
                     str(row["files_scanned"]) + " |")
    for row in rows:
        lines.extend(["", "## " + row["repository"], ""])
        for issue in row["findings"]:
            lines.append("- " + issue["severity"] + " " + issue["file"] + ":" +
                         str(issue["line"]) + " — " + issue["detail"] +
                         " (" + issue["excerpt"] + ")")
        if not row["findings"]:
            lines.append("No matching version problems in scanned files.")
        for skipped in row["skipped"]:
            lines.append("- INCOMPLETE: " + skipped)
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--all-indexed", action="store_true")
    modes.add_argument("--all-public", action="store_true")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--strict", action="store_true",
                        help="Fail if a website uses EOL software or coverage is incomplete")
    args = parser.parse_args()
    requested = (public_repositories() if args.all_public
                 else indexed(args.all_indexed))
    expected = dict(indexed(True))
    requested = [(n, site or expected.get(n, False))
                 for n, site in requested if n not in EXCLUDE]
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(inspect_repo, n, s): (n, s) for n, s in requested}
        for f in as_completed(futures):
            name, site = futures[f]
            try:
                results.append(f.result())
            except Exception as exc:
                results.append({"repository": name, "website": site,
                                "branch": "?", "files_scanned": 0, "findings": [],
                                "skipped": [type(exc).__name__ + ": " + str(exc)]})
    results.sort(key=lambda x: x["repository"].lower())
    if args.format == "json":
        print(json.dumps({"policy_as_of": POLICY_DATE, "results": results}, indent=2))
    else:
        print(report(results), end="")
    if args.strict and (any(row["skipped"] for row in results) or
                        any(row["website"] and any(f["severity"] == "error"
                            for f in row["findings"]) for row in results)):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
