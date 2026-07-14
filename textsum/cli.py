import json
import sys
import time

import click
from tqdm import tqdm

from textsum import config as cfg
from textsum import input_utils
from textsum import extractive
from textsum import abstractive
from textsum import export
from textsum import interactive


def _detect_language(text: str) -> str | None:
    try:
        from langdetect import detect
        return detect(text)
    except ImportError:
        return None
    except Exception:
        return None


def _load_stopwords(lang: str):
    if lang and lang != "en":
        try:
            from nltk.corpus import stopwords as sw
            try:
                return set(sw.words(lang))
            except OSError:
                return None
        except ImportError:
            return None
    return None


def _filter_summary_sentences(text: str, num_lines: int) -> tuple[str, list[tuple[str, float]]]:
    return extractive.summarize(text, num_lines=num_lines)


@click.command(context_settings={"ignore_unknown_options": False})
@click.argument("inputs", nargs=-1, required=True)
@click.option("-m", "--mode", type=click.Choice(["extractive", "abstractive"]), help="Summarization mode")
@click.option("-l", "--lines", type=int, help="Number of sentences in summary")
@click.option("-o", "--output", type=click.Path(), help="Write to file instead of stdout")
@click.option("-f", "--format", "fmt", type=click.Choice(["text", "json", "markdown", "html"]), help="Output format")
@click.option("-i", "--interactive", "interactive_mode", is_flag=True, help="Interactive sentence selection")
@click.option("-c", "--config", "config_path", type=click.Path(), help="Config file path")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.option("--model", help="HuggingFace model for abstractive mode")
@click.option("--prompt", help="Custom prompt for abstractive mode")
@click.option("--api-key", help="API key (reserved for future use)")
def main(inputs, mode, lines, output, fmt, interactive_mode, config_path, verbose, model, prompt, api_key):
    config = cfg.load_config(config_path)

    mode = mode or config.get("mode", "extractive")
    lines = lines or config.get("lines", 5)
    fmt = fmt or config.get("format", "text")
    model = model or config.get("model", "facebook/bart-large-cnn")
    prompt = prompt or config.get("prompt")
    verbose = verbose or config.get("verbose", False)

    all_summaries = []

    for source in inputs:
        if verbose:
            tqdm.write(f"[textsum] reading: {source}")
        t0 = time.time()

        text = input_utils.read_input(source)

        if verbose:
            lang = _detect_language(text)
            tqdm.write(f"[textsum] language: {lang or 'unknown'} | length: {len(text)} chars | time: {time.time()-t0:.2f}s")

        if mode == "extractive":
            summary, scored = extractive.summarize(text, num_lines=lines)
        else:
            summary, scored = abstractive.summarize(text, num_lines=lines, model_name=model, prompt=prompt, verbose=verbose)

        if interactive_mode:
            if mode != "extractive":
                if verbose:
                    tqdm.write("[textsum] interactive mode uses extractive sentences for selection")
                _, scored = extractive.summarize(text, num_lines=lines * 3)
                scored = sorted(scored, key=lambda x: -x[1])
            scored = interactive.run(scored, lines)
            if not scored:
                continue
            summary = "\n".join(s for s, _ in scored)

        meta = {"source": source, "mode": mode, "model": model} if verbose else None
        all_summaries.append({
            "source": source,
            "summary": summary,
            "scored": scored,
            "meta": meta,
        })

    result_text = _render(all_summaries, fmt)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(result_text + "\n")
        if verbose:
            click.echo(f"[textsum] written to: {output}")
    else:
        click.echo(result_text)


def _render(summaries: list[dict], fmt: str) -> str:
    if len(summaries) == 1:
        s = summaries[0]
        return _render_one(s["summary"], s["scored"], s["meta"], fmt)

    parts = []
    for s in summaries:
        header = f"# {s['source']}\n" if fmt == "markdown" else f"--- {s['source']} ---\n"
        body = _render_one(s["summary"], s["scored"], s["meta"], fmt)
        parts.append(header + body)
    return "\n\n".join(parts)


def _render_one(summary: str, scored: list[tuple[str, float]], meta: dict | None, fmt: str) -> str:
    if fmt == "json":
        return export.format_json(summary, scored, meta)
    elif fmt == "markdown":
        return export.format_markdown(summary, scored)
    elif fmt == "html":
        return export.format_html(summary, scored)
    else:
        return export.format_text(summary, scored)


if __name__ == "__main__":
    main()
