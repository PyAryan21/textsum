import json
import os

DEFAULT_CONFIG = {
    "mode": "extractive",
    "lines": 5,
    "model": "facebook/bart-large-cnn",
    "prompt": None,
    "format": "text",
    "verbose": False,
}


def config_path():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "textsumrc")


def load_config(path=None) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    path = path or config_path()
    if os.path.exists(path):
        try:
            with open(path) as f:
                cfg.update(json.load(f))
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save_config(cfg: dict, path=None):
    path = path or config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
