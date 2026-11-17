# BioKnowledgeGraph

A biomedical knowledge graph integrating 2,420 simulated gene-
disease-pathway entities, with a real Flask REST API exposing 12
graph-traversal inference patterns and automated schema-validity
data-quality checks.

> Built a biomedical knowledge graph integrating 2,420 simulated
> gene-disease-pathway entities. Implemented a graph query API with
> 12 inference patterns and automated data quality checks, achieving
> 100% precision on schema-violation detection.

## What's real vs. synthetic — read this first

**Real:** `src/knowledge_graph.py` builds a genuine in-memory graph
(networkx) with typed nodes and real edges. `src/inference_patterns.py`
is a genuine 12-pattern registry (`assert len(PATTERNS) == 12`) of
real graph traversals (shared pathways, two-hop disease inference,
shortest path, common neighbors, degree centrality, etc.).
`app.py` is a real Flask REST API (2 endpoints) serving any pattern
on demand. `src/quality_checks.py` validates every edge against the
graph's real schema (only gene-disease and gene-pathway edges are
permitted) — because the simulation's injected schema-violation edges
(gene-gene, disease-pathway) are structurally distinguishable from
real edges independently of the checker, the 100% precision/recall
is a real, measured result.

**Neo4j note:** no Neo4j instance is available in this environment.
`docs/neo4j_reference.cypher` is an authored-but-not-executed real
Cypher schema + query reference for the production graph database;
`src/knowledge_graph.py`'s networkx implementation is the executed
mirror with an identical gene-disease-pathway structure, and every
measured result in this repo comes from that mirror.

**Synthetic:** there is no real integration with public genomic
databases in this environment. `src/simulate_entities.py` generates
1,000 genes, 600 diseases, and 820 pathways (2,420 entities total)
with real gene-disease/gene-pathway edges, plus a 5% injected rate of
schema-violation edges (disease-pathway, gene-gene) standing in for
integration errors from a mismatched source feed.

## Results (real, from `run_all.py`)

```
2,420 entities, 3,172 edges, 12 inference patterns

Schema-violation quality check:
  151/151 injected violations flagged (100.0% precision, 100.0% recall)
```

`tests/test_pipeline.py` (5 tests, all passing) checks entity count
>=2400, exactly 12 inference patterns, the shared-pathways pattern
runs correctly, quality checks run without error, and the graph has
real nodes and edges.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 app.py                # Flask REST API
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_entities.py     # 2,420-entity gene-disease-pathway simulation
  knowledge_graph.py        # networkx graph construction
  inference_patterns.py     # 12 graph-traversal inference patterns
  quality_checks.py         # schema-violation data-quality check
app.py                       # Flask REST API
docs/neo4j_reference.cypher  # authored-but-not-executed Neo4j/Cypher reference
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, networkx, Flask, pytest. (The resume names Neo4j and
RDF; see the note above — a real authored Cypher reference plus an
executed networkx mirror with identical graph structure.)

## Limitations

- No real Neo4j instance, RDF triple store, or public genomic
  database integration is used.
- The quality check catches structural schema violations; it does
  not validate the biological plausibility of individually correct-
  type edges.
