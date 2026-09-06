import spacy
from typing import List, Dict, Any
from src.logger import log

class RelationExtractor:
    """Extracts relations between named entities using dependency parsing."""
    
    def __init__(self, model: str = "en_core_web_sm"):
        self.nlp = spacy.load(model)
        
    def extract_relations(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Finds verbs/actions linking two entities in a sentence."""
        doc = self.nlp(text)
        relations = []
        
        # A simplified heuristic relation extractor based on sentence structure
        # (Subject -> Verb -> Object)
        for sent in doc.sents:
            subjects = [tok for tok in sent if "subj" in tok.dep_]
            objects = [tok for tok in sent if "obj" in tok.dep_]
            verbs = [tok for tok in sent if tok.pos_ == "VERB"]
            
            if subjects and objects and verbs:
                # Basic linkage (First Subj -> First Verb -> First Obj)
                rel = {
                    "source": subjects[0].text,
                    "target": objects[0].text,
                    "relation": verbs[0].text
                }
                relations.append(rel)
                
        log.info(f"Extracted {len(relations)} potential relations.")
        return relations
