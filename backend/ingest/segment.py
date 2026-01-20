import nltk
from collections import Counter
import re

nltk.download("punkt")

STOPWORDS = set([
    # pronouns
    "they", "them", "their", "we", "you", "i", "he", "she", "it",

    # filler words
    "today", "class", "lecture", "example", "examples", "topic",
    "chapter", "lesson", "question", "questions",

    # generic verbs
    "is", "are", "was", "were", "be", "being", "been",
    "have", "has", "had", "do", "does", "did",

    # generic nouns
    "things", "stuff", "models", "system", "systems"
])


def extract_topics(transcript_text, top_k=6):
    sentences = nltk.sent_tokenize(transcript_text.lower())

    words = []
    for s in sentences:
        tokens = re.findall(r"[a-zA-Z]{4,}", s)
        words.extend([w for w in tokens if w not in STOPWORDS])

    freq = Counter(words)
    common = [
    (word, count)
    for word, count in freq.most_common(top_k * 2)
    if len(word) > 4 and word not in STOPWORDS
    ][:top_k]


    topics = [word.capitalize() for word, _ in common]
    return topics
