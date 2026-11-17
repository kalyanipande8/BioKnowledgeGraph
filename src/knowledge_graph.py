"""Real in-memory graph construction via networkx -- the executed
Python mirror of a Neo4j property graph (see README's Neo4j
disclosure)."""
from __future__ import annotations

import networkx as nx


def build_graph(data: dict) -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(data["genes"], node_type="gene")
    g.add_nodes_from(data["diseases"], node_type="disease")
    g.add_nodes_from(data["pathways"], node_type="pathway")
    g.add_edges_from(data["edges"])
    return g
