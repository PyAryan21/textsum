import re
import sys

import requests
from bs4 import BeautifulSoup

from textsum.cache import get as cache_get, set as cache_set

URL_RE = re.compile(r"^https?://", re.IGNORECASE)

_PDF_IMPORTED = False
PdfReader = None


def _import_pdf():
    global _PDF_IMPORTED, PdfReader
    if _PDF_IMPORTED:
        return True
    try:
        from pypdf import PdfReader as PR
        PdfReader = PR
        _PDF_IMPORTED = True
        return True
    except ImportError:
        return False


def read_input(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    if URL_RE.match(source):
        cached = cache_get(source)
        if cached:
            return cached
        text = _fetch_url(source)
        cache_set(source, text)
        return text
    if _is_pdf(source):
        return _read_pdf(source)
    return _read_file(source)


def _read_file(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _fetch_url(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; TextSum/1.0)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    ct = resp.headers.get("Content-Type", "")
    if "application/pdf" in ct:
        import io
        if not _import_pdf():
            raise RuntimeError("pypdf is required for PDF URLs: pip install pypdf")
        reader = PdfReader(io.BytesIO(resp.content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n")


def _is_pdf(path: str) -> bool:
    if path.lower().endswith(".pdf"):
        return True
    try:
        with open(path, "rb") as f:
            return f.read(5) == b"%PDF-"
    except OSError:
        return False


def _read_pdf(path: str) -> str:
    if not _import_pdf():
        raise RuntimeError("pypdf is required for PDF files: pip install pypdf")
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)
