from data_loader import get_suspicious_queries
from extract_subqueries import extract_subqueries

if __name__ == "__main__":
    queries = get_suspicious_queries()
    print(f"Total de documentos suspeitos oficiais: {len(queries)}")

    counts = []
    for q in queries:
        with open(q["path"], encoding="utf-8", errors="ignore") as f:
            text = f.read()
        n = len(extract_subqueries(text))
        counts.append(n)

    total = sum(counts)
    print(f"Total de subconsultas somando os 64 documentos: {total}")
    print(f"Média por documento: {total / len(counts):.1f}")
    print(f"Mínimo: {min(counts)} | Máximo: {max(counts)}")

    # Estimativa de tempo com a otimização (84.3ms/query, medido antes)
    ms_per_query = 84.3
    horas_uma_combinacao = (total * ms_per_query / 1000) / 3600
    print(f"\nEstimativa (com otimização top-15 termos, {ms_per_query}ms/query):")
    print(f"  1 combinação: {horas_uma_combinacao:.2f}h")
    print(f"  2 combinações (7 + 8): {horas_uma_combinacao * 2:.2f}h")