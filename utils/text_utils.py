import re

class TextCleaner:
    CLEAN_RE = re.compile(r'\s+')

    @staticmethod
    def clean_text(text: str, min_len: int, max_len: int) -> str | None:
        if not text:
            return None
        cleaned = TextCleaner.CLEAN_RE.sub(' ', text.strip())
        return cleaned if min_len < len(cleaned) < max_len else None