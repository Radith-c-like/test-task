from models.ner_model import NERModel
from scrapers.web_scraper import WebScraper
from config import Config
import logging

class ProductService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ner_model = NERModel(Config.NER_MODEL_NAME, Config.CHECKPOINT_PATH)
        self.web_scraper = WebScraper(Config.USER_AGENT, Config.REQUEST_TIMEOUT, Config.KEYWORDS)

    def extract_products(self, url: str) -> tuple[list, list]:
        if not self.ner_model.pipeline:
            return ["Error: NER model not loaded"], []

        # Scrape the web page
        scraped_texts = self.web_scraper.scrape_page(url, Config.MIN_TEXT_LEN, Config.MAX_TEXT_LEN)
        if not scraped_texts:
            return ["Error: Failed to scrape page"], []

        # Apply NER to extracted texts
        products = []
        tokenized_data = []
        for text in scraped_texts:
            product_words, token_data = self.ner_model.process_text(text, Config.MIN_SCORE)
            if product_words:
                cleaned_products = [p for p in product_words if p and not any(c in p for c in ['#', '$', '%'])]
                products.extend(cleaned_products)
                if token_data["tokens"]:  # Only add if tokens exist
                    tokenized_data.append(token_data)
        

        tr_products = []
        for p in products:
            ln_l = 0
            ln = 0
            for w in p:
                if w.isalpha():
                    print(w)
                    ln += 1
                    if w.isupper():
                        ln_l += 1
            if ln != 0:
                pr = ln_l / ln
            else:
                pr = 0

            if len(p.split()) > 3 and len(p) < 100 and pr < 0.5:
                tr_products.append(p)
        print(tr_products)
        return tr_products if tr_products else [], tokenized_data