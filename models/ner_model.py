from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import logging

class NERModel:
    def __init__(self, model_name: str, checkpoint_path: str):
        self.logger = logging.getLogger(__name__)
        self.pipeline = self._load_model(model_name, checkpoint_path)

    def _load_model(self, model_name: str, checkpoint_path: str):
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForTokenClassification.from_pretrained(checkpoint_path)
            return pipeline(
                "ner",
                model=model,
                tokenizer=tokenizer,
                aggregation_strategy="simple"
            )
        except Exception as e:
            self.logger.error(f"Failed to load NER model: {e}")
            return None

    def process_text(self, text: str, min_score: float) -> tuple[list, dict]:
        if not self.pipeline:
            return [], {"tokens": [], "labels": []}
        
        try:
            words = text.split()
            word_labels = ["O"] * len(words)
            entities = self.pipeline(text)
            product_words = []
            
            for ent in entities:
                if ent['entity_group'] == "PRODUCT" and ent['score'] >= min_score:
                    product_words.append(ent['word'])
                    product_span = ent['word'].split()
                    for i in range(len(words) - len(product_span) + 1):
                        if ' '.join(words[i:i+len(product_span)]) == ent['word']:
                            for j in range(i, i + len(product_span)):
                                word_labels[j] = "PRODUCT"
            
            return product_words, {"tokens": words, "labels": word_labels}
        except Exception as e:
            self.logger.warning(f"NER processing failed for text '{text}': {e}")
            return [], {"tokens": [], "labels": []}