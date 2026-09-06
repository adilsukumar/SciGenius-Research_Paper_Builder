import spacy
from typing import List, Dict, Any
from src.logger import log

class NEREngine:
    """Extracts Named Entities (Concepts, Technologies, Organizations) from text."""
    
    def __init__(self, model: str = "en_core_web_sm"):
        log.info(f"Loading NLP model: {model}")
        try:
            self.nlp = spacy.load(model)
        except OSError:
            log.warning(f"Model {model} not found. Attempting to download...")
            spacy.cli.download(model)
            self.nlp = spacy.load(model)
            
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Processes text and returns a list of named entities."""
        doc = self.nlp(text)
        entities = []
        
        # We focus on specific entity types relevant to research
        relevant_labels = {"ORG", "PERSON", "GPE", "PRODUCT", "EVENT", "WORK_OF_ART"}
        
        for ent in doc.ents:
            if ent.label_ in relevant_labels or len(ent.text) > 3: # Also capture long unknown terms (potential concepts)
                entities.append({
                    "text": ent.text.strip(),
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
        
        # Deduplicate entities
        unique_entities = {e['text']: e for e in entities}.values()
        log.info(f"Extracted {len(unique_entities)} unique entities.")
        return list(unique_entities)
