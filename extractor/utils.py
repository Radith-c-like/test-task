# extractor/utils.py
import re

def is_valid_url(url: str) -> bool:
    """Проверяет, что URL непустой и корректный (http/https)."""
    if not url or not isinstance(url, str):
        return False
    return bool(re.match(r"^https?://", url.strip()))
