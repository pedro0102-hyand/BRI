import json
import time
from collections import defaultdict
from whoosh import index, qparser, scoring
from config import REPORTS_DIR
from data_loader import get_suspicious_queries
from extract_subqueries import extract_subqueries
from index_woosh import INDEX_DIR
from query_term_selection import select_top_terms

K_TERMS = 15
TOP_K_RESULTS = 10
OUTPUT_PATH = REPORTS_DIR / "whoosh_combo7_results.json"


def search_suspicious_document(searcher, parser, text: str) -> list[tuple[str, float]]:

    subqueries = extract_subqueries(text)
    aggregated = defaultdict(float)

    for tokens in subqueries:
        top_terms = select_top_terms(tokens, searcher, k=K_TERMS)
        if not top_terms:
            continue
        query = parser.parse(" ".join(top_terms))
        for r in searcher.search(query, limit=TOP_K_RESULTS):
            aggregated[r["doc_id"]] += r.score

    ranked = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
    return ranked[:TOP_K_RESULTS]


if __name__ == "__main__":
    ix = index.open_dir(str(INDEX_DIR))
    parser = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
    queries = get_suspicious_queries()

    print(f"Buscando {len(queries)} documentos suspeitos (combinação 7)...")
    results = {}

    start = time.perf_counter()
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        for i, q in enumerate(queries, start=1):
            with open(q["path"], encoding="utf-8", errors="ignore") as f:
                text = f.read()

            doc_start = time.perf_counter()
            ranking = search_suspicious_document(searcher, parser, text)
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