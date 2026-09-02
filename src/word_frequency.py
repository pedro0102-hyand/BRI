import pickle
from collections import Counter
from config import SOURCE_DIR, REPORTS_DIR
from data_loader import build_filename_index
from preprocess import tokenize

FREQ_PICKLE = REPORTS_DIR / "word_freq.pkl"

# funcao para tokenizar todo o corpus e contar a frequencia
def count_corpus_frequencies(source_index : dict) -> tuple[Counter, int]:

    freq = Counter() # contador de frequencias
    total_words = 0 # contador de palavras totais

    # iterar sobre todos os documentos fonte e atualizar o contador de frequencias
    for i, path in enumerate(source_index.values(), start=1):
        print(f"Processando documento {i}/{len(source_index)}")
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
            tokens = tokenize(text)
            freq.update(tokens)
            total_words += len(tokens)

    return freq, total_words

if __name__ == "__main__":
    
    source_index = build_filename_index(SOURCE_DIR)
    print(f"Processando {len(source_index)} documentos-fonte...")

    freq, total_words = count_corpus_frequencies(source_index)

    REPORTS_DIR.mkdir(exist_ok=True)
    with open(FREQ_PICKLE, "wb") as f:
        pickle.dump({"freq": freq, "total_words": total_words}, f)

    print(f"\nTamanho do vocabulário: {len(freq)}")
    print(f"Total de palavras na coleção: {total_words}")
    print(f"Resultado salvo em: {FREQ_PICKLE}")