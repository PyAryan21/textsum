import sys
import re
import requests
from bs4 import BeautifulSoup


URL_RE = re.compile(r'^https?://', re.IGNORECASE)


def read_input(source: str) -> str:
    if source == '-':
        return sys.stdin.read()
    if URL_RE.match(source):
        return _fetch_url(source)
    return _read_file(source)


def _read_file(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        return f.read()


def _fetch_url(url: str) -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; TextSum/1.0)'}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    return soup.get_text(separator='\n')
