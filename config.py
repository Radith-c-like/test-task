import os

class Config:
    CHECKPOINT_PATH = os.path.expandvars("/home/chr43/Projects/MyModel/furniture_ner_trainer/checkpoint-70")
    MIN_TEXT_LEN = 2
    MAX_TEXT_LEN = 150
    USER_AGENT = "Mozilla/5.0"
    NER_MODEL_NAME = "dslim/bert-base-NER"
    MIN_SCORE = 0.7