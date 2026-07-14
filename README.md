# TextSum

A CLI text summarization tool with two modes: **extractive** (TF-IDF scoring) and **abstractive** (HuggingFace BART model).

## Features

- **Extractive mode** — scores sentences by word frequency and position, removes redundancy via cosine similarity
- **Abstractive mode** — generates novel summary text using `facebook/bart-large-cnn`
- **Multi-source input** — files, URLs, and stdin piping
- **Configurable summary length**
- **Output to stdout or file**

## Installation

```bash
pip install -r requirements.txt
```

The first run in abstractive mode will download the BART model (~1.6 GB) and cache it locally.

## Usage

```
python textsum.py [OPTIONS] INPUT

Arguments:
  INPUT              File path, URL, or "-" for stdin

Options:
  -m, --mode TEXT    Summarization mode: 'extractive' or 'abstractive'
                     [default: extractive]
  -l, --lines INT    Number of sentences in summary [default: 5]
  -o, --output PATH  Write to file instead of stdout
  --help             Show help
```

### Examples

```bash
# Summarize a file (extractive, 5 sentences)
python textsum.py article.txt

# Summarize a URL with abstractive mode
python textsum.py "https://example.com/long-article" --mode abstractive --lines 3

# Pipe text from stdin
cat notes.txt | python textsum.py -

# Write summary to a file
python textsum.py report.txt -o summary.txt
```

## How It Works

### Extractive
1. Tokenizes text into sentences
2. Scores each sentence by TF-IDF weighted word frequency with a position bias (earlier sentences weighted higher)
3. Selects top N sentences while filtering out near-duplicates via cosine similarity (>0.7 threshold)

### Abstractive
1. Uses HuggingFace's `facebook/bart-large-cnn` model
2. Chunks long text exceeding the model's 1024-token limit
3. Summarizes each chunk, then recursively summarizes the combined result if needed

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies
