from sklearn.metrics.pairwise import cosine_similarity
from config import model, ANCHOR_EMBEDDINGS, SIMILARITY_THRESHOLD
from .fetcher import fetch_page
from .parser import parse_candidates

def extract_products(url, verbose=False):
    soup, error = fetch_page(url)
    
    if error:
        return [error]

    candidates = parse_candidates(soup, verbose=verbose)

    if not candidates:
        return ["Error: No valid product information found on the page"]

    cand_emb = model.encode(candidates, convert_to_tensor=True, show_progress_bar=False)
    if cand_emb.is_cuda:
        cand_emb = cand_emb.cpu()
    cand_emb = cand_emb.numpy()

    sim_matrix = cosine_similarity(cand_emb, ANCHOR_EMBEDDINGS)
    max_similarities = sim_matrix.max(axis=1)

    products = [(candidates[i], sim) for i, sim in enumerate(max_similarities) if sim > SIMILARITY_THRESHOLD]
    products.sort(key=lambda x: x[1], reverse=True)

    return [p[0] for p in products]
