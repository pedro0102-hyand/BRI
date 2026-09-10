import json
from config import REPORTS_DIR
from data_loader import get_suspicious_queries
from precision import precision_at_k  # reaproveitado para comparação


def recall_at_k(ranked_doc_ids: list[str], relevant: set[str], k: int) -> float:
   
    if not relevant:
        return 0.0
    top_k = ranked_doc_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant)
    return hits / len(relevant)


def average_recall_at_k(results: dict, gabarito: dict, k: int) -> float:
    
    scores = []
    for filename, ranking in results.items():
        ranked_doc_ids = [doc_id for doc_id, _ in ranking]
        relevant = set(gabarito[filename])
        scores.append(recall_at_k(ranked_doc_ids, relevant, k))
    return sum(scores) / len(scores)


if __name__ == "__main__":
    
    queries = get_suspicious_queries()
    gabarito = {q["filename"]: q["src_file"] for q in queries}

    with open(REPORTS_DIR / "whoosh_combo7_results.json", encoding="utf-8") as f:
        results = json.load(f)

    avg_gabarito_size = sum(len(v) for v in gabarito.values()) / len(gabarito)
    print(f"Tamanho médio do gabarito (fontes verdadeiras por consulta): {avg_gabarito_size:.1f}\n")

    print("Recall@k - Whoosh, combinação 7 (média sobre as 64 consultas):")
    for k in [2, 4, 6, 8, 10]:
        r = average_recall_at_k(results, gabarito, k)
        print(f"  r@{k}: {r:.4f}")