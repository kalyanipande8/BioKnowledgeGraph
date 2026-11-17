// Authored-but-not-executed reference: the real Neo4j/Cypher schema
// and queries this knowledge graph would use in production. No Neo4j
// instance is available in this environment, so src/knowledge_graph.py
// builds the identical gene-disease-pathway graph in networkx as the
// executed mirror, and all measured results in this repo come from
// that mirror.

CREATE CONSTRAINT gene_id IF NOT EXISTS FOR (g:Gene) REQUIRE g.id IS UNIQUE;
CREATE CONSTRAINT disease_id IF NOT EXISTS FOR (d:Disease) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT pathway_id IF NOT EXISTS FOR (p:Pathway) REQUIRE p.id IS UNIQUE;

// gene-disease and gene-pathway relationships
MATCH (g:Gene {id: $gene_id}), (d:Disease {id: $disease_id})
MERGE (g)-[:ASSOCIATED_WITH]->(d);

// inference pattern example: shared pathways between two genes
// (the same traversal src/inference_patterns.py's shared_pathways() performs)
MATCH (g1:Gene {id: $gene_a})-[:PARTICIPATES_IN]->(p:Pathway)<-[:PARTICIPATES_IN]-(g2:Gene {id: $gene_b})
RETURN p.id;

// two-hop disease inference via pathway (same traversal as
// two_hop_diseases_via_pathway())
MATCH (g:Gene {id: $gene_id})-[:PARTICIPATES_IN]->(:Pathway)<-[:PARTICIPATES_IN]-(:Gene)-[:ASSOCIATED_WITH]->(d:Disease)
RETURN DISTINCT d.id;
