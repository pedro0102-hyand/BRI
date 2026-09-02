import re
from data_loader import build_filename_index
from config import SOURCE_DIR

# expressão regular para identificar tokens (palavras) no texto
TOKEN_RE = re.compile(r"[a-zA-ZÀ-ÿ]+")

# Função para tokenizar o texto em palavras
def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


if __name__ == "__main__":

    source_index = build_filename_index(SOURCE_DIR)
    sample_name, sample_path = next(iter(source_index.items()))

    with open(sample_path, encoding="utf-8", errors="ignore") as f:
        text = f.read()

    tokens = tokenize(text)
    print(f"Documento de teste: {sample_name}")
    print(f"Tamanho do texto: {len(text)} caracteres")
    print(f"Total de tokens: {len(tokens)}")
    print(f"Primeiros 20 tokens: {tokens[:20]}")