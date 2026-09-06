from src.generation.llm_client import LLMClient
from src.generation.prompts import LIT_REVIEW_PROMPT
from src.logger import log

class LiteratureReviewGenerator:
    """Generates the Lit Review section using the Knowledge Graph."""
    
    def __init__(self):
        self.llm = LLMClient()
        
    def generate(self, topic: str, graph_summary: str) -> str:
        """Generates the lit review based on the graph."""
        log.info("Generating Literature Review from Knowledge Graph...")
        prompt = LIT_REVIEW_PROMPT.format(topic=topic, graph_summary=graph_summary)
        
        # Medium temperature for synthesis
        draft = self.llm.generate_text(prompt, temperature=0.5)
        log.info("Literature review draft complete.")
        return draft
