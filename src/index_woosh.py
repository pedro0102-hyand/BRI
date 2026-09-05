import time
from whoosh import index
from whoosh.analysis import SimpleAnalyzer
from whoosh.fields import ID, TEXT, Schema
from config import BASE_DIR, SOURCE_DIR
from data_loader import build_filename_index
from preprocess_b import preprocess_b
INDEX_DIR = BASE_DIR / "whoosh_index"

# SimpleAnalyzer: só tokeniza por regex + lowercase, SEM stemming/stopwords
SCHEMA = Schema(doc_id=ID(stored=True, unique=True),content=TEXT(analyzer=SimpleAnalyzer()),)

# Função para construir o índice de documentos-fonte usando Whoosh
def build_index():

    INDEX_DIR.mkdir(exist_ok=True)
    ix = index.create_in(str(INDEX_DIR), SCHEMA)
    writer = ix.writer(limitmb=512, procs=1)

    # Indexar todos os documentos-fonte
    source_index = build_filename_index(SOURCE_DIR)
    total = len(source_index)
    print(f"Indexando {total} documentos-fonte...")

    start = time.perf_counter()
    for i, (filename, path) in enumerate(source_index.items(), start=1):
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        tokens = preprocess_b(text)
        writer.add_document(doc_id=filename, content=" ".join(tokens))

        if i % 500 == 0:
            elapsed = time.perf_counter() - start
            print(f"  {i}/{total} documentos indexados ({elapsed:.1f}s)...")

    print("Commitando índice (pode demorar)...")
    writer.commit()
    elapsed = time.perf_counter() - start
    print(f"Indexação concluída em {elapsed:.1f}s ({elapsed / total:.3f}s/doc)")
    return ix


if __name__ == "__main__":
    build_index()
    print(f"\nÍndice salvo em: {INDEX_DIR}")