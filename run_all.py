import json
import os

from src.simulate_entities import simulate
from src.knowledge_graph import build_graph
from src.inference_patterns import PATTERNS
from src.quality_checks import flag_schema_violations, validate_quality_checks


def main():
    data = simulate()
    g = build_graph(data)

    flagged = flag_schema_violations(g)
    quality = validate_quality_checks(flagged, data["true_edges"], data["noisy_edges"])

    n_entities = g.number_of_nodes()
    summary = {"n_entities": n_entities, "n_edges": g.number_of_edges(),
               "n_inference_patterns": len(PATTERNS), "quality_checks": quality}

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
