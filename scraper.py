# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import re
from config import Config

CLEAN_RE = re.compile(r'\s+')

def clean_text(text):
    if not text:
        return None
    cleaned = CLEAN_RE.sub(' ', text.strip())
    if Config.MIN_TEXT_LEN < len(cleaned) < Config.MAX_TEXT_LEN:
        return cleaned
    return None

class FurnitureScraper:
    def __init__(self):
        self.keywords = ["product", "title", "name", "heading", "card", "grid"]

    def fetch_page(self, url):
        try:
            resp = requests.get(url, headers={"User-Agent": Config.USER_AGENT}, timeout=10)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            print(f"[ERROR] Failed to load page: {e}")
            return None

    def extract_texts(self, soup):
        results = set()
        if not soup:
            return results

        for el in soup.find_all(True):
            if el.name in ("script", "style"):
                continue
            cls = el.get("class")
            eid = el.get("id")
            joined = ""
            if cls:
                joined += " " + " ".join(cls).lower()
            if eid:
                joined += " " + str(eid).lower()
            for kw in self.keywords:
                if kw in joined:
                    text = el.get_text(strip=True)
                    cleaned_text = clean_text(text)
                    if cleaned_text:
                        results.add(cleaned_text)
                    break

        # Title and meta
        if soup.title and soup.title.string:
            cleaned_title = clean_text(soup.title.string)
            if cleaned_title:
                results.add(cleaned_title)

        for meta_attr in [("property", "og:title"), ("name", "twitter:title")]:
            meta = soup.find("meta", attrs={meta_attr[0]: meta_attr[1]})
            if meta and meta.get("content"):
                cleaned_meta = clean_text(meta["content"])
                if cleaned_meta:
                    results.add(cleaned_meta)

        # JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "{}")
                self._walk_json(data, results)
            except Exception as e:
                print(f"[WARNING] Failed to parse JSON-LD: {e}")

        return results

    def _walk_json(self, obj, results):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.lower() in ("name", "title") and isinstance(v, str):
                    cleaned = clean_text(v)
                    if cleaned:
                        results.add(cleaned)
                else:
                    self._walk_json(v, results)
        elif isinstance(obj, list):
            for i in obj:
                self._walk_json(i, results)
