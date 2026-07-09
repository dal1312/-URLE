#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import webbrowser
import os

PORT = 8000
ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    os.chdir(ROOT)
    url = f"http://localhost:{PORT}/00_RUNTIME/index.html"
    print(f"Forli Digital Twin server: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    ThreadingHTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler).serve_forever()
