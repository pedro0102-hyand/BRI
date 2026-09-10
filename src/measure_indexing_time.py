import time
from config import SOURCE_DIR, REPORTS_DIR
from data_loader import build_filename_index
from preprocess_b import preprocess_b

SAMPLE_SIZE = 500

# Tempos totais já medidos nas indexações completas (rodadas anteriores)
WHOOSH_TOTAL_S_PER_DOC = 1760.8 / 11093
ES_TOTAL_S_PER_DOC = 1404.9 / 11093


if __name__ == "__main__":
    
    source_index = build_filename_index(SOURCE_DIR)
    sample_paths = list(source_index.values())[:SAMPLE_SIZE]

    print(f"Medindo tempo de pré-processamento em {SAMPLE_SIZE} documentos-fonte...")

    start = time.perf_counter()
    for path in sample_paths:
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        preprocess_b(text)
    elapsed = time.perf_counter() - start

    preprocess_s_per_doc = elapsed / SAMPLE_SIZE

    print(f"\nTempo total: {elapsed:.1f}s para {SAMPLE_SIZE} documentos")
    print(f"Tempo médio de pré-processamento (isolado): {preprocess_s_per_doc:.4f}s/doc")

    print("\n--- Comparação (Whoosh vs Elasticsearch) ---")
    print(f"{'Métrica':<55} {'Whoosh':>10} {'Elasticsearch':>15}")
    print(f"{'Pré-processamento (isolado)':<55} {preprocess_s_per_doc:>9.4f}s {preprocess_s_per_doc:>14.4f}s")
    print(f"{'Pré-processamento+representação+indexação (total)':<55} "
          f"{WHOOSH_TOTAL_S_PER_DOC:>9.4f}s {ES_TOTAL_S_PER_DOC:>14.4f}s")
    print(f"{'Só representação+indexação (derivado)':<55} "
          f"{WHOOSH_TOTAL_S_PER_DOC - preprocess_s_per_doc:>9.4f}s "
          f"{ES_TOTAL_S_PER_DOC - preprocess_s_per_doc:>14.4f}s")

    # Salva os números para uso na Parte 4 do relatório
    import json
    output = {
        "amostra_documentos": SAMPLE_SIZE,
        "preprocessamento_isolado_s_por_doc": round(preprocess_s_per_doc, 4),
        "whoosh_total_s_por_doc": round(WHOOSH_TOTAL_S_PER_DOC, 4),
        "elasticsearch_total_s_por_doc": round(ES_TOTAL_S_PER_DOC, 4),
        "whoosh_so_indexacao_s_por_doc": round(WHOOSH_TOTAL_S_PER_DOC - preprocess_s_per_doc, 4),
        "elasticsearch_so_indexacao_s_por_doc": round(ES_TOTAL_S_PER_DOC - preprocess_s_per_doc, 4),
    }
    REPORTS_DIR.mkdir(exist_ok=True)
    with open(REPORTS_DIR / "tempos_indexacao.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nResultado salvo em: {REPORTS_DIR / 'tempos_indexacao.json'}")