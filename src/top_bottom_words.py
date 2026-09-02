import pickle
from word_frequency import FREQ_PICKLE

# Função para carregar as frequências de palavras do arquivo pickle
def load_frequencies():

    with open(FREQ_PICKLE, "rb") as f:
        data = pickle.load(f)
    return data["freq"], data["total_words"]


if __name__ == "__main__":

    freq, total_words = load_frequencies()
    print("Top 10 palavras mais frequentes:")
    for word, count in freq.most_common(10):
        print(f"  {word}: {count}")

    print("\nTop 10 palavras menos frequentes (entre as que aparecem):")
    # least_common() não existe no Counter; ordenamos manualmente
    least = sorted(freq.items(), key=lambda x: x[1])[:10]
    for word, count in least:
        print(f"  {word}: {count}")

    # Quantas palavras aparecem só 1 vez (hapax legomena) - dado útil pra discussão
    hapax = sum(1 for _, c in freq.items() if c == 1)
    print(f"\nPalavras que aparecem apenas 1 vez: {hapax} ({hapax / len(freq):.1%} do vocabulário)")