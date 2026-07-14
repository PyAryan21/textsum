import hashlib
import json
import os
import time

TTL = 86400


def _cache_dir():
    base = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
    path = os.path.join(base, "textsum")
    os.makedirs(path, exist_ok=True)
    return path


def _key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:32]


def get(url: str) -> str | None:
    path = os.path.join(_cache_dir(), _key(url))
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            entry = json.load(f)
        if time.time() - entry["time"] > TTL:
            os.remove(path)
            return None
        return entry["text"]
    except (OSError, json.JSONDecodeError):
        return None


def set(url: str, text: str):
    path = os.path.join(_cache_dir(), _key(url))
    try:
        with open(path, "w") as f:
            json.dump({"url": url, "text": text, "time": time.time()}, f)
    except OSError:
        pass
