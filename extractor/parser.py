import json
import re
from .cleaner import clean_text, is_noise_text

def parse_candidates(soup, verbose=False):
    candidates = set()

    # Удаляем шумные блоки
    for tag in soup.select('.megamenu, .nav, .navbar, .menu, .footer, .header'):
        tag.decompose()

    # h1-h6
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        text = clean_text(tag.get_text())
        if text and not is_noise_text(text):
            candidates.add(text)

    # div/span с классами product/item
    for tag in soup.find_all(["div", "span"], class_=[re.compile(r'(product|item|title|name|card|product-card|item-card|product-link)', re.I)]):
        text = clean_text(tag.get_text())
        if text and not is_noise_text(text):
            candidates.add(text)

    # JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for el in data:
                    if isinstance(el, dict) and el.get("@type") in {"Product", "ProductModel", "Offer"} and "name" in el:
                        text = clean_text(el["name"])
                        if text and not is_noise_text(text):
                            candidates.add(text)
            elif isinstance(data, dict):
                if data.get("@type") in {"Product", "ProductModel", "Offer"} and "name" in data:
                    text = clean_text(data["name"])
                    if text and not is_noise_text(text):
                        candidates.add(text)
        except Exception:
            continue

    return list(candidates)
