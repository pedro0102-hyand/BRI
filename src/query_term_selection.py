"""Otimização de busca: reduz cada subconsulta aos N termos mais raros
(maior IDF / menor frequência de documento) antes de montar a query.

Justificativa: termos comuns (mesmo sem serem stopwords) contribuem pouco
para o ranking BM25 mas custam caro para o Whoosh combinar via OR. Manter
só os termos mais discriminativos reduz o custo de busca e concentra a
consulta no que de fato ajuda a diferenciar documentos - o mesmo princípio
discutido na análise de Zipf da Parte 1.
"""
import time
from whoosh import index, qparser, scoring
from index_woosh import INDEX_DIR
from extract_subqueries import extract_subqueries
from data_loader import get_suspicious_queries

def select_top_terms(tokens: list[str], searcher, field: str = "content", k: int = 15) -> list[str]:
    """Seleciona os k termos com menor frequência de documento (mais raros)
    entre os tokens de uma subconsulta, usando as estatísticas já
    calculadas pelo próprio índice.
    """
    reader = searcher.reader()
    unique_tokens = set(tokens)

    scored = []
    for t in unique_tokens:
        df = reader.doc_frequency(field, t)
        if df > 0:  # ignora termos que não existem no índice
            scored.append((t, df))

    scored.sort(key=lambda x: x[1])  # menor df primeiro = mais raro
    return [t for t, _ in scored[:k]]


if __name__ == "__main__":
  
    N_SAMPLES = 20
    K_TERMS = 15

    ix = index.open_dir(str(INDEX_DIR))
    queries = get_suspicious_queries()
    sample = queries[0]

    with open(sample["path"], encoding="utf-8", errors="ignore") as f:
        text = f.read()

    subqueries = extract_subqueries(text)[:N_SAMPLES]
    parser = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)

    search_time = 0.0
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        for tokens in subqueries:
            top_terms = select_top_terms(tokens, searcher, k=K_TERMS)
            query = parser.parse(" ".join(top_terms))

            t0 = time.perf_counter()
            results = searcher.search(query, limit=10)
            t1 = time.perf_counter()
            search_time += (t1 - t0)

    print(f"Com top-{K_TERMS} termos por subconsulta (em vez de ~62):")
    print(f"Tempo total de search(): {search_time:.3f}s ({search_time / N_SAMPLES * 1000:.1f}ms/query)")
    print(f"Extrapolando para 64 documentos x 2 combinações: "
          f"{(search_time / N_SAMPLES) * 1684 * 64 * 2 / 3600:.1f}h (estimativa grosseira)")