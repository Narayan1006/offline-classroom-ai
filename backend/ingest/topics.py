import nltk
import re
from collections import Counter

# Download once (safe even if repeated)
nltk.download("punkt", quiet=True)

STOPWORDS = set([
    "they", "them", "their", "we", "you", "i", "he", "she", "it",
    "today", "class", "lecture", "example", "examples", "topic",
    "chapter", "lesson", "question", "questions",
    "is", "are", "was", "were", "be", "being", "been",
    "have", "has", "had", "do", "does", "did",
    "things", "stuff", "models", "system", "systems"
])


def extract_topics(transcript_text, top_k=6):
    """
    Extract key lesson topics from transcript text.
    """

    sentences = nltk.sent_tokenize(transcript_text.lower())

    words = []
    for s in sentences:
        tokens = re.findall(r"[a-zA-Z]{4,}", s)
        words.extend([w for w in tokens if w not in STOPWORDS])

    freq = Counter(words)

    common = [
        word for word, _ in freq.most_common(top_k * 2)
        if len(word) > 4 and word not in STOPWORDS
    ][:top_k]

    return [w.capitalize() for w in common]
