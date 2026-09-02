import nltk
from nltk.corpus import stopwords
from top_bottom_words import load_frequencies

try:

    STOPWORDS_EN = set(stopwords.words("english"))
except LookupError:

    nltk.download("stopwords")
    STOPWORDS_EN = set(stopwords.words("english"))


if __name__ == "__main__":

    freq, total_words = load_frequencies()
    # Frequência de cada stopword na coleção (0 se não aparecer)
    stopword_freq = [(w, freq.get(w, 0)) for w in STOPWORDS_EN]
    stopword_freq.sort(key=lambda x: x[1], reverse=True)

    print(f"Total de stopwords NLTK (inglês): {len(STOPWORDS_EN)}")

    print("\nTop 10 stopwords mais frequentes na coleção:")
    for word, count in stopword_freq[:10]:
        print(f"  {word}: {count}")

    print("\nTop 10 stopwords menos frequentes na coleção:")
    for word, count in stopword_freq[-10:]:
        print(f"  {word}: {count}")

    # Quantas stopwords nem aparecem na coleção
    zero_count = sum(1 for _, c in stopword_freq if c == 0)
    print(f"\nStopwords que não aparecem na coleção: {zero_count}")

    # Quanto as stopwords representam do total de palavras (peso no corpus)
    stopword_total = sum(c for _, c in stopword_freq)
    print(f"Soma de ocorrências de stopwords: {stopword_total} "
          f"({stopword_total / total_words:.1%} do total de palavras)")