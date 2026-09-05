import time
from whoosh import index, qparser, scoring
from index_woosh import INDEX_DIR
from extract_subqueries import extract_subqueries
from config import SUSPICIOUS_DIR
from data_loader import get_suspicious_queries
N_SAMPLES = 20


if __name__ == "__main__":
    ix = index.open_dir(str(INDEX_DIR))
    queries = get_suspicious_queries()
    sample = queries[0]

    with open(sample["path"], encoding="utf-8", errors="ignore") as f:
        text = f.read()

    subqueries = extract_subqueries(text)[:N_SAMPLES]
    print(f"Documento de teste: {sample['filename']}")
    print(f"Testando {len(subqueries)} subconsultas (de {len(extract_subqueries(text))} totais)\n")

    parser = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)

    parse_time = 0.0
    search_time = 0.0
    query_sizes = []

    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        for tokens in subqueries:
            query_sizes.append(len(tokens))

            t0 = time.perf_counter()
            query = parser.parse(" ".join(tokens))
            t1 = time.perf_counter()
            results = searcher.search(query, limit=10)
            t2 = time.perf_counter()

            parse_time += (t1 - t0)
            search_time += (t2 - t1)

    print(f"Tamanho médio das subconsultas: {sum(query_sizes) / len(query_sizes):.1f} tokens")
    print(f"\nTempo total de parse():  {parse_time:.3f}s ({parse_time / N_SAMPLES * 1000:.1f}ms/query)")
    print(f"Tempo total de search(): {search_time:.3f}s ({search_time / N_SAMPLES * 1000:.1f}ms/query)")
    print(f"Total: {parse_time + search_time:.3f}s para {N_SAMPLES} subconsultas")
    print(f"\nGargalo: {'parse()' if parse_time > search_time else 'search()'}")