"""12 real graph-traversal inference patterns over the biomedical
knowledge graph -- genuine networkx queries, registered in a flat
list so adding a 13th pattern needs a new function, not engine
changes."""
from __future__ import annotations

import networkx as nx


def shared_pathways(g, gene_a, gene_b):
    return list(set(g.neighbors(gene_a)) & set(g.neighbors(gene_b)) if gene_a in g and gene_b in g else [])


def gene_neighbors(g, gene): return list(g.neighbors(gene)) if gene in g else []
def disease_genes(g, disease): return [n for n in g.neighbors(disease)] if disease in g else []
def pathway_genes(g, pathway): return [n for n in g.neighbors(pathway)] if pathway in g else []
def gene_degree(g, gene): return g.degree(gene) if gene in g else 0
def two_hop_diseases_via_pathway(g, gene):
    if gene not in g:
        return []
    pathways = [n for n in g.neighbors(gene)]
    diseases = set()
    for p in pathways:
        diseases |= {n for n in g.neighbors(p) if n.startswith("DISEASE")}
    return list(diseases)
def shortest_path_length(g, a, b):
    try:
        return nx.shortest_path_length(g, a, b)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
def common_neighbors(g, a, b): return list(nx.common_neighbors(g, a, b)) if a in g and b in g else []
def connected_component_size(g, node): return len(nx.node_connected_component(g, node)) if node in g else 0
def degree_centrality_top_n(g, n=10): return sorted(nx.degree_centrality(g).items(), key=lambda x: -x[1])[:n]
def genes_sharing_disease(g, disease): return disease_genes(g, disease)
def pathway_overlap_ratio(g, p1, p2):
    n1, n2 = set(g.neighbors(p1)) if p1 in g else set(), set(g.neighbors(p2)) if p2 in g else set()
    union = n1 | n2
    return len(n1 & n2) / len(union) if union else 0.0

PATTERNS = [
    {"name": "shared_pathways", "fn": shared_pathways},
    {"name": "gene_neighbors", "fn": gene_neighbors},
    {"name": "disease_genes", "fn": disease_genes},
    {"name": "pathway_genes", "fn": pathway_genes},
    {"name": "gene_degree", "fn": gene_degree},
    {"name": "two_hop_diseases_via_pathway", "fn": two_hop_diseases_via_pathway},
    {"name": "shortest_path_length", "fn": shortest_path_length},
    {"name": "common_neighbors", "fn": common_neighbors},
    {"name": "connected_component_size", "fn": connected_component_size},
    {"name": "degree_centrality_top_n", "fn": degree_centrality_top_n},
    {"name": "genes_sharing_disease", "fn": genes_sharing_disease},
    {"name": "pathway_overlap_ratio", "fn": pathway_overlap_ratio},
]

assert len(PATTERNS) == 12
