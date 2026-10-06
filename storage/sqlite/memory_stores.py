from typing import Optional, List, Dict, Any
from core.contracts import Document, Entity, Event, Problem, Evidence
import json

class InMemoryDocumentStore:
    def __init__(self):
        self.docs: Dict[str, Document] = {}

    async def save_document(self, document: Document) -> None:
        self.docs[document.document_id] = document

    async def get_document(self, document_id: str) -> Optional[Document]:
        return self.docs.get(document_id)

    async def list_documents(self, limit: int = 100, offset: int = 0) -> List[Document]:
        return list(self.docs.values())[offset:offset+limit]

class InMemoryEntityStore:
    def __init__(self):
        self.entities: Dict[str, Entity] = {}

    async def save_entity(self, entity: Entity) -> None:
        self.entities[entity.entity_id] = entity

    async def get_entity(self, entity_id: str) -> Optional[Entity]:
        return self.entities.get(entity_id)

    async def search_entities(self, query: str) -> List[Entity]:
        return [e for e in self.entities.values() if query.lower() in e.canonical_name.lower()]

class InMemoryEventStore:
    def __init__(self):
        self.events: Dict[str, Event] = {}

    async def save_event(self, event: Event) -> None:
        self.events[event.event_id] = event

    async def get_event(self, event_id: str) -> Optional[Event]:
        return self.events.get(event_id)

    async def list_events_for_actor(self, actor_id: str) -> List[Event]:
        return [e for e in self.events.values() if actor_id in e.actors]

class InMemoryProblemStore:
    def __init__(self):
        self.problems: Dict[str, Problem] = {}

    async def save_problem(self, problem: Problem) -> None:
        self.problems[problem.problem_id] = problem

    async def get_problem(self, problem_id: str) -> Optional[Problem]:
        return self.problems.get(problem_id)

    async def list_problems(self, limit: int = 100) -> List[Problem]:
        return list(self.problems.values())[:limit]

class InMemoryEvidenceStore:
    def __init__(self):
        self.evidence: Dict[str, Evidence] = {}

    async def save_evidence(self, evidence: Evidence) -> None:
        self.evidence[evidence.evidence_id] = evidence

    async def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        return self.evidence.get(evidence_id)

class InMemoryGraphStore:
    def __init__(self):
        self.edges: List[Dict[str, Any]] = []

    async def add_edge(self, source_id: str, target_id: str, relation: str, metadata: Dict[str, Any]) -> None:
        self.edges.append({
            "source_id": source_id,
            "target_id": target_id,
            "relation": relation,
            "metadata": metadata
        })

    async def get_neighbors(self, node_id: str, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for edge in self.edges:
            if edge["source_id"] == node_id or edge["target_id"] == node_id:
                if relation is None or edge["relation"] == relation:
                    results.append(edge)
        return results

class InMemoryIndexStore:
    def __init__(self):
        self.corpus: Dict[str, str] = {}

    async def index_document(self, document_id: str, text: str, metadata: Dict[str, Any]) -> None:
        self.corpus[document_id] = text

    async def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        results = []
        q_tokens = set(query.lower().split())
        for doc_id, text in self.corpus.items():
            t_tokens = set(text.lower().split())
            score = len(q_tokens.intersection(t_tokens))
            if score > 0:
                results.append({"document_id": doc_id, "score": float(score)})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

class InMemoryJobStore:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}

    async def save_job(self, job_id: str, status: str, payload: Dict[str, Any]) -> None:
        self.jobs[job_id] = {"job_id": job_id, "status": status, "payload": payload}

    async def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.jobs.get(job_id)

class InMemoryFeedbackStore:
    def __init__(self):
        self.feedbacks: List[Dict[str, Any]] = []

    async def save_feedback(self, feedback_id: str, target_type: str, target_id: str, feedback: str) -> None:
        self.feedbacks.append({
            "feedback_id": feedback_id,
            "target_type": target_type,
            "target_id": target_id,
            "feedback": feedback
        })

    async def get_feedback(self, target_id: str) -> List[Dict[str, Any]]:
        return [f for f in self.feedbacks if f["target_id"] == target_id]
