import math
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("english"))
DAMPING = 0.85
MAX_ITER = 100
CONVERGENCE = 1e-4


def _clean(w: str) -> str:
    return w.lower().strip(".,!?;:()[]\"'-")


def _sentence_vector(sent: str) -> Counter:
    words = [_clean(w) for w in word_tokenize(sent) if _clean(w) and _clean(w) not in STOPWORDS]
    return Counter(words)


def _cosine_sim(a: Counter, b: Counter) -> float:
    intersection = set(a) & set(b)
    num = sum(a[w] * b[w] for w in intersection)
    den = math.sqrt(sum(v**2 for v in a.values())) * math.sqrt(sum(v**2 for v in b.values()))
    return num / den if den else 0.0


def _textrank(sentences: list[str]) -> list[tuple[str, float]]:
    n = len(sentences)
    if n == 0:
        return []
    if n == 1:
        return [(sentences[0], 1.0)]

    vectors = [_sentence_vector(s) for s in sentences]
    sim_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = _cosine_sim(vectors[i], vectors[j])
            sim_matrix[i][j] = s
            sim_matrix[j][i] = s

    scores = [1.0 / n] * n
    for _ in range(MAX_ITER):
        prev = scores[:]
        for i in range(n):
            total = 0.0
            for j in range(n):
                if i != j:
                    row_sum = sum(sim_matrix[j])
                    total += sim_matrix[j][i] / row_sum * prev[j] if row_sum > 0 else 0
            scores[i] = (1 - DAMPING) + DAMPING * total
        if sum(abs(scores[i] - prev[i]) for i in range(n)) < CONVERGENCE:
            break

    max_score = max(scores) if scores else 1
    return [(sentences[i], scores[i] / max_score) for i in range(n)]


def summarize(text: str, num_lines: int = 5) -> tuple[str, list[tuple[str, float]]]:
    sentences = sent_tokenize(text)
    if len(sentences) <= num_lines:
        return text, [(s, 1.0) for s in sentences]

    scored = _textrank(sentences)
    ranked = sorted(scored, key=lambda x: -x[1])

    selected = []
    selected_vecs = []
    for sent, score in ranked:
        vec = _sentence_vector(sent)
        if any(_cosine_sim(vec, sv) > 0.7 for sv in selected_vecs):
            continue
        selected.append((sent, score))
        selected_vecs.append(vec)
        if len(selected) >= num_lines:
            break

    selected.sort(key=lambda x: sentences.index(x[0]))
    summary = "\n".join(s for s, _ in selected)
    return summary, selected
