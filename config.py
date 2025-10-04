from sentence_transformers import SentenceTransformer

# Модель эмбеддингов
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Якоря
ANCHORS = [
    "sofa", "couch", "loveseat", "sectional", "chaise",
    "chair", "armchair", "recliner", "stool", "ottoman",
    "table", "dining table", "coffee table", "side table", "console table",
    "bed", "bed frame", "bunk bed", "platform bed", "storage bed", "headboard",
    "mattress", "euro top mattress", "foam mattress",
    "wardrobe", "closet", "dresser", "chest of drawers", "nightstand",
    "desk", "writing desk", "office desk",
    "bookshelf", "bookcase", "shelf", "cabinet", "sideboard", "buffet",
    "bench", "bar stool", "dining chair",
    "light", "lamp", "reading light", "wall light", "table lamp", "floor lamp",
    "pendant light", "chandelier", "ceiling light", "led light", "bedhead light",
    "sheet", "sheet set", "bedding", "duvet", "comforter", "quilt",
    "pillow", "cushion", "throw pillow",
    "curtain", "drape", "blind", "shade",
    "rug", "carpet", "mat",
    "blanket", "throw", "bedspread",
    "storage", "storage box", "basket", "bin", "organizer",
    "shelving", "rack", "storage unit",
    "mirror", "wall mirror", "floor mirror",
    "painting", "art print", "wall art",
    "vase", "planter", "pot",
    "candle holder", "candle", "lantern",
    "mattress protector", "bed skirt", "bed base",
    "kitchen island", "bar cart",
    "towel", "bath mat", "shower curtain", "gift", "card"
]
ANCHOR_EMBEDDINGS = model.encode(ANCHORS)

# Шумовые слова
NOISE_WORDS = {
    "home", "packages", "package", "frames", "bedroom", "catalog", "category",
    "menu", "shop", "store", "description", "care", "instructions", "warranty",
    "shipping", "contact", "about", "policy", "terms", "conditions", "cart",
    "checkout", "login", "account", "trustpilot", "notify", "quantity",
    "product features", "dimensions", "specs", "included", "frequently", "variants",
    "also pay", "free shipping", "sold out", "decrease", "increase", "tax included",
    "you might", "skip", "learn more", "add to cart", "wishlist", "compare",
    "mattresses", "beds", "sofas", "chairs", "tables", "lamps", "lights", "sheets",
    "pillows", "curtains", "rugs", "mirrors", "shelves", "cabinets", "desks", "wardrobes"
}

# Настройки фильтрации
MIN_TEXT_LEN = 15
MAX_TEXT_LEN = 150
MIN_WORD_COUNT = 3
SIMILARITY_THRESHOLD = 0.35
