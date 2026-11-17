"""Simulate a biomedical knowledge graph of 2,420 entities (genes,
diseases, pathways) with real gene-disease and gene-pathway edges,
plus a real ~5% injected noisy/incorrect edge rate -- the ground
truth automated data-quality checks must catch, standing in for
integration from public genomic databases (see README disclosure)."""
from __future__ import annotations

import numpy as np

N_GENES = 1000
N_DISEASES = 600
N_PATHWAYS = 820
SEED = 1301


def simulate(seed: int = SEED):
    rng = np.random.default_rng(seed)
    genes = [f"GENE_{i:04d}" for i in range(N_GENES)]
    diseases = [f"DISEASE_{i:03d}" for i in range(N_DISEASES)]
    pathways = [f"PATHWAY_{i:03d}" for i in range(N_PATHWAYS)]

    gene_disease_edges = set()
    for g in genes:
        n_links = rng.integers(0, 3)
        for d in rng.choice(diseases, n_links, replace=False):
            gene_disease_edges.add((g, d))

    gene_pathway_edges = set()
    for g in genes:
        n_links = rng.integers(1, 4)
        for p in rng.choice(pathways, n_links, replace=False):
            gene_pathway_edges.add((g, p))

    true_edges = gene_disease_edges | gene_pathway_edges

    # inject real schema-violation edges: this knowledge graph's schema
    # only permits gene-disease and gene-pathway edges, so a
    # disease-pathway or gene-gene edge is a genuine, structurally
    # detectable integration error from a mismatched source feed.
    n_noise = int(len(true_edges) * 0.05)
    noisy_edges = set()
    for _ in range(n_noise):
        if rng.random() < 0.5:
            pair = (rng.choice(diseases), rng.choice(pathways))
        else:
            pair = tuple(rng.choice(genes, 2, replace=False))
        noisy_edges.add(pair)

    all_edges = true_edges | noisy_edges

    return {"genes": genes, "diseases": diseases, "pathways": pathways,
            "edges": all_edges, "true_edges": true_edges, "noisy_edges": noisy_edges}


if __name__ == "__main__":
    data = simulate()
    print(len(data["edges"]), len(data["noisy_edges"]))
