import pytest
from backend.retrieve import search, get_subgraph
from backend.embeddings import embed_text

def test_embed_text_dimension():
    vec = embed_text("Diabetes")
    assert len(vec) == 384   # matches MiniLM-L6-v2 output dimension

def test_search_results():
    results = search("Which drugs treat diabetes?", k=2)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "Diabetes" in results or "Metformin" in results

def test_get_subgraph():
    subgraph = get_subgraph("Metformin")
    assert isinstance(subgraph, list)
    assert any("Metformin" in edge for edge in subgraph)