import json
import matplotlib.pyplot as plt
from config import REPORTS_DIR

K_VALUES = [2, 4, 6, 8, 10]

def plot_recall(data: dict, tool_name: str, combo7_key: str, combo8_key: str, output_path):

    r7 = [data[combo7_key]["recall"][str(k)] for k in K_VALUES]
    r8 = [data[combo8_key]["recall"][str(k)] for k in K_VALUES]

    plt.figure(figsize=(7, 5))
    plt.plot(K_VALUES, r7, marker="o", label="Combinação 7 (sem expansão)")
    plt.plot(K_VALUES, r8, marker="o", label="Combinação 8 (com expansão)")
    plt.xlabel("k")
    plt.ylabel("Recall@k (média das 64 consultas)")
    plt.title(f"Recall@k - {tool_name}")
    plt.xticks(K_VALUES)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Salvo: {output_path}")


if __name__ == "__main__":

    with open(REPORTS_DIR / "metricas_consolidadas.json", encoding="utf-8") as f:
        data = json.load(f)

    plot_recall(data, "Whoosh", "whoosh_combo7", "whoosh_combo8",
                REPORTS_DIR / "recall_whoosh.png")
    plot_recall(data, "Elasticsearch", "es_combo7", "es_combo8",
                REPORTS_DIR / "recall_elasticsearch.png")