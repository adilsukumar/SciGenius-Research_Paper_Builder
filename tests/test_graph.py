import pytest
from src.graph.pdf_parser import PDFParser
from src.graph.builder import GraphBuilder

def test_clean_text():
    raw = "This   is \n\n a test."
    cleaned = PDFParser.clean_text(raw)
    assert cleaned == "This is \n a test."
    
def test_graph_builder():
    builder = GraphBuilder()
    entities = [{"text": "AI", "label": "CONCEPT"}, {"text": "Machine Learning", "label": "CONCEPT"}]
    relations = [{"source": "Machine Learning", "target": "AI", "relation": "is a subset of"}]
    
    g = builder.build(entities, relations)
    assert g.number_of_nodes() == 2
    assert g.number_of_edges() == 1
    assert g.has_edge("Machine Learning", "AI")
