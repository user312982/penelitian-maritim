"""Ambil screenshot semua halaman dashboard langsung dari web app yang berjalan.

Pakai:
    python scripts/screenshot.py            # jalankan app sendiri, simpan ke images/
    python scripts/screenshot.py --url http://localhost:8501   # pakai app yang sudah jalan

Butuh: pip install playwright && playwright install chromium
(atau pakai Google Chrome terpasang, dipakai otomatis jika ada).
"""

import argparse
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import Error, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images"
PORT = 8599

# (nama file, path URL halaman Streamlit)
PAGES = [
    ("peta-utama", "/"),
    ("detail-deteksi", "/detail"),
    ("unggah-citra", "/unggah"),
]
MAP_MODES = [("heatmap", "Heatmap"), ("cluster", "Cluster")]


def wait_for_server(url: str, timeout: float = 60) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url + "/_stcore/health", timeout=2)
            return
        except OSError:
            time.sleep(1)
    sys.exit(f"Server tidak merespons di {url}")


def settle(page, has_map: bool) -> None:
    """Tunggu Streamlit selesai render (dan tile satelit Esri untuk halaman peta)."""
    page.wait_for_selector('[data-testid="stMainBlockContainer"] h1', timeout=60_000)
    page.wait_for_timeout(1000)
    if has_map:
        frame = page.frame_locator("iframe").first
        frame.locator(".leaflet-tile-loaded").first.wait_for(timeout=60_000)
    page.wait_for_timeout(3000)


def launch(p):
    try:
        return p.chromium.launch(channel="chrome")
    except Error:
        return p.chromium.launch()


def capture(base_url: str) -> None:
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = launch(p)
        for scheme in ("light", "dark"):
            page = browser.new_page(
                viewport={"width": 1440, "height": 1100}, color_scheme=scheme, device_scale_factor=1
            )
            for name, path in PAGES:
                page.goto(base_url + path)
                settle(page, path == "/")
                page.screenshot(path=OUT / f"{name}-{scheme}.png", full_page=True)
                print(f"  images/{name}-{scheme}.png")

            if scheme == "light":
                for name, label in MAP_MODES:
                    page.goto(base_url + "/")
                    settle(page, True)
                    page.locator("button", has_text=label).click()
                    settle(page, True)
                    page.screenshot(path=OUT / f"peta-{name}-{scheme}.png", full_page=True)
                    print(f"  images/peta-{name}-{scheme}.png")
            page.close()
        browser.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", help="URL app yang sudah berjalan; jika kosong, app dijalankan otomatis")
    args = ap.parse_args()

    if args.url:
        capture(args.url.rstrip("/"))
        return

    base_url = f"http://localhost:{PORT}"
    server = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true",
         f"--server.port={PORT}", "--browser.gatherUsageStats=false"],
        cwd=ROOT, stdout=subprocess.DEVNULL,
    )
    try:
        wait_for_server(base_url)
        capture(base_url)
    finally:
        server.terminate()
        server.wait()


if __name__ == "__main__":
    main()
