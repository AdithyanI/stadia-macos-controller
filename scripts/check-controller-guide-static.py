#!/usr/bin/env python3
"""Check the published static artifact against its canonical mapping source."""

import json
import shutil
import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen


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
    assert 'fetch("/api/mappings.json"' in (output / "app.js").read_text()
    node = shutil.which("node")
    if node:
        for name in ("boot.js", "app.js"):
            subprocess.run([node, "--check", str(output / name)], check=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(SimpleHTTPRequestHandler, directory=str(output)),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        for route, mime in (
            ("/", "text/html"), ("/api/mappings.json", "application/json"),
            ("/api/health.json", "application/json"), ("/styles.css", "text/css"),
        ):
            with urlopen(base + route, timeout=3) as response:
                assert response.status == 200
                assert response.headers.get_content_type() == mime
                if route == "/api/mappings.json":
                    assert response.read() == (ROOT / "config/mappings.json").read_bytes()
        try:
            urlopen(base + "/config/mappings.json", timeout=3)
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("Static preview exposed source configuration")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
    print("[check-controller-guide-static] artifact isolation, mappings, HTTP routes, JavaScript and headers passed")


if __name__ == "__main__":
    main()
