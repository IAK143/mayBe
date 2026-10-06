from typing import Protocol, Dict, Any, List
from core.contracts import Document, Provenance
import hashlib
import trafilatura

class WebExtractor:
    @staticmethod
    def extract_clean_text(html: str) -> str:
        extracted = trafilatura.extract(html)
        if extracted:
            return extracted
        # Fallback simple tag stripping
        import re
        clean = re.sub('<[^<]+?>', '', html)
        return clean.strip()

class SemHashReference:
    @staticmethod
    def compute_hash(text: str) -> str:
        return hashlib.sha256(text.lower().encode('utf-8')).hexdigest()[:16]

class LocalDeduplicator:
    def __init__(self):
        self.seen_hashes: set = set()

    def is_duplicate(self, text: str) -> bool:
        h = SemHashReference.compute_hash(text)
        if h in self.seen_hashes:
            return True
        self.seen_hashes.add(h)
        return False
