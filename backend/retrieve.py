import faiss
import numpy as np
import os
from neo4j import GraphDatabase
from backend.embeddings import embed_text

# ---------------- FAISS ----------------
DIM = 384
INDEX_FILE = "faiss.index"

nodes = ["Diabetes", "Metformin", "Insulin"]

def build_index():
    embeddings = [embed_text(n) for n in nodes]
    index = faiss.IndexFlatL2(DIM)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, INDEX_FILE)
    return index

def load_index():
    if os.path.exists(INDEX_FILE):
        return faiss.read_index(INDEX_FILE)
    return build_index()

index = load_index()

def search(query: str, k=3):
    q_vec = embed_text(query).astype("float32")
    D, I = index.search(np.array([q_vec]), k)
    return [nodes[i] for i in I[0]]

# ---------------- Neo4j ----------------
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=(os.getenv("NEO4J_USER", ""),
          os.getenv("NEO4J_PASS", ""))
)

def get_subgraph(node_name: str):
    with driver.session() as session:
        result = session.run("""
            MATCH (n {name:$name})-[r]->(m)
            RETURN n.name AS n_name, type(r) AS rel_type, m.name AS m_name
        """, name=node_name)

        return [
            f"{rec['n_name']} -[{rec['rel_type']}]-> {rec['m_name']}"
            for rec in result
        ]