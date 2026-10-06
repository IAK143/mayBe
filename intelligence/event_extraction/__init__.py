from typing import List, Dict, Any
from core.contracts import Document, Event, Provenance

class DEEIAReference:
    """Reference event extraction module based on rule and semantic triggers."""

    @staticmethod
    def extract_events(doc: Document) -> List[Event]:
        text = doc.extracted_text.lower()
        events = []

        event_types = {
            "complaint": ["complaint", "backlog", "issue", "problem", "missed", "cannot", "failed"],
            "question": ["how are", "looking for", "recommendation", "anyone know"],
            "attempt": ["tries", "trying", "tried", "tested", "attempt"],
            "failure": ["failed", "isn't keeping up", "doesn't work", "broken"],
            "search": ["searches", "searching", "alternative", "looking again"],
            "resolution": ["fixed it", "solved", "works", "ended up using"]
        }

        for etype, triggers in event_types.items():
            if any(trig in text for trig in triggers):
                events.append(Event(
                    event_type=etype,
                    timestamp=doc.timestamp,
                    source_documents=[doc.document_id],
                    arguments={"raw_trigger_text": text},
                    confidence=0.85,
                    provenance=doc.provenance
                ))

        return events
