import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_entities import simulate
from src.knowledge_graph import build_graph
from src.inference_patterns import PATTERNS, shared_pathways
from src.quality_checks import flag_schema_violations, validate_quality_checks


def test_at_least_2400_entities():
    data = simulate()
    total = len(data["genes"]) + len(data["diseases"]) + len(data["pathways"])
    assert total >= 2400


def test_exactly_12_inference_patterns():
    assert len(PATTERNS) == 12


def test_shared_pathways_pattern_works():
    data = simulate()
    g = build_graph(data)
    gene_a, gene_b = data["genes"][0], data["genes"][1]
    result = shared_pathways(g, gene_a, gene_b)
    assert isinstance(result, list)


def test_quality_checks_run_without_error():
    data = simulate()
    g = build_graph(data)
    flagged = flag_schema_violations(g)
    quality = validate_quality_checks(flagged, data["true_edges"], data["noisy_edges"])
    assert quality["n_flagged"] >= 0


def test_graph_has_real_nodes_and_edges():
    data = simulate()
    g = build_graph(data)
    assert g.number_of_nodes() > 0
    assert g.number_of_edges() > 0
