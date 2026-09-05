import time
from collections import defaultdict
from whoosh import index, qparser, scoring
from config import SUSPICIOUS_DIR
from data_loader import build_filename_index, load_papers
from index_woosh import INDEX_DIR
from extract_subqueries import extract_subqueries

# Função para buscar uma subconsulta no índice e retornar os resultados
def search_subquery(searcher, parser, tokens: list[str], limit: int = 10):

    if not tokens:
        return []
    
    query = parser.parse(" ".join(tokens))
    results = searcher.search(query, limit=limit)
    return [(r["doc_id"], r.score) for r in results]

# Função para buscar um documento suspeito no índice, agregando os scores das subconsultas
def search_suspicious_document(ix, text: str, top_k: int = 10):

    subqueries = extract_subqueries(text)
    parser = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
    aggregated = defaultdict(float)

    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        for tokens in subqueries:
            for doc_id, score in search_subquery(searcher, parser, tokens):
                aggregated[doc_id] += score

    ranked = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


if __name__ == "__main__":

    ix = index.open_dir(str(INDEX_DIR))
    suspicious_index = build_filename_index(SUSPICIOUS_DIR)
    sample_name, sample_path = next(iter(suspicious_index.items()))

    with open(sample_path, encoding="utf-8", errors="ignore") as f:
        text = f.read()

    print(f"Documento de teste: {sample_name}")
    start = time.perf_counter()
    ranking = search_suspicious_document(ix, text, top_k=10)
    elapsed = time.perf_counter() - start

    print(f"Busca concluída em {elapsed:.1f}s")
    print("\nTop 10 documentos-fonte recuperados (doc_id, score agregado):")
    for doc_id, score in ranking:
        print(f"  {doc_id}: {score:.2f}")

    papers = load_papers()
    entry = next(p for p in papers if p["filename"] == sample_name)
    true_sources = set(entry["src_file"])
    retrieved = {doc_id for doc_id, _ in ranking}
    hits = true_sources & retrieved
    print(f"\nFontes verdadeiras (gabarito): {len(true_sources)}")
    print(f"Acertos no top 10: {len(hits)} -> {hits}")