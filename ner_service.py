# ner_service.py
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from config import Config

class NERService:
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(Config.NER_MODEL_NAME)
            self.model = AutoModelForTokenClassification.from_pretrained(Config.CHECKPOINT_PATH)
            self.ner_pipeline = pipeline(
                "ner",
                model=self.model,
                tokenizer=self.tokenizer,
                aggregation_strategy="simple"
            )
        except Exception as e:
            print(f"[ERROR] Failed to load NER model: {e}")
            self.ner_pipeline = None

    def extract_entities(self, text):
        if not self.ner_pipeline:
            return []
        return self.ner_pipeline(text)
