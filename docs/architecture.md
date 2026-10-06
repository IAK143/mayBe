# System Architecture & Data Flow

## Overview
The Open Internet Intelligence Engine is an open-source, local-first, continuously learning system designed to observe internet observations, extract entities & events, construct temporal problem graphs, and infer unresolved market problems (open loops).

```text
INTERNET
   ↓
DISCOVERY
   ↓
CRAWLING
   ↓
EXTRACTION
   ↓
NORMALIZATION
   ↓
DEDUP
   ↓
SPARSE RETRIEVAL
   ↓
MULTI-VECTOR RETRIEVAL
   ↓
RERANKING
   ↓
ENTITY EXTRACTION
   ↓
EVENT EXTRACTION
   ↓
ENTITY RESOLUTION
   ↓
TEMPORAL GRAPH
   ↓
EVENT CLUSTERING
   ↓
PROBLEM DISCOVERY
   ↓
CHANGE DETECTION
   ↓
STATE INFERENCE
   ↓
RESOLUTION DETECTION
   ↓
OPEN LOOP DETECTION
   ↓
EVIDENCE RANKING
   ↓
HUMAN FEEDBACK
   ↓
ONLINE LEARNING
   └───────────────────────────┐
                               ↓
                        SEARCH POLICY
                               ↓
                         INTERNET AGAIN
```

## Subsystem Breakdown
- **Core (`core/`)**: Standard internal Pydantic v2 domain models and contracts.
- **Ingestion (`ingestion/`)**: Source-aware adapters, deterministic HTML parsing (`trafilatura`), and multi-layer deduplication (`SemHash`).
- **Retrieval (`retrieval/`)**: Three-stage retrieval stack (lexical BM25, sparse vector, multi-vector late interaction, multi-hop) backed by GuideKP, SPRAWL, BMP, ConstBERT, PyLate, FastPlaid, SPLADE, and Baleen adapters.
- **Intelligence (`intelligence/`)**: Entity extraction (GLiNER), event extraction (DEEIA), entity resolution (Splink), online event clustering (StoryForest), contradiction & resolution engines.
- **Temporal & Graph (`temporal/`, `graph/`)**: Probabilistic problem state inference $P(Z_t | O_{1:t})$, resolution state inference $P(R_t | E_{1:t})$, change-point detection (ruptures), streaming online learning (River), and temporal graph state tracking.
- **Ranking & Storage (`ranking/`, `storage/`)**: Open-loop score calculation and dual-mode storage (SQLite/DuckDB for development mode, PostgreSQL/pgvector readiness for production).
- **Control API (`apps/worker/`)**: REST programmatic control & inspection API endpoints.
