from typing import List, Dict, Any
from core.contracts import Document
import math

class BM25Reference:
    def __init__(self):
        self.docs: Dict[str, Document] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.df: Dict[str, int] = {}
        self.avg_dl: float = 0.0

    def add_document(self, doc: Document):
        self.docs[doc.document_id] = doc
        tokens = doc.extracted_text.lower().split()
        self.doc_tokens[doc.document_id] = tokens
        for token in set(tokens):
            self.df[token] = self.df.get(token, 0) + 1
        total_len = sum(len(t) for t in self.doc_tokens.values())
        self.avg_dl = total_len / max(1, len(self.docs))

    def search(self, query: str, top_k: int = 10, k1: float = 1.5, b: float = 0.75) -> List[Dict[str, Any]]:
        q_tokens = query.lower().split()
        scores = {}
        n_docs = len(self.docs)

        for doc_id, tokens in self.doc_tokens.items():
            doc_len = len(tokens)
            score = 0.0
            tf_map = {}
            for t in tokens:
                tf_map[t] = tf_map.get(t, 0) + 1

            for qt in q_tokens:
                if qt in tf_map:
                    doc_freq = self.df.get(qt, 0)
                    idf = math.log((n_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
                    tf = tf_map[qt]
                    num = tf * (k1 + 1)
                    den = tf + k1 * (1 - b + b * (doc_len / max(1.0, self.avg_dl)))
                    score += idf * (num / den)

            if score > 0:
                scores[doc_id] = score

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [{"document_id": doc_id, "score": score, "document": self.docs[doc_id]} for doc_id, score in sorted_docs]
