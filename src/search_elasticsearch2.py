import json
import time
from collections import defaultdict
from elasticsearch import Elasticsearch
from config import REPORTS_DIR
from data_loader import get_suspicious_queries
from extract_subqueries_expanded import extract_subqueries_expanded
from index_elasticsearch import ES_URL, INDEX_NAME
from search_elasticsearch import search_subquery

TOP_K_RESULTS = 10 
OUTPUT_PATH = REPORTS_DIR / "es_combo8_results.json"


def search_suspicious_document(es, text: str) -> list[tuple[str, float]]:
  
    subqueries = extract_subqueries_expanded(text)
    aggregated = defaultdict(float)

    for tokens in subqueries:
        for doc_id, score in search_subquery(es, tokens, limit=TOP_K_RESULTS):
            aggregated[doc_id] += score

    ranked = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
    return ranked[:TOP_K_RESULTS]


if __name__ == "__main__":
    es = Elasticsearch(ES_URL)
    queries = get_suspicious_queries()

    print(f"Buscando {len(queries)} documentos suspeitos (Elasticsearch, combinação 8)...")
    results = {}

    start = time.perf_counter()
    for i, q in enumerate(queries, start=1):
        with open(q["path"], encoding="utf-8", errors="ignore") as f:
            text = f.read()

        doc_start = time.perf_counter()
        ranking = search_suspicious_document(es, text)
        doc_elapsed = time.perf_counter() - doc_start

        results[q["filename"]] = ranking
        elapsed_total = time.perf_counter() - start
        print(f"  [{i}/{len(queries)}] {q['filename']}: "
              f"{doc_elapsed:.1f}s (total até agora: {elapsed_total / 60:.1f}min)")

    total_elapsed = time.perf_counter() - start

    REPORTS_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nConcluído em {total_elapsed / 60:.1f} minutos")
    print(f"Resultados salvos em: {OUTPUT_PATH}")