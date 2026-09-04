import nltk
from config import SUSPICIOUS_DIR
from data_loader import build_filename_index
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

def split_sentences(text: str) -> list[str]:
    return sent_tokenize(text)


def make_windows(sentences: list[str], window_size: int = 5, stride: int = 3) -> list[str]:
    windows = []
    for start in range(0, len(sentences), stride):
        block = sentences[start:start + window_size]
        if not block:
            break
        windows.append(" ".join(block))
        if start + window_size >= len(sentences):
            break
    return windows


if __name__ == "__main__":
    
    suspicious_index = build_filename_index(SUSPICIOUS_DIR)
    sample_name, sample_path = next(iter(suspicious_index.items()))

    with open(sample_path, encoding="utf-8", errors="ignore") as f:
        text = f.read()

    sentences = split_sentences(text)
    windows = make_windows(sentences, window_size=5, stride=3)

    print(f"Documento de teste: {sample_name}")
    print(f"Total de sentenças: {len(sentences)}")
    print(f"Total de janelas geradas (tamanho=5, passo=3): {len(windows)}")
    print(f"\nPrimeira janela:\n  {windows[0][:200]}...")
    print(f"\nSegunda janela (deve sobrepor com a primeira):\n  {windows[1][:200]}...")