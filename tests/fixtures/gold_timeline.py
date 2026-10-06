from datetime import datetime, timezone, timedelta
from typing import List, Tuple
from core.contracts import Document, Provenance

def generate_gold_timeline_fixtures() -> List[Tuple[int, Document]]:
    """
    Synthetic 12-Day World Timeline Fixture:
    Day 1: complaint ("our support backlog doubled, calls missed")
    Day 3: asks for recommendation ("looking for recommendation for support software")
    Day 5: tries solution A ("tries Solution A for handling support")
    Day 7: solution A fails ("Solution A failed to handle call volume")
    Day 10: searches for alternative ("searches for alternative solution")
    Day 12: solution B works ("Solution B fixed it and solved the issue")
    """
    base_time = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
    events_raw = [
        (1, "our support backlog doubled, calls missed"),
        (3, "looking for recommendation for support software"),
        (5, "tries Solution A for handling support"),
        (7, "Solution A failed to handle call volume"),
        (10, "searches for alternative solution"),
        (12, "Solution B fixed it and solved the issue")
    ]

    fixtures = []
    for day, text in events_raw:
        dt = base_time + timedelta(days=day-1)
        prov = Provenance(source="synthetic_gold_fixture", observed_at=dt)
        doc = Document(
            source="synthetic",
            canonical_url=f"http://example.com/day_{day}",
            timestamp=dt,
            author_reference="Person A",
            raw_text=text,
            extracted_text=text,
            provenance=prov
        )
        fixtures.append((day, doc))

    return fixtures
