# TextSum

A CLI text summarization tool with **extractive** (TextRank) and **abstractive** (HuggingFace) modes.  
Accepts files, URLs, PDFs, and stdin — outputs plain text, JSON, Markdown, or HTML.

## Features

- **TextRank extractive** — graph-based sentence ranking with redundancy filtering and confidence scores
- **Abstractive mode** — generates novel summaries using HuggingFace models (BART, DistilBART, T5)
- **Multiple input sources** — local files, URLs, PDFs, stdin
- **Interactive mode** — browse ranked sentences and hand-pick your summary
- **Batch mode** — summarize multiple inputs in one command
- **Export formats** — text, JSON, Markdown, HTML
- **Language detection** — auto-detects text language (requires `langdetect`)
- **URL caching** — cached fetches avoid redundant downloads
- **Config file** — persistent defaults via `~/.config/textsumrc`
- **Custom prompts** — guide abstractive summaries with your own instructions
- **Progress bars** — visible feedback during long abstractive runs
- **Verbose mode** — timing, token counts, model info
- **PyPI installable** — `pip install textsum`

## Installation

```bash
pip install -r requirements.txt

# Optional: language detection
pip install langdetect
```

## Usage

```
textsum [OPTIONS] INPUTS...

Arguments:
  INPUTS               One or more files, URLs, or "-" for stdin

Options:
  -m, --mode TEXT       extractive | abstractive  [default: extractive]
  -l, --lines INT       Number of sentences       [default: 5]
  -o, --output PATH     Write to file
  -f, --format TEXT     text | json | markdown | html  [default: text]
  -i, --interactive     Interactive sentence selection
  -c, --config PATH     Config file path
  -v, --verbose         Verbose output
  --model TEXT           HuggingFace model for abstractive mode
  --prompt TEXT          Custom prompt for abstractive mode
  --help                 Show help
```

### Examples

```bash
# Extractive summary of a file
textsum article.txt

# Abstractive summary of a URL with custom prompt
textsum "https://example.com/article" --mode abstractive --prompt "Summarize in 3 bullet points"

# Batch mode: summarize multiple files
textsum report1.pdf report2.pdf report3.txt --lines 3

# Interactive mode: pick which sentences to include
textsum article.txt --interactive

# Export as Markdown
textsum article.txt --format markdown -o summary.md

# Use a lighter model for abstractive
textsum article.txt --mode abstractive --model t5-small

# Verbose with timing info
textsum article.txt -v

# Pipe from stdin
cat notes.txt | textsum -

# Use config file for defaults
textsum article.txt -c ~/.config/textsumrc
```

## Configuration

Create `~/.config/textsumrc` (JSON):

```json
{
  "mode": "extractive",
  "lines": 5,
  "model": "facebook/bart-large-cnn",
  "format": "text",
  "verbose": false
}
```

## How It Works

### Extractive (TextRank)
1. Builds a similarity graph between sentences (cosine similarity of word vectors)
2. Runs PageRank on the graph to rank sentence importance
3. Selects top N sentences while filtering near-duplicates (>0.7 cosine similarity)
4. Returns sentences ordered as they appear in the original text

### Abstractive
1. Loads a HuggingFace seq2seq model (BART, T5, or DistilBART)
2. Chunks text exceeding the model's token limit (1024 tokens)
3. Summarizes each chunk with progress bar, re-summarizes if combined output is still long

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependencies

## Docker

```bash
docker build -t textsum .
docker run --rm textsum article.txt -l 3
```

## License

MIT
