"""Print an offline study HTML page to PDF with headless Microsoft Edge (or Chrome/Chromium).

Bridge sets keep hints and solutions in <details class="hint"> / <details class="sol"> blocks.
Modes:
  problems   strip every hint/solution block (a clean worksheet to write on)
  solutions  expand every hint/solution block
  asis       print the page as it is (aid sheets, worked-solution pages)

Always prints in light mode with print margins, then reports the page count so the
caller can check it (e.g. an aid sheet must be exactly 2 pages).

Usage:
  python print_pdf.py <page.html> <out.pdf> [problems|solutions|asis]
"""
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Any Chromium-based browser can print to PDF headlessly. Edge ships with Windows, so it's tried first.
BROWSER_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
BROWSER_COMMANDS = ["msedge", "microsoft-edge", "google-chrome", "chromium", "chromium-browser"]


def find_edge() -> str:
    for path in BROWSER_PATHS:
        if Path(path).exists():
            return path
    for name in BROWSER_COMMANDS:
        if found := shutil.which(name):
            return found
    sys.exit("No Edge or Chrome found; one is needed for headless PDF printing.")


def prepare(html: str, mode: str) -> str:
    # Dark mode would print light text on white paper, so neutralize it.
    html = html.replace("@media (prefers-color-scheme: dark)", "@media (prefers-color-scheme: no-preference-never)")
    if mode != "asis":
        html = html.replace(
            "</style>",
            "@page{margin:14mm} body{background:#fff} main{padding-top:0} .card{break-inside:avoid}</style>",
            1,
        )
    if mode == "problems":
        html = re.sub(r'\s*<details class="(hint|sol)">.*?</details>', "", html, flags=re.S)
    elif mode == "solutions":
        html = html.replace('<details class="hint">', '<details class="hint" open>')
        html = html.replace('<details class="sol">', '<details class="sol" open>')
    return html


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    mode = sys.argv[3] if len(sys.argv) > 3 else "asis"
    if mode not in {"problems", "solutions", "asis"}:
        sys.exit(f"Unknown mode {mode!r}")

    # Edge keeps its profile locked briefly after printing, so it gets its own long-lived
    # folder instead of living inside the temp dir (which would fail to clean up).
    profile = Path(tempfile.gettempdir()) / "bridge-edge-profile"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(prepare(src.read_text(encoding="utf-8"), mode), encoding="utf-8")
        if out.exists():
            out.unlink()
        subprocess.run(
            [find_edge(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
             f"--user-data-dir={profile}", f"--print-to-pdf={out}", page.as_uri()],
            check=False, capture_output=True, timeout=120,
        )
        # The Edge launcher can return before the PDF is fully written, so wait until
        # the file exists and its size has stopped changing.
        last_size, deadline = -1, time.time() + 60
        while time.time() < deadline:
            if out.exists() and out.stat().st_size == last_size and last_size > 0:
                break
            last_size = out.stat().st_size if out.exists() else -1
            time.sleep(0.5)

    if not out.exists():
        sys.exit("Edge did not produce a PDF.")
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(str(out)).pages)
        print(f"{out.name}: {pages} pages")
    except ImportError:
        print(f"{out.name}: written (install pypdf to report page count)")


if __name__ == "__main__":
    main()
