from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl
import uuid

def default_uuid() -> str:
    return str(uuid.uuid4())

def default_now() -> datetime:
    return datetime.now(timezone.utc)

class Provenance(BaseModel):
    provenance_id: str = Field(default_factory=default_uuid)
    source: str
    source_url: Optional[str] = None
    observed_at: datetime = Field(default_factory=default_now)
    algorithm: str = "reference"
    algorithm_version: str = "0.1.0"
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    parent_provenance_ids: List[str] = Field(default_factory=list)

class Document(BaseModel):
    document_id: str = Field(default_factory=default_uuid)
    source: str
    canonical_url: Optional[str] = None
    timestamp: datetime = Field(default_factory=default_now)
    author_reference: Optional[str] = None
    raw_text: str
    extracted_text: str
    language: str = "en"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    provenance: Provenance

class Entity(BaseModel):
    entity_id: str = Field(default_factory=default_uuid)
    type: str  # Person, Organization, Product, Technology, Problem, Solution, Location
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    provenance: Provenance

class Event(BaseModel):
    event_id: str = Field(default_factory=default_uuid)
    event_type: str  # complaint, question, attempt, failure, resolution, search, switch, etc.
    timestamp: datetime = Field(default_factory=default_now)
    actors: List[str] = Field(default_factory=list)  # Entity IDs
    objects: List[str] = Field(default_factory=list)  # Entity IDs or strings
    arguments: Dict[str, Any] = Field(default_factory=dict)
    source_documents: List[str] = Field(default_factory=list)  # Document IDs
    confidence: float = 1.0
    provenance: Provenance

class Evidence(BaseModel):
    evidence_id: str = Field(default_factory=default_uuid)
    source_document: str  # Document ID
    extracted_span: str
    evidence_type: str  # supports, contradicts, supersedes
    supports: List[str] = Field(default_factory=list)  # Problem ID / Event ID / Claim
    contradicts: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=default_now)
    reliability: float = 1.0
    provenance: Provenance

class ProblemStateDistribution(BaseModel):
    UNKNOWN: float = 0.0
    LATENT_FRICTION: float = 0.0
    ACTIVE_PROBLEM: float = 0.0
    INVESTIGATING: float = 0.0
    SEARCHING_FOR_SOLUTION: float = 0.0
    COMPARING_SOLUTIONS: float = 0.0
    PROCUREMENT: float = 0.0
    RESOLVED: float = 0.0
    PARTIALLY_RESOLVED: float = 0.0
    FAILED: float = 0.0
    ABANDONED: float = 0.0
    RECURRED: float = 0.0
    ESCALATING: float = 0.0

class ResolutionStateDistribution(BaseModel):
    UNRESOLVED: float = 1.0
    PARTIALLY_RESOLVED: float = 0.0
    RESOLVED: float = 0.0
    FAILED_SOLUTION: float = 0.0
    UNKNOWN: float = 0.0

class Problem(BaseModel):
    problem_id: str = Field(default_factory=default_uuid)
    canonical_description: str
    semantic_cluster: str
    actors: List[str] = Field(default_factory=list)
    symptoms: List[str] = Field(default_factory=list)
    causes: List[str] = Field(default_factory=list)
    attempted_solutions: List[str] = Field(default_factory=list)
    competing_solutions: List[str] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    first_seen: datetime = Field(default_factory=default_now)
    last_seen: datetime = Field(default_factory=default_now)
    state: ProblemStateDistribution = Field(default_factory=ProblemStateDistribution)
    resolution_state: ResolutionStateDistribution = Field(default_factory=ResolutionStateDistribution)
    urgency: float = 0.5
    novelty: float = 0.5
    confidence: float = 1.0
    open_loop_score: float = 0.0
