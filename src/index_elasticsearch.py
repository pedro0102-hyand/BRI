import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from data_loader import build_filename_index
from config import SOURCE_DIR
from preprocess_b import preprocess_b

# Configurações do Elasticsearch
ES_URL = "http://localhost:9200"
INDEX_NAME = "bri_combo_b"
BATCH_SIZE = 500

# Mapeamento do índice
MAPPING = {
    "settings": {
        "index": {
            "similarity": {
                "default": {"type": "BM25"}
            }
        }
    },
    "mappings": {
        "properties": {
            "doc_id": {"type": "keyword"},
            # analyzer "whitespace": só separa por espaço, sem stemming/
            # stopwords próprios do ES - já fizemos isso manualmente
            "content": {"type": "text", "analyzer": "whitespace"},
        }
    },
}

# Função para gerar ações de indexação em lote
def generate_actions(source_index: dict):
    for filename, path in source_index.items():
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        tokens = preprocess_b(text)
        yield {
            "_index": INDEX_NAME,
            "_id": filename,
            "_source": {"doc_id": filename, "content": " ".join(tokens)},
        }


if __name__ == "__main__":

    es = Elasticsearch(ES_URL)

    # Verifica se o índice já existe e o recria
    if es.indices.exists(index=INDEX_NAME):
        print(f"Índice '{INDEX_NAME}' já existe, apagando para recriar...")
        es.indices.delete(index=INDEX_NAME)

    es.indices.create(index=INDEX_NAME, body=MAPPING)
    print(f"Índice '{INDEX_NAME}' criado.")

    # Indexa os documentos-fonte usando a API Bulk
    source_index = build_filename_index(SOURCE_DIR)
    total = len(source_index)
    print(f"Indexando {total} documentos-fonte via Bulk API...")

    start = time.perf_counter()

    # Executa a indexação em lote
    success, errors = bulk(
        es,
        generate_actions(source_index),
        chunk_size=BATCH_SIZE,
        request_timeout=120,
    )
    
    elapsed = time.perf_counter() - start

    print(f"\nIndexação concluída em {elapsed:.1f}s ({elapsed / total:.3f}s/doc)")
    print(f"Documentos indexados com sucesso: {success}")
    if errors:
        print(f"Erros: {errors}")