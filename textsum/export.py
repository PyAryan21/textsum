import json
from html import escape


def format_text(summary: str, scores: list[tuple[str, float]] | None = None) -> str:
    if scores is None:
        return summary
    lines = []
    for sent, score in scores:
        bar = "#" * round(score * 20)
        pct = f"{score * 100:.0f}%"
        lines.append(f"[{pct:>4}] {bar} {sent}")
    return "\n".join(lines)


def format_json(summary: str, scores: list[tuple[str, float]] | None, meta: dict | None = None) -> str:
    obj = {"summary": summary}
    if scores:
        obj["sentences"] = [{"text": s, "confidence": round(score, 4)} for s, score in scores]
    if meta:
        obj["meta"] = meta
    return json.dumps(obj, indent=2, ensure_ascii=False)


def format_markdown(summary: str, scores: list[tuple[str, float]] | None = None) -> str:
    lines = ["## Summary\n"]
    if scores:
        for sent, score in scores:
            confidence = f"*(confidence: {score * 100:.0f}%)*"
            lines.append(f"- {sent} {confidence}")
    else:
        for sent in summary.split("\n"):
            if sent.strip():
                lines.append(f"- {sent.strip()}")
    return "\n".join(lines)


def format_html(summary: str, scores: list[tuple[str, float]] | None = None) -> str:
    parts = ["<!DOCTYPE html><html><head><meta charset='utf-8'><title>Summary</title>",
             "<style>body{font-family:sans-serif;max-width:720px;margin:2em auto;line-height:1.6}"
             ".bar{display:inline-block;height:1em;background:#4f46e5;border-radius:3px;vertical-align:middle;margin-right:8px}"
             ".sentence{margin:.5em 0;padding:.3em .6em;background:#f8fafc;border-radius:4px}"
             "</style></head><body><h1>Summary</h1>"]
    if scores:
        for sent, score in scores:
            bar_width = round(score * 200)
            pct = f"{score * 100:.0f}%"
            bar = f"<span class='bar' style='width:{bar_width}px;background:#4f46e5;display:inline-block;height:1em;border-radius:3px;vertical-align:middle;margin-right:8px'></span>"
            parts.append(f"<div class='sentence'>{bar}<strong>{pct}</strong> {escape(sent)}</div>")
    else:
        for sent in summary.split("\n"):
            if sent.strip():
                parts.append(f"<p>{escape(sent.strip())}</p>")
    parts.append("</body></html>")
    return "\n".join(parts)
