from src.generation.llm_client import LLMClient
from src.generation.prompts import STYLE_EDIT_PROMPT
from src.logger import log


class StyleEditor:
    """Improves the clarity of a draft while preserving its claims and citations."""

    def __init__(self):
        self.llm = LLMClient()

    def edit(self, draft_text: str) -> str:
        """Return a clearer academic draft for the researcher to review."""
        log.info("Editing draft for clarity and consistency...")
        prompt = STYLE_EDIT_PROMPT.format(draft=draft_text)
        edited_text = self.llm.generate_text(prompt, temperature=0.35)
        log.info("Style edit complete; human verification is still required.")
        return edited_text
