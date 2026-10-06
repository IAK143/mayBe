from typing import List, Dict, Any
from core.contracts import Document, Entity, Provenance
import re

class GLiNERReference:
    """Deterministic fallback reference implementation for zero-shot GLiNER entity extraction."""

    @staticmethod
    def extract_entities(doc: Document) -> List[Entity]:
        text = doc.extracted_text
        entities = []

        # Simple rule-based/regex extraction fallback for entities
        # Persons (Capitalized Words)
        persons = re.findall(r'\b[A-Z][a-z]+\b', text)
        for p in set(persons):
            if p not in ["I", "A", "The", "Day", "Problem", "Solution"]:
                entities.append(Entity(
                    type="Person",
                    canonical_name=p,
                    confidence=0.8,
                    provenance=doc.provenance
                ))

        # Keywords for Products / Problems
        if "solution" in text.lower() or "tool" in text.lower():
            entities.append(Entity(
                type="Product",
                canonical_name="Target System / Product",
                confidence=0.7,
                provenance=doc.provenance
            ))

        return entities
