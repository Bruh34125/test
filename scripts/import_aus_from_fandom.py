"""Import Undertale AUs from Fandom category pages into aus/<id>/au.json.

Usage:
  python scripts/import_aus_from_fandom.py

Notes:
- Attempts to crawl pagination from the provided category URL.
- Excludes entries that look NSFW based on keyword filtering.
- Generates default metadata so game can load all imported AUs.
"""

from __future__ import annotations
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import html
import json
import os
import re
from pathlib import Path

ROOT_URL = "https://undertale-au.fandom.com/wiki/Category:AUs"
OUT_DIR = Path("aus")

LINK_RE = re.compile(r'<a[^>]*class="category-page__member-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
NEXT_RE = re.compile(r'<a[^>]*class="category-page__pagination-next"[^>]*href="([^"]+)"', re.I)
TAG_RE = re.compile(r"<[^>]+>")

NSFW_RE = re.compile(
    r"(nsfw|18\+|r18|rule\s*34|lewd|smut|sex|porn|hentai|futa|yaoi|yuri|lust)",
    re.I,
)


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return slug or "unnamed_au"


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(req, timeout=30).read().decode("utf-8", "ignore")


def crawl_names(start_url: str) -> list[str]:
    names: list[str] = []
    seen_urls = set()
    url = start_url
    while url and url not in seen_urls:
        seen_urls.add(url)
        text = fetch(url)

        for _, raw_name in LINK_RE.findall(text):
            name = html.unescape(TAG_RE.sub("", raw_name)).strip()
            if not name or NSFW_RE.search(name):
                continue
            names.append(name)

        next_m = NEXT_RE.search(text)
        url = urljoin(url, html.unescape(next_m.group(1))) if next_m else None

    deduped = []
    for n in names:
        if n not in deduped:
            deduped.append(n)
    return deduped


def write_au(name: str) -> None:
    au_id = slugify(name)
    folder = OUT_DIR / au_id
    folder.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": au_id,
        "name": name,
        "description": f"Imported from Fandom category listing: {name}.",
        "authors": ["community"],
        "special_rule": "Imported AU entry with default prototype behavior.",
        "enemy_hp": 30,
        "reward_item": f"relic_{au_id}",
        "act_line": f"You attempt to understand {name}.",
    }
    (folder / "au.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    names = crawl_names(ROOT_URL)
    if not names:
        raise SystemExit("No AUs discovered. Check network access or source page format.")

    OUT_DIR.mkdir(exist_ok=True)
    for name in names:
        write_au(name)

    report = {"count": len(names), "source": ROOT_URL, "nsfw_filter": NSFW_RE.pattern}
    Path("data").mkdir(exist_ok=True)
    Path("data/au_import_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Imported {len(names)} AUs into {OUT_DIR}/")


if __name__ == "__main__":
    main()
