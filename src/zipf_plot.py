import matplotlib.pyplot as plt
from config import REPORTS_DIR
from top_bottom_words import load_frequencies

OUTPUT_PATH = REPORTS_DIR / "zipf_distribution.png"


if __name__ == "__main__":
    freq, total_words = load_frequencies()

    # Ordena por frequência decrescente -> a posição na lista é o rank
    counts = sorted(freq.values(), reverse=True)
    ranks = range(1, len(counts) + 1)

    plt.figure(figsize=(8, 6))
    plt.loglog(ranks, counts, marker=".", linestyle="none", markersize=2)
    plt.xlabel("Rank da palavra (log)")
    plt.ylabel("Frequência (log)")
    plt.title("Distribuição das palavras no corpus x frequência das palavras (Lei de Zipf)")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)

    REPORTS_DIR.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    print(f"Gráfico salvo em: {OUTPUT_PATH}")