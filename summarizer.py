import re
from collections import Counter

def summarize_text(text, max_sentences=2):
    if not text:
        return "Summary not available."

    text = re.sub(r'\s+', ' ', text)
    sentences = text.split(". ")

    if len(sentences) <= max_sentences:
        return text

    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)

    sentence_scores = {}
    for sentence in sentences:
        for word in re.findall(r'\w+', sentence.lower()):
            sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_freq[word]

    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
    return ". ".join(top_sentences) + "."
