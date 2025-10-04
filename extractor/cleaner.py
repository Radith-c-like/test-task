import re
from config import NOISE_WORDS, ANCHORS

CLEAN_RE = re.compile(r'\s+')

def clean_text(text, min_len=15, max_len=150, min_words=3):
    if not text:
        return None
    cleaned = CLEAN_RE.sub(' ', text.strip())
    words = cleaned.split()
    if min_len <= len(cleaned) <= max_len and len(words) >= min_words:
        return cleaned
    return None

def is_noise_text(text):
    words = text.lower().split()
    if any(word in NOISE_WORDS for word in words):
        return True
    if 1 <= len(words) <= 3:
        anchor_words = set(word[:-1] if word.endswith('s') else word for word in words if word in ANCHORS or word[:-1] in ANCHORS)
        if len(anchor_words) == len(words):
            return True
    return False
