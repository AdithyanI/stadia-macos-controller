#!/usr/bin/env python3
"""Build the isolated static guide for Cloudflare Pages, without the Swift bridge."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ("index.html", "boot.js", "app.js", "styles.css")


def build(output: Path, source_sha: str) -> None:
    # Refuse an arbitrary delete target: builds replace only the owned dist directory.
    if output.resolve() != ROOT / "dist":
        raise ValueError("Build output must be the repository's dist directory")
    mappings = (ROOT / "config/mappings.json").read_bytes()
    json.loads(mappings)  # Never publish invalid JSON.
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    for name in ASSETS:
        shutil.copyfile(ROOT / "guide" / name, output / name)
    (output / "api").mkdir()
    (output / "api/mappings.json").write_bytes(mappings)
    (output / "api/health.json").write_text(
        json.dumps(
            {"status": "ok", "config": "config/mappings.json", "source_sha": source_sha}
        ) + "\n",
        encoding="utf-8",
    )
    # Explicit 404 disables Pages' implicit SPA fallback.
    (output / "404.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        "<title>Not found</title><h1>Not found</h1></html>\n",
        encoding="utf-8",
    )
    (output / "_redirects").write_text(
        "/api/mappings /api/mappings.json 200\n"
        "/api/health /api/health.json 200\n",
        encoding="utf-8",
    )
    (output / "_headers").write_text(
        "/*\n"
        "  Cache-Control: no-store\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: no-referrer\n"
        "  X-Frame-Options: DENY\n"
        "  Content-Security-Policy: default-src 'self'; script-src 'self'; "
        "style-src 'self'; img-src 'self' data:; connect-src 'self'; "
        "object-src 'none'; base-uri 'none'; frame-ancestors 'none'\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-sha", help="Release identity; defaults to CF_PAGES_COMMIT_SHA or git HEAD")
    args = parser.parse_args()
    source_sha = args.source_sha or os.environ.get("CF_PAGES_COMMIT_SHA") or subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
    ).strip()
    build(ROOT / "dist", source_sha)
    print(f"[build-controller-guide] dist ready ({source_sha})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
