import requests
from bs4 import BeautifulSoup
import json
import logging
from utils.text_utils import TextCleaner

class WebScraper:
    def __init__(self, user_agent: str, timeout: int, keywords: list[str]):
        self.user_agent = user_agent
        self.timeout = timeout
        self.keywords = keywords
        self.logger = logging.getLogger(__name__)

    def scrape_page(self, url: str, min_len: int, max_len: int) -> set[str]:
        results = set()
        try:
            resp = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Extract from elements with relevant classes/ids
            for el in soup.find_all(True):
                if el.name in ("script", "style"):
                    continue
                cls = el.get("class") or []
                eid = el.get("id") or ""
                joined = " ".join(cls).lower() + " " + str(eid).lower()
                
                if any(kw in joined for kw in self.keywords):
                    text = el.get_text(strip=True)
                    cleaned = TextCleaner.clean_text(text, min_len, max_len)
                    if cleaned:
                        results.add(cleaned)

            # Extract from title
            if soup.title and soup.title.string:
                cleaned_title = TextCleaner.clean_text(soup.title.string, min_len, max_len)
                if cleaned_title:
                    results.add(cleaned_title)

            # Extract from meta tags
            for meta_attr in [("property", "og:title"), ("name", "twitter:title")]:
                meta = soup.find("meta", attrs={meta_attr[0]: meta_attr[1]})
                if meta and meta.get("content"):
                    cleaned_meta = TextCleaner.clean_text(meta.get("content"), min_len, max_len)
                    if cleaned_meta:
                        results.add(cleaned_meta)

            # Extract from JSON-LD
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "{}")
                    self._walk_json_ld(data, results, min_len, max_len)
                except Exception as e:
                    self.logger.warning(f"Failed to parse JSON-LD: {e}")

            # Extract related products from Shopify API
            try:
                domain = url.split('/')[2]
                handle = url.split("/products/")[-1].split("?")[0]
                product_api_url = f"https://{domain}/products/{handle}.js"
                product_resp = requests.get(product_api_url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
                if product_resp.status_code == 200:
                    product_data = product_resp.json()
                    product_id = product_data.get("id")
                    rec_url = f"https://{domain}/recommendations/products.json?product_id={product_id}&limit=10"
                    rec_resp = requests.get(rec_url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
                    if rec_resp.status_code == 200:
                        rec_data = rec_resp.json()
                        for p in rec_data.get("products", []):
                            title = p.get("title")
                            cleaned_title = TextCleaner.clean_text(title, min_len, max_len)
                            if cleaned_title:
                                results.add(cleaned_title)
            except Exception as e:
                self.logger.warning(f"Failed to get related products: {e}")

        except Exception as e:
            self.logger.error(f"Failed to load page: {e}")
            return set()

        return results

    def _walk_json_ld(self, obj, results: set, min_len: int, max_len: int):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k.lower() in ("name", "title") and isinstance(v, str):
                    cleaned = TextCleaner.clean_text(v, min_len, max_len)
                    if cleaned:
                        results.add(cleaned)
                else:
                    self._walk_json_ld(v, results, min_len, max_len)
        elif isinstance(obj, list):
            for i in obj:
                self._walk_json_ld(i, results, min_len, max_len)