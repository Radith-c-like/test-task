import os
import re

class Config:
    CHECKPOINT_PATH = os.path.expandvars("/home/chr43/Projects/MyModel/furniture_ner_trainer/checkpoint-70")
    NER_MODEL_NAME = "dslim/bert-base-NER"
    MIN_TEXT_LEN = 2
    MAX_TEXT_LEN = 150
    MIN_SCORE = 0.7
    KEYWORDS = ["product", "title", "name", "heading", "card", "grid"]
    REQUEST_TIMEOUT = 10
    USER_AGENT = "Mozilla/5.0"
    CLEAN_RE = re.compile(r'\s+')