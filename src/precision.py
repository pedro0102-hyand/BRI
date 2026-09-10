import json
from config import REPORTS_DIR
from data_loader import get_suspicious_queries


def precision_at_k(ranked_doc_ids: list[str], relevant: set[str], k: int) -> float:

    top_k = ranked_doc_ids[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for doc_id in top_k if doc_id in relevant)
    return hits / k


def average_precision_at_k(results: dict, gabarito: dict, k: int) -> float:
   
    scores = []
    for filename, ranking in results.items():
        ranked_doc_ids = [doc_id for doc_id, _ in ranking]
        relevant = set(gabarito[filename])
        scores.append(precision_at_k(ranked_doc_ids, relevant, k))
    return sum(scores) / len(scores)


if __name__ == "__main__":
    # Carrega o gabarito (src_file de cada documento suspeito)
    queries = get_suspicious_queries()
    gabarito = {q["filename"]: q["src_file"] for q in queries}

    # Testa com os resultados já salvos da combinação 7 (Whoosh)
    with open(REPORTS_DIR / "whoosh_combo7_results.json", encoding="utf-8") as f:
        results = json.load(f)

    print("Precision@k - Whoosh, combinação 7 (média sobre as 64 consultas):")
    for k in [2, 4, 6, 8, 10]:
        p = average_precision_at_k(results, gabarito, k)
        print(f"  p@{k}: {p:.4f}")