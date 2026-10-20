#!/usr/bin/env python3
"""Check the published static artifact against its canonical mapping source."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/build-controller-guide.py")],
        check=True,
    )
    output = ROOT / "dist"
    expected = {
        "index.html", "boot.js", "app.js", "styles.css", "404.html",
        "api/mappings.json", "api/health.json", "_redirects", "_headers",
    }
    assert {str(p.relative_to(output)) for p in output.rglob("*") if p.is_file()} == expected
    assert (output / "api/mappings.json").read_bytes() == (ROOT / "config/mappings.json").read_bytes()
    for name in ("index.html", "boot.js", "app.js", "styles.css"):
        assert (output / name).read_bytes() == (ROOT / "guide" / name).read_bytes()
    health = json.loads((output / "api/health.json").read_text())
    assert health["status"] == "ok" and health["source_sha"]
    redirects = (output / "_redirects").read_text().splitlines()
    assert redirects == [
        "/api/mappings /api/mappings.json 200",
        "/api/health /api/health.json 200",
    ]
    assert "frame-ancestors 'none'" in (output / "_headers").read_text()
    assert "Cache-Control: no-store" in (output / "_headers").read_text()
    print("[check-controller-guide-static] artifact isolation, mappings, routes and headers passed")


if __name__ == "__main__":
    main()
