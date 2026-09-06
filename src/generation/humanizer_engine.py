from src.generation.llm_client import LLMClient
from src.generation.prompts import HUMANIZE_PROMPT
from src.logger import log

class HumanizerEngine:
    """Takes AI-generated text and rewrites it to bypass AI detection."""
    
    def __init__(self):
        self.llm = LLMClient()
        
    def humanize(self, draft_text: str) -> str:
        """Rewrites the text to increase perplexity and burstiness."""
        log.info("Humanizing text to evade AI detection...")
        prompt = HUMANIZE_PROMPT.format(draft=draft_text)
        
        # High temperature (0.8 - 0.9) to introduce variability and unpredictability
        # This is the key to defeating perplexity-based AI detectors
        humanized_text = self.llm.generate_text(prompt, temperature=0.85)
        log.info("Humanization complete.")
        return humanized_text
