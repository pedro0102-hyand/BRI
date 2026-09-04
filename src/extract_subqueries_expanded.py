from preprocess import tokenize
from preprocess_b import remove_stopwords, stem
from query_expansion import expand_tokens
from sliding_window import make_windows, split_sentences
from config import SUSPICIOUS_DIR
from data_loader import build_filename_index
from extract_subqueries import extract_subqueries


def preprocess_b_expanded(text: str, max_synonyms: int = 2) -> list[str]:

    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = expand_tokens(tokens, max_synonyms=max_synonyms)
    tokens = stem(tokens)
    return tokens


def extract_subqueries_expanded(text: str, window_size: int = 5, stride: int = 3, max_synonyms: int = 2) -> list[list[str]]:

    sentences = split_sentences(text)
    windows = make_windows(sentences, window_size=window_size, stride=stride)
    return [preprocess_b_expanded(window, max_synonyms=max_synonyms) for window in windows]


if __name__ == "__main__":

    suspicious_index = build_filename_index(SUSPICIOUS_DIR)
    sample_name, sample_path = next(iter(suspicious_index.items()))

    with open(sample_path, encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Compara combinação 7 (sem expansão) vs 8 (com expansão) na mesma janela
    subqueries_7 = extract_subqueries(text)
    subqueries_8 = extract_subqueries_expanded(text)

    print(f"Documento de teste: {sample_name}")
    print(f"Total de subconsultas (mesmo em ambas): {len(subqueries_8)}")
    print(f"\nPrimeira subconsulta - combinação 7 (sem expansão), "
          f"{len(subqueries_7[0])} tokens:")
    print(f"  {subqueries_7[0]}")
    print(f"\nPrimeira subconsulta - combinação 8 (com expansão), "
          f"{len(subqueries_8[0])} tokens:")
    print(f"  {subqueries_8[0]}")