# TextSum

A powerful CLI text summarization tool with **extractive** (TextRank) and **abstractive** (HuggingFace) modes.  
Accepts files, URLs, PDFs, and stdin — outputs plain text, JSON, Markdown, or HTML.

## Features

### Summarization
- **TextRank extractive** — graph-based sentence ranking using PageRank, with cosine similarity redundancy filtering, position bias, and confidence scores per sentence
- **Abstractive generation** — generates novel summary text using HuggingFace seq2seq models (BART, DistilBART, T5) with automatic chunking for long documents

### Input & Output
- **Multi-source input** — local files, URLs, PDF documents, and stdin piping
- **Batch processing** — summarize multiple inputs in a single command
- **Export formats** — plain text with confidence bars, structured JSON, Markdown, and styled HTML
- **Interactive mode** — browse ranked sentences, toggle them with number/range input, and hand-pick your final summary

### Intelligence
- **Language detection** — auto-detects input language (via `langdetect`) for better processing
- **Custom prompts** — guide abstractive summaries with your own instructions (e.g. "Summarize in 3 bullet points")
- **Multiple models** — plug in different HuggingFace models: BART (default), T5-small (fast), DistilBART (lightweight)

### Developer Experience
- **URL caching** — fetched content cached locally for 24 hours (SHA256-keyed, `~/.cache/textsum/`)
- **Progress bars** — visible feedback via `tqdm` during long abstractive runs
- **Config file** — persistent defaults via `~/.config/textsumrc` (JSON format)
- **Verbose mode** — timing, character counts, language detection, token estimates, model info
- **PyPI installable** — `pip install textsum` with console entry point
- **Docker support** — ready-to-use container image
- **Pre-commit hook** — integrate into your Git workflow

## Installation

### From PyPI

```bash
pip install textsum

# Optional: PDF and language detection support
pip install textsum[all]

# Or install extras individually
pip install textsum[pdf]
pip install textsum[langdetect]
```

### From source

```bash
git clone https://github.com/PyAryan21/textsum.git
cd textsum
pip install -r requirements.txt
pip install -e .
```

### Docker

```bash
docker build -t textsum .
docker run --rm textsum article.txt -l 3
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
# Basic extractive summary
textsum article.txt

# Abstractive summary with custom prompt
textsum "https://example.com/article" --mode abstractive --prompt "Summarize in 3 bullet points"

# Use a lighter model for faster results
textsum long_report.txt --mode abstractive --model t5-small

# Batch mode: summarize multiple files at once
textsum report1.pdf report2.pdf notes.txt --lines 3

# Interactive mode: browse and pick sentences manually
textsum article.txt --interactive

# Export as Markdown
textsum article.txt --format markdown -o summary.md

# Export as HTML with confidence bars
textsum article.txt --format html -o summary.html

# Verbose mode with timing and language info
textsum article.txt -v

# Pipe from stdin
cat notes.txt | textsum -

# JSON output for scripting
textsum article.txt --format json

# Use a config file for persistent defaults
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

1. Tokenizes text into sentences and builds a word-frequency vector for each
2. Constructs a similarity graph where edges represent cosine similarity between sentence vectors
3. Runs PageRank on the graph to compute each sentence's importance score
4. Filters out near-duplicate sentences (cosine similarity > 0.7)
5. Returns the top N sentences in their original order with normalized confidence scores

### Abstractive

1. Loads a HuggingFace seq2seq model (default: `facebook/bart-large-cnn`)
2. Splits long text into chunks (1024-token limit) with `tqdm` progress bar
3. Summarizes each chunk independently
4. Re-summarizes the combined output if it still exceeds the token limit
5. Supports custom prompts by prepending them to the input text

## Output Formats

### Text (default)
```
[100%] #################### Main sentence with highest confidence
[ 53%] ########### Secondary sentence with medium confidence
[ 10%] ## Lower-confidence sentence
```

### JSON
```json
{
  "summary": "Full summary text...",
  "sentences": [
    {"text": "...", "confidence": 1.0},
    {"text": "...", "confidence": 0.5278}
  ]
}
```

### Markdown
```markdown
## Summary

- Main sentence *(confidence: 100%)*
- Secondary sentence *(confidence: 53%)*
```

### HTML
Styled HTML page with horizontal confidence bars beside each sentence.

## Roadmap

- [ ] **Additional abstractive backends** — OpenAI, Anthropic, local Ollama API support
- [ ] **Multi-language stopwords** — auto-select NLTK stopwords based on detected language (extractive)
- [ ] **TL;DR mode** — single-sentence extreme summarization
- [ ] **Comparison mode** — diff-style comparison between extractive and abstractive summaries
- [ ] **Streaming input** — real-time summarization of live text streams
- [ ] **Web UI** — minimal web interface (FastAPI + htmx)
- [ ] **Plugins** — custom summarization algorithms via entry points
- [ ] **CI/CD** — automated testing, PyPI publishing via GitHub Actions

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
