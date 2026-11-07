from __future__ import annotations

import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    docs = ROOT / "docs"
    pages = [str(page.relative_to(docs)).replace("\\", "/") for page in sorted(docs.rglob("*.html"))]
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(docs))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                for width in (360, 390, 768, 1440):
                    page = browser.new_page(viewport={"width": width, "height": 900})
                    errors: list[str] = []
                    page.on("pageerror", lambda error, _errors=errors: _errors.append(str(error)))
                    for path in pages:
                        response = page.goto(f"http://127.0.0.1:{server.server_port}/{path}", wait_until="load")
                        assert response and response.status == 200, path
                        overflow = page.evaluate("Math.max(0, document.documentElement.scrollWidth - innerWidth)")
                        assert overflow == 0, f"{path} at {width}px: horizontal overflow {overflow}px"
                        outside = page.locator("nav a, nav button").evaluate_all(
                            "els => els.filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.left < 0 || r.right > innerWidth + 1); }).length"
                        )
                        assert outside == 0, f"{path} at {width}px: {outside} navigation controls outside viewport"
                        assert not errors, errors
                        print(f"{path}: width={width}, overflow={overflow}, outside_controls={outside}")
                    page.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
