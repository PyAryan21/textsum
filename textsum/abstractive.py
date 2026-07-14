import warnings

import nltk
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

nltk.download("punkt_tab", quiet=True)

SUPPORTED_MODELS = {
    "bart": "facebook/bart-large-cnn",
    "t5-small": "t5-small",
    "distilbart": "distilbart-cnn-12-6",
}

_pipelines = {}


def _get_pipeline(model_name: str):
    if model_name not in _pipelines:
        from transformers import pipeline
        warnings.filterwarnings("ignore", category=FutureWarning)
        _pipelines[model_name] = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name,
        )
    return _pipelines[model_name]


def _estimate_tokens(text: str) -> int:
    return len(text.split())


def summarize(
    text: str,
    num_lines: int = 5,
    model_name: str = "facebook/bart-large-cnn",
    prompt: str | None = None,
    verbose: bool = False,
) -> tuple[str, list[tuple[str, float]]]:
    pipe = _get_pipeline(model_name)

    if prompt:
        text = f"{prompt}\n\n{text}"

    max_chunk = 1024
    min_length = max(10, num_lines * 8)
    max_length = num_lines * 30

    words = text.split()
    total_tokens = len(words)

    if total_tokens <= max_chunk:
        if verbose:
            tqdm.write(f"[abstractive] input: {total_tokens} tokens")
        result = pipe(text, max_length=max_length, min_length=min_length, do_sample=False)
        summary = result[0]["summary_text"]
        sentences = sent_tokenize(summary)
        return summary, [(s, 1.0 / len(sentences)) for s in sentences]

    chunks = []
    for i in range(0, total_tokens, max_chunk):
        chunks.append(" ".join(words[i:i + max_chunk]))

    if verbose:
        tqdm.write(f"[abstractive] splitting into {len(chunks)} chunks ({total_tokens} tokens)")

    summaries = []
    for chunk in tqdm(chunks, desc="Summarizing", disable=not verbose):
        result = pipe(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(result[0]["summary_text"])

    combined = " ".join(summaries)
    combined_tokens = _estimate_tokens(combined)

    if combined_tokens > max_chunk * 1.5:
        if verbose:
            tqdm.write(f"[abstractive] re-summarizing combined output ({combined_tokens} tokens)")
        result = pipe(combined, max_length=max_length, min_length=min_length, do_sample=False)
        summary = result[0]["summary_text"]
    else:
        summary = combined

    sentences = sent_tokenize(summary)
    return summary, [(s, 1.0 / len(sentences)) for s in sentences]
