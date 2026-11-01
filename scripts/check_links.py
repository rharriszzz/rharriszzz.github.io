#!/usr/bin/env python3
"""Check every external page and asset in the built index. No GitHub token needed."""
import argparse
import concurrent.futures
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.urls.add(value)


def check(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "rharriszzz-project-index-link-check/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                response.read(1024)
                return url, response.status, response.url
        except (OSError, urllib.error.URLError) as error:
            if attempt == 2:
                return url, "FAILED", str(error)
            time.sleep(attempt + 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", help="Also check all built page assets and catalog at the deployed URL")
    args = parser.parse_args()
    links = Links()
    links.feed((ROOT / "dist/index.html").read_text())
    urls = {u for u in links.urls if u.startswith("https://")}
    # The production canonical URL is checked after deployment, not before it exists.
    if not args.base_url:
        urls.discard("https://rharriszzz.github.io/")
    data = json.loads((ROOT / "projects.json").read_text())
    urls |= {p["image"]["source"] for p in data["projects"] if "image" in p}
    if args.base_url:
        urls.add(args.base_url)
        urls |= {urllib.parse.urljoin(args.base_url, u) for u in links.urls if not u.startswith(("https://", "#"))}
        urls.add(urllib.parse.urljoin(args.base_url, "projects.json"))
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for url, status, destination in pool.map(check, sorted(urls)):
            print(f"{status} {url}" + (f" → {destination}" if url != destination else ""))
            if status == "FAILED":
                failures.append(url)
    print(f"Checked {len(urls)} links; {len(failures)} failures")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
