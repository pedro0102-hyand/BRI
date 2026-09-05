import json
from config import PAPERS_JSON, SOURCE_DIR, SUSPICIOUS_DIR

def load_papers():
    """Retorna a lista bruta de registros do papers.json."""
    with open(PAPERS_JSON, encoding="utf-8") as f:
        return json.load(f)


def split_documents(papers):
    """Separa os registros em documentos fonte e suspeitos."""
    source = [p for p in papers if p["type"] == "source-document"]
    suspicious = [p for p in papers if p["type"] == "suspicious-document"]
    return source, suspicious


def build_filename_index(root_dir):
    """Mapeia filename -> caminho completo, varrendo as pastas partX/."""
    return {p.name: p for p in root_dir.glob("part*/*.txt")}


def get_suspicious_queries():
    """Retorna só os documentos suspeitos OFICIAIS (os que estão registrados
    no papers.json com type=suspicious-document) - a pasta no disco pode ter
    mais arquivos do que os 64 que de fato são consultas do trabalho.

    Retorna lista de dicts: {filename, path, src_file (gabarito)}.
    """
    papers = load_papers()
    _, suspicious_records = split_documents(papers)
    suspicious_index = build_filename_index(SUSPICIOUS_DIR)

    queries = []
    for record in suspicious_records:
        filename = record["filename"]
        path = suspicious_index.get(filename)
        if path is None:
            print(f"AVISO: {filename} está no papers.json mas não foi encontrado em disco")
            continue
        queries.append({
            "filename": filename,
            "path": path,
            "src_file": record["src_file"],
        })
    return queries


if __name__ == "__main__":
    papers = load_papers()
    source, suspicious = split_documents(papers)
    print(f"Total de registros: {len(papers)}")
    print(f"Documentos fonte: {len(source)}")
    print(f"Documentos suspeitos: {len(suspicious)}")

    source_index = build_filename_index(SOURCE_DIR)
    suspicious_index = build_filename_index(SUSPICIOUS_DIR)
    print(f"Arquivos .txt encontrados em source-document/: {len(source_index)}")
    print(f"Arquivos .txt encontrados em suspicious-document/: {len(suspicious_index)}")