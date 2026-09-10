import time
from config import REPORTS_DIR
from data_loader import get_suspicious_queries
from preprocess_b import preprocess_b
from extract_subqueries import extract_subqueries
from extract_subqueries_expanded import extract_subqueries_expanded
import json

if __name__ == "__main__":

    queries = get_suspicious_queries()
    n = len(queries)
    print(f"Medindo tempo de processamento em {n} documentos suspeitos oficiais...")

    texts = []

    for q in queries:
        with open(q["path"], encoding="utf-8", errors="ignore") as f:
            texts.append(f.read())

    # Pré-processamento isolado (documento inteiro, sem quebrar em janelas)
    start = time.perf_counter()
    for text in texts:
        preprocess_b(text)
    preprocess_time = time.perf_counter() - start
    preprocess_avg = preprocess_time / n

    # Pipeline completo combinação 7 (janela + pré-processamento, sem expansão)
    start = time.perf_counter()
    for text in texts:
        extract_subqueries(text)
    combo7_time = time.perf_counter() - start
    combo7_avg = combo7_time / n

    #Pipeline completo combinação 8 (janela + pré-processamento + expansão)
    start = time.perf_counter()
    for text in texts:
        extract_subqueries_expanded(text)
    combo8_time = time.perf_counter() - start
    combo8_avg = combo8_time / n

    print(f"\n--- Tempo médio por documento suspeito ---")
    print(f"Pré-processamento (isolado, documento inteiro): {preprocess_avg:.3f}s")
    print(f"Pré-processamento+representação+extração (combinação 7, sem expansão): {combo7_avg:.3f}s")
    print(f"Pré-processamento+representação+extração (combinação 8, com expansão): {combo8_avg:.3f}s")
    print(f"\nCusto adicional só da extração por janelas (combo 7 - pré-proc isolado): "
          f"{combo7_avg - preprocess_avg:.3f}s")
    print(f"Custo adicional só da expansão de sinônimos (combo 8 - combo 7): "
          f"{combo8_avg - combo7_avg:.3f}s")

    output = {
        "n_documentos": n,
        "preprocessamento_isolado_s": round(preprocess_avg, 4),
        "combo7_total_s": round(combo7_avg, 4),
        "combo8_total_s": round(combo8_avg, 4),
        "custo_extracao_janelas_s": round(combo7_avg - preprocess_avg, 4),
        "custo_expansao_sinonimos_s": round(combo8_avg - combo7_avg, 4),
    }
    REPORTS_DIR.mkdir(exist_ok=True)
    with open(REPORTS_DIR / "tempos_busca_preprocessamento.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nResultado salvo em: {REPORTS_DIR / 'tempos_busca_preprocessamento.json'}")