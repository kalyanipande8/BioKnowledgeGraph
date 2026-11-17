"""Real Flask REST API over the biomedical knowledge graph, serving
any of the 12 registered inference patterns on demand."""
from __future__ import annotations

from flask import Flask, jsonify, request

from src.simulate_entities import simulate
from src.knowledge_graph import build_graph
from src.inference_patterns import PATTERNS

app = Flask(__name__)
_data = simulate()
_graph = build_graph(_data)
_PATTERN_REGISTRY = {p["name"]: p["fn"] for p in PATTERNS}


@app.route("/api/patterns")
def list_patterns():
    return jsonify(sorted(_PATTERN_REGISTRY.keys()))


@app.route("/api/query/<pattern_name>")
def run_pattern(pattern_name):
    if pattern_name not in _PATTERN_REGISTRY:
        return jsonify({"error": "unknown pattern"}), 404
    args = request.args.getlist("node")
    try:
        result = _PATTERN_REGISTRY[pattern_name](_graph, *args)
    except TypeError:
        result = _PATTERN_REGISTRY[pattern_name](_graph)
    return jsonify(result if not isinstance(result, (set,)) else list(result))


if __name__ == "__main__":
    app.run(debug=True)
