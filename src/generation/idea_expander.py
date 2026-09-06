from src.generation.llm_client import LLMClient
from src.generation.prompts import IDEA_EXPANSION_PROMPT
from src.logger import log

class IdeaExpander:
    """Takes a brief user idea and expands it into a comprehensive research outline."""
    
    def __init__(self):
        self.llm = LLMClient()
        
    def expand(self, user_idea: str) -> str:
        """Expands the user idea."""
        log.info("Expanding user idea into research outline...")
        prompt = IDEA_EXPANSION_PROMPT.format(idea=user_idea)
        
        # Lower temperature for the outline to keep it structured and logical
        expanded_outline = self.llm.generate_text(prompt, temperature=0.3)
        log.info("Idea expansion complete.")
        return expanded_outline
