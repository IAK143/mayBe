from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uuid
from core.contracts import Document, Entity, Event, Problem, Provenance
from storage.sqlite.memory_stores import (
    InMemoryDocumentStore, InMemoryEntityStore, InMemoryEventStore,
    InMemoryProblemStore, InMemoryJobStore, InMemoryFeedbackStore
)

app = FastAPI(
    title="Open Internet Intelligence Engine API",
    version="0.1.0",
    description="Programmatic control & inspection REST layer (No UI)"
)

# Global store instances
doc_store = InMemoryDocumentStore()
entity_store = InMemoryEntityStore()
event_store = InMemoryEventStore()
problem_store = InMemoryProblemStore()
job_store = InMemoryJobStore()
feedback_store = InMemoryFeedbackStore()

class IngestRequest(BaseModel):
    source: str
    url: Optional[str] = None
    raw_text: str

class FeedbackRequest(BaseModel):
    target_type: str
    target_id: str
    feedback: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "open-internet-intelligence-engine", "version": "0.1.0"}

@app.get("/metrics")
async def get_metrics():
    return {
        "documents_count": len(doc_store.docs),
        "entities_count": len(entity_store.entities),
        "events_count": len(event_store.events),
        "problems_count": len(problem_store.problems)
    }

@app.get("/pipeline/status")
async def pipeline_status():
    return {"status": "idle", "active_jobs": len(job_store.jobs)}

@app.post("/jobs/ingest")
async def job_ingest(req: IngestRequest):
    job_id = str(uuid.uuid4())
    prov = Provenance(source=req.source, source_url=req.url)
    doc = Document(
        source=req.source,
        canonical_url=req.url,
        raw_text=req.raw_text,
        extracted_text=req.raw_text,
        provenance=prov
    )
    await doc_store.save_document(doc)
    await job_store.save_job(job_id, "COMPLETED", {"document_id": doc.document_id})
    return {"job_id": job_id, "status": "COMPLETED", "document_id": doc.document_id}

@app.post("/jobs/reindex")
async def job_reindex():
    job_id = str(uuid.uuid4())
    await job_store.save_job(job_id, "COMPLETED", {"action": "reindex"})
    return {"job_id": job_id, "status": "COMPLETED"}

@app.post("/jobs/recluster")
async def job_recluster():
    job_id = str(uuid.uuid4())
    await job_store.save_job(job_id, "COMPLETED", {"action": "recluster"})
    return {"job_id": job_id, "status": "COMPLETED"}

@app.post("/jobs/recompute-state")
async def job_recompute_state():
    job_id = str(uuid.uuid4())
    await job_store.save_job(job_id, "COMPLETED", {"action": "recompute-state"})
    return {"job_id": job_id, "status": "COMPLETED"}

@app.get("/document/{id}")
async def get_document(id: str):
    doc = await doc_store.get_document(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@app.get("/entity/{id}")
async def get_entity(id: str):
    ent = await entity_store.get_entity(id)
    if not ent:
        raise HTTPException(status_code=404, detail="Entity not found")
    return ent

@app.get("/event/{id}")
async def get_event(id: str):
    ev = await event_store.get_event(id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    return ev

@app.get("/problem/{id}")
async def get_problem(id: str):
    prob = await problem_store.get_problem(id)
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")
    return prob

@app.get("/provenance/{id}")
async def get_provenance(id: str):
    doc = await doc_store.get_document(id)
    if doc:
        return doc.provenance
    raise HTTPException(status_code=404, detail="Provenance not found for given ID")
