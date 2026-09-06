import json
import time
from collections import defaultdict
from whoosh import index, qparser, scoring
from config import REPORTS_DIR
from data_loader import get_suspicious_queries
from extract_subqueries_expanded import extract_subqueries_expanded
from index_whoosh import INDEX_DIR
from query_term_selection import select_top_terms

K_TERMS = 15 # Número de termos selecionados por subconsulta
TOP_K_RESULTS = 10 # Número de resultados retornados por documento suspeito
OUTPUT_PATH = REPORTS_DIR / "whoosh_combo8_results.json"

# Função para buscar documentos suspeitos no índice
def search_suspicious_document(searcher, parser, text: str) -> list[tuple[str, float]]:

    # Extração de subconsultas com expansao de termos
    subqueries = extract_subqueries_expanded(text)
    aggregated = defaultdict(float)

    # Para cada subconsulta, seleciona os top K termos e realiza a busca no índice
    for tokens in subqueries:

        top_terms = select_top_terms(tokens, searcher, k=K_TERMS)
        if not top_terms:
            continue
        query = parser.parse(" ".join(top_terms))
        for r in searcher.search(query, limit=TOP_K_RESULTS):
            aggregated[r["doc_id"]] += r.score

    # Ordena os resultados agregados por score decrescente 
    ranked = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
    return ranked[:TOP_K_RESULTS]


if __name__ == "__main__":
    
    ix = index.open_dir(str(INDEX_DIR))
    parser = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
    queries = get_suspicious_queries()

    print(f"Buscando {len(queries)} documentos suspeitos (combinação 8, com expansão)...")
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