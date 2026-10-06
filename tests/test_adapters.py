import pytest
from core.contracts import Entity, Event, Provenance
from retrieval.sparse.adapters import StoryForestAdapter, SplinkAdapter, RupturesAdapter, RiverAdapter

def test_storyforest_adapter():
    adapter = StoryForestAdapter()
    prov = Provenance(source="test")
    events = [
        Event(event_type="complaint", provenance=prov),
        Event(event_type="complaint", provenance=prov),
        Event(event_type="search", provenance=prov)
    ]
    clusters = adapter.cluster_events(events)
    assert len(clusters["complaint"]) == 2
    assert len(clusters["search"]) == 1

def test_splink_adapter():
    adapter = SplinkAdapter()
    prov = Provenance(source="test")
    entities = [
        Entity(type="Person", canonical_name="Alice", provenance=prov),
        Entity(type="Person", canonical_name="alice", provenance=prov)
    ]
    resolved = adapter.resolve_entities(entities)
    assert len(resolved) == 1

def test_ruptures_adapter():
    adapter = RupturesAdapter()
    signal = [0.1, 0.1, 0.9, 0.9]
    cps = adapter.detect_change_points(signal)
    assert cps == [2]

def test_river_adapter():
    adapter = RiverAdapter()
    adapter.update_query_policy("support software", 1.0)
    assert adapter.weight > 0.5
