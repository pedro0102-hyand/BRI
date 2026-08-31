import json
from config import PAPERS_JSON, SOURCE_DIR, SUSPICIOUS_DIR

# carregar os registros do papers.json
def load_papers():
    with open(PAPERS_JSON, encoding = "utf-8") as f :
        return json.load(f)

# dividir em documentos fontes e suspeitos
def split_documents(papers):

    source = [p for p in papers if p["type"] == "source-document"]
    suspicious = [p for p in papers if p["type"] == "suspicious-document"]
    return source, suspicious

def build_filename_index(root_dir):
    return {p.name : p for p in root_dir.glob("part*/*.txt")}

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