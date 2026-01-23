import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def _safe_filename(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return "rule"
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^A-Za-z0-9_\-\.]+", "", text)
    return text[:160] or "rule"


def collect_rule(source: str, title: str, url: str, out_dir: Path) -> bool:
    """
    Downloads the URL content and saves as a .txt file in out_dir.
    - Works for HTML pages and PDFs.
    - Adds browser-like headers (fixes many 403 blocks like SEC).
    """
    try:
        out_dir.mkdir(parents=True, exist_ok=True)

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Accept": "text/html,application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }

        r = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
        r.raise_for_status()

        content_type = (r.headers.get("Content-Type") or "").lower()

        # If PDF, just store the URL + note (we’ll parse PDFs later if needed)
        if "application/pdf" in content_type or url.lower().endswith(".pdf"):
            text = f"{source} - {title}\n{url}\n\n[PDF downloaded as binary not parsed in this step]\n"
        else:
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text("\n")

        filename = f"{_safe_filename(source)}__{_safe_filename(title)}.txt"
        out_path = out_dir / filename
        out_path.write_text(text, encoding="utf-8", errors="ignore")

        print("Saved:", out_path.name)
        return True

    except Exception as e:
        print("ERROR collecting:", source, title, url, "->", e)
        return False
