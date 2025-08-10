#!/usr/bin/env python3
"""Create a snapshot dataset from documentation URLs.

Reads URLs from data/sources/urls.txt, fetches HTML with a browser-like
User-Agent, extracts readable text using BeautifulSoup, saves .txt files
and writes a manifest.json with metadata.

Usage:
  python scripts/make_dataset.py
"""

from __future__ import annotations

import datetime
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional

import requests
from bs4 import BeautifulSoup


DATASETS_DIR = Path("data/datasets")
URLS_FILE = Path("data/sources/urls.txt")


@dataclass
class SavedDoc:
    file: str
    url: str
    title: str
    sha256: str
    bytes: int
    fetched_at: str


def read_urls(urls_file: Path) -> List[str]:
    if not urls_file.exists():
        raise FileNotFoundError(f"URLs file not found: {urls_file}")
    # Strip BOM if present and ignore comments/blank lines
    raw = urls_file.read_text(encoding="utf-8", errors="ignore")
    urls: List[str] = []
    for line in raw.splitlines():
        ln = line.strip().lstrip("\ufeff")
        if not ln or ln.startswith("#"):
            continue
        urls.append(ln)
    return urls


def fetch_html(url: str, timeout: int = 30) -> Optional[str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[warn] fetch failed: {url} -> {e}")
        return None


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Remove non-content elements
    for tag in soup(["script", "style", "noscript", "template", "svg"]):
        tag.decompose()
    # Get text, normalize whitespace
    text = soup.get_text("\n")
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)


def title_from_url(url: str) -> str:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if path:
        return path.replace("/", " - ").replace("-", " ").title()
    return parsed.netloc.replace("www.", "")


def safe_filename_from_url(url: str, extension: str = ".txt") -> str:
    import re
    from urllib.parse import urlparse

    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "_")
    path = parsed.path.replace("/", "_").replace("-", "_")
    name = re.sub(r"[^\w_]", "", f"{domain}{path}")
    return (name[:100] if len(name) > 100 else name) + extension


def save_text(content: str, out_dir: Path, filename: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    fp = out_dir / filename
    fp.write_text(content, encoding="utf-8")
    return fp


def build_snapshot(urls: Iterable[str]) -> Path:
    snapshot_dir = DATASETS_DIR / f"docs_snapshot_{datetime.date.today().isoformat()}"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    manifest: List[SavedDoc] = []
    saved = 0
    for url in urls:
        html = fetch_html(url)
        if not html:
            continue
        text = html_to_text(html)
        if not text or len(text) < 100:
            print(f"[warn] too little text, skipping: {url}")
            continue
        fname = safe_filename_from_url(url)
        fp = save_text(text, snapshot_dir, fname)
        meta = SavedDoc(
            file=fp.name,
            url=url,
            title=title_from_url(url),
            sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            bytes=fp.stat().st_size,
            fetched_at=datetime.datetime.utcnow().isoformat() + "Z",
        )
        manifest.append(meta)
        saved += 1
        print(f"[ok] saved: {url} -> {fp}")

    (snapshot_dir / "manifest.json").write_text(
        json.dumps([asdict(m) for m in manifest], indent=2), encoding="utf-8"
    )
    print(f"\nSummary: saved={saved} manifest={snapshot_dir / 'manifest.json'}")
    return snapshot_dir


def main() -> int:
    try:
        urls = read_urls(URLS_FILE)
    except Exception as e:
        print(f"[error] could not read URLs: {e}")
        return 1

    # Optional: filter out domains known to block scraping (can be re-enabled later)
    skip_domains = {"platform.openai.com", "docs.x.ai", "langchain-ai.github.io"}
    from urllib.parse import urlparse

    filtered = []
    for u in urls:
        host = urlparse(u).netloc
        if host in skip_domains:
            print(f"[info] skipping (blocked domain): {u}")
            continue
        filtered.append(u)

    snapshot_dir = build_snapshot(filtered)
    print(f"Dataset created at: {snapshot_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


