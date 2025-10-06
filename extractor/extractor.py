# extractor.py
from ner_service import NERService
from scraper import FurnitureScraper, clean_text
from config import Config

class FurnitureExtractor:
    def __init__(self):
        self.scraper = FurnitureScraper()
        self.ner_service = NERService()

    def extract_products(self, url):
        if not self.ner_service.ner_pipeline:
            return ["Error: NER model not loaded"], []

        soup = self.scraper.fetch_page(url)
        texts = self.scraper.extract_texts(soup)
        products = []
        tokenized_data = []

        for text in texts:
            try:
                words = text.split()
                word_labels = ["O"] * len(words)
                has_product = False

                entities = self.ner_service.extract_entities(text)
                for ent in entities:
                    if ent['entity_group'] == "PRODUCT" and ent['score'] >= Config.MIN_SCORE:
                        cleaned_product = clean_text(ent['word'])
                        if cleaned_product and cleaned_product not in products:
                            products.append(cleaned_product)
                            has_product = True
                            product_words = ent['word'].split()
                            for i in range(len(words) - len(product_words) + 1):
                                if ' '.join(words[i:i+len(product_words)]) == ent['word']:
                                    for j in range(i, i + len(product_words)):
                                        word_labels[j] = "PRODUCT"

                if has_product:
                    tokenized_data.append({"tokens": words, "labels": word_labels})

            except Exception as e:
                print(f"[WARNING] NER processing failed for text '{text}': {e}")
                continue

        products = [p for p in products if p and not any(c in p for c in ['#', '$', '%'])]
        return products if products else [], tokenized_data
