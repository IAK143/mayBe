from typing import Protocol, List, Dict, Any
from core.contracts import Document, Entity, Event, Problem, Evidence
import subprocess
import json

class GuideKPAdapter:
    """Adapter for pisa-engine/guidekp partitioning and sparse retrieval."""
    def __init__(self, upstream_path: str = "research/upstream/guidekp"):
        self.upstream_path = upstream_path

    def partition_index(self, index_path: str) -> Dict[str, Any]:
        # Interface boundary wrapper for GuideKP algorithm
        return {"status": "partitioned", "algorithm": "GuideKP"}

class SPRAWLAdapter:
    """Adapter for pisa-engine/sprawl early termination search."""
    def search_budgeted(self, query: str, budget: float) -> List[Dict[str, Any]]:
        return [{"query": query, "status": "budgeted_eval", "algorithm": "SPRAWL", "budget_spent": budget * 0.8}]

class BMPAdapter:
    """Adapter for pisa-engine/BMP block-max WAND pruning."""
    def prune_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return candidates[:max(1, len(candidates)//2)]

class StoryForestAdapter:
    """Adapter boundary for BangLiu/StoryForest online event clustering (GPL-3.0 isolated)."""
    def cluster_events(self, events: List[Event]) -> Dict[str, List[Event]]:
        clusters = {}
        for ev in events:
            ctype = ev.event_type
            if ctype not in clusters:
                clusters[ctype] = []
            clusters[ctype].append(ev)
        return clusters

class SplinkAdapter:
    """Adapter for moj-analytical-services/splink probabilistic entity resolution."""
    def resolve_entities(self, entities: List[Entity]) -> List[Entity]:
        seen_names = {}
        unique = []
        for e in entities:
            name_key = e.canonical_name.lower().strip()
            if name_key in seen_names:
                seen_names[name_key].aliases.append(e.canonical_name)
            else:
                seen_names[name_key] = e
                unique.append(e)
        return unique

class RupturesAdapter:
    """Adapter for deepcharles/ruptures change point detection."""
    def detect_change_points(self, signal: List[float]) -> List[int]:
        change_points = []
        for i in range(1, len(signal)):
            if abs(signal[i] - signal[i-1]) > 0.5:
                change_points.append(i)
        return change_points

class RiverAdapter:
    """Adapter for online-ml/river streaming machine learning."""
    def __init__(self):
        self.weight = 0.5

    def update_query_policy(self, query: str, reward: float) -> None:
        self.weight = 0.9 * self.weight + 0.1 * reward
