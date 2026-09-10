import json
from config import REPORTS_DIR
from data_loader import get_suspicious_queries
from precision import average_precision_at_k
from recall import average_recall_at_k

K_VALUES = [2, 4, 6, 8, 10]

RESULT_FILES = {
    "whoosh_combo7": "whoosh_combo7_results.json",
    "whoosh_combo8": "whoosh_combo8_results.json",
    "es_combo7": "es_combo7_results.json",
    "es_combo8": "es_combo8_results.json",
}


if __name__ == "__main__":
    
    queries = get_suspicious_queries()
    gabarito = {q["filename"]: q["src_file"] for q in queries}

    summary = {}
    for name, filename in RESULT_FILES.items():
        path = REPORTS_DIR / filename
        if not path.exists():
            print(f"AVISO: {path} não encontrado, pulando '{name}'")
            continue

        with open(path, encoding="utf-8") as f:
            results = json.load(f)

        summary[name] = {
            "precision": {k: average_precision_at_k(results, gabarito, k) for k in K_VALUES},
            "recall": {k: average_recall_at_k(results, gabarito, k) for k in K_VALUES},
        }

        print(f"\n{name}:")
        print(f"  {'k':<4} {'precision':>10} {'recall':>10}")
        for k in K_VALUES:
            p = summary[name]["precision"][k]
            r = summary[name]["recall"][k]
            print(f"  {k:<4} {p:>10.4f} {r:>10.4f}")

    with open(REPORTS_DIR / "metricas_consolidadas.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResumo salvo em: {REPORTS_DIR / 'metricas_consolidadas.json'}")