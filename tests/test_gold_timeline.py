import pytest
import asyncio
from tests.fixtures.gold_timeline import generate_gold_timeline_fixtures
from intelligence.event_extraction import DEEIAReference
from temporal.state_inference import ProblemStateInferencer
from ingestion.extraction import LocalDeduplicator

@pytest.mark.e2e
def test_gold_timeline_synthetic_progression():
    fixtures = generate_gold_timeline_fixtures()
    dedup = LocalDeduplicator()
    extractor = DEEIAReference()
    inferencer = ProblemStateInferencer()

    accumulated_events = []

    # Store inferred problems per day
    results = {}

    for day, doc in fixtures:
        assert not dedup.is_duplicate(doc.extracted_text)
        events = extractor.extract_events(doc)
        accumulated_events.extend(events)

        problem = inferencer.infer_state(accumulated_events, doc.document_id, doc.provenance)
        results[day] = problem

    # Day 1: ACTIVE_PROBLEM should be high
    p1 = results[1]
    assert p1.state.ACTIVE_PROBLEM > 0.0

    # Day 3: SEARCHING_FOR_SOLUTION should emerge
    p3 = results[3]
    assert p3.state.SEARCHING_FOR_SOLUTION > 0.0

    # Day 7: FAILED_SOLUTION / FAILED state should increase
    p7 = results[7]
    assert p7.state.FAILED > 0.0 or p7.resolution_state.FAILED_SOLUTION > 0.0

    # Day 10: OPEN_LOOP score should be peak / high
    p10 = results[10]
    assert p10.open_loop_score > 0.0

    # Day 12: RESOLVED should dominate and open loop drops
    p12 = results[12]
    assert p12.state.RESOLVED > 0.0
    assert p12.resolution_state.RESOLVED > 0.0
    assert p12.open_loop_score == 0.0
