from preprocess_b import preprocess_b
from sliding_window import make_windows, split_sentences
from config import SUSPICIOUS_DIR
from data_loader import build_filename_index

# Função para extrair subconsultas do texto, aplicando tokenização, remoção de stopwords e stemming
def extract_subqueries(text: str, window_size: int = 5, stride: int = 3) -> list[list[str]]:

    sentences = split_sentences(text)
    windows = make_windows(sentences, window_size=window_size, stride=stride)
    return [preprocess_b(window) for window in windows]


if __name__ == "__main__":
  
    suspicious_index = build_filename_index(SUSPICIOUS_DIR)
    sample_name, sample_path = next(iter(suspicious_index.items()))

    with open(sample_path, encoding="utf-8", errors="ignore") as f:
        text = f.read()

    subqueries = extract_subqueries(text)

    print(f"Documento de teste: {sample_name}")
    print(f"Total de subconsultas geradas: {len(subqueries)}")
    print(f"\nPrimeira subconsulta (tokens pós preprocess_b):")
    print(f"  {subqueries[0]}")
    print(f"\nTamanho médio de tokens por subconsulta: "
          f"{sum(len(s) for s in subqueries) / len(subqueries):.1f}")