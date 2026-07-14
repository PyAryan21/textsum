from transformers import pipeline

_summarizer = None


def _get_pipeline():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    return _summarizer


def summarize(text: str, num_lines: int = 5) -> str:
    pipe = _get_pipeline()
    max_chunk = 1024
    min_length = max(10, num_lines * 8)
    max_length = num_lines * 30

    if len(text.split()) <= max_chunk:
        result = pipe(text, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]['summary_text']

    words = text.split()
    chunks = [' '.join(words[i:i + max_chunk]) for i in range(0, len(words), max_chunk)]
    summaries = []
    for chunk in chunks:
        result = pipe(chunk, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(result[0]['summary_text'])

    combined = ' '.join(summaries)
    if len(combined.split()) > max_chunk * 1.5:
        result = pipe(combined, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]['summary_text']

    return combined
