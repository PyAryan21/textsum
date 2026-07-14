import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

STOPWORDS = set(stopwords.words('english'))


def _clean_word(w: str) -> str:
    return w.lower().strip('.,!?;:()[]"\'')


def _sentence_scores(sentences: list[str]) -> list[tuple[str, float]]:
    word_freq: Counter = Counter()
    for sent in sentences:
        words = [_clean_word(w) for w in word_tokenize(sent) if _clean_word(w) and _clean_word(w) not in STOPWORDS]
        word_freq.update(w for w in words if w)

    max_freq = max(word_freq.values()) if word_freq else 1
    n_sents = len(sentences)
    scored = []
    for i, sent in enumerate(sentences):
        words = [_clean_word(w) for w in word_tokenize(sent) if _clean_word(w) and _clean_word(w) not in STOPWORDS]
        if not words:
            scored.append((sent, 0.0))
            continue
        tfidf_score = sum(word_freq[w] / max_freq for w in set(words)) / len(words)
        position_bonus = 1.0 + 0.3 * (1.0 - i / n_sents)
        scored.append((sent, tfidf_score * position_bonus))
    return scored


def _cosine_sim(a: Counter, b: Counter) -> float:
    intersection = set(a) & set(b)
    num = sum(a[w] * b[w] for w in intersection)
    den = math.sqrt(sum(v ** 2 for v in a.values())) * math.sqrt(sum(v ** 2 for v in b.values()))
    return num / den if den else 0.0


def summarize(text: str, num_lines: int = 5) -> str:
    sentences = sent_tokenize(text)
    if len(sentences) <= num_lines:
        return text

    scored = _sentence_scores(sentences)
    ranked = sorted(scored, key=lambda x: -x[1])

    selected_indices: list[int] = []
    selected_vecs: list[Counter] = []
    for sent, _ in ranked:
        idx = sentences.index(sent)
        words = [_clean_word(w) for w in word_tokenize(sent) if _clean_word(w) and _clean_word(w) not in STOPWORDS]
        vec = Counter(words)
        if any(_cosine_sim(vec, sv) > 0.7 for sv in selected_vecs):
            continue
        selected_indices.append(idx)
        selected_vecs.append(vec)
        if len(selected_indices) >= num_lines:
            break

    selected_indices.sort()
    return '\n'.join(sentences[i] for i in selected_indices)
