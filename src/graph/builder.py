import networkx as nx
from typing import List, Dict, Any
from src.logger import log

class GraphBuilder:
    """Constructs a NetworkX Knowledge Graph from Entities and Relations."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def build(self, entities: List[Dict[str, Any]], relations: List[Dict[str, Any]]) -> nx.DiGraph:
        """Adds nodes and edges to the graph."""
        log.info("Building Knowledge Graph...")
        
        # Add Nodes
        for ent in entities:
            self.graph.add_node(ent['text'], label=ent.get('label', 'CONCEPT'))
            
        # Add Edges
        for rel in relations:
            # Only add edge if both source and target exist as nodes (to keep graph clean)
            if self.graph.has_node(rel['source']) and self.graph.has_node(rel['target']):
                self.graph.add_edge(rel['source'], rel['target'], relation=rel['relation'])
            else:
                # Add them anyway for a richer, albeit noisier, graph
                self.graph.add_edge(rel['source'], rel['target'], relation=rel['relation'])
                
        log.info(f"Graph built with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")
        return self.graph
        
    def get_summary(self) -> str:
        """Returns a string summary of the graph (useful for LLM context)."""
        nodes = list(self.graph.nodes())[:50] # Limit to avoid context explosion
        edges = list(self.graph.edges(data=True))[:50]
        
        summary = f"Graph Summary: {self.graph.number_of_nodes()} Nodes, {self.graph.number_of_edges()} Edges.\n"
        summary += f"Key Concepts: {', '.join([str(n) for n in nodes])}\n"
        summary += "Key Relations:\n"
        for u, v, data in edges:
            summary += f"- {u} [{data.get('relation', 'related_to')}] {v}\n"
            
        return summary
