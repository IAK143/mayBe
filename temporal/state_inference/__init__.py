from typing import List, Dict
from core.contracts import Event, Problem, Evidence, ProblemStateDistribution, ResolutionStateDistribution, Provenance

class ProblemStateInferencer:
    """Probabilistic State Inferencer updating P(Zt | O1:t) and P(Rt | E1:t)."""

    def infer_state(self, events: List[Event], doc_id: str, prov: Provenance) -> Problem:
        state = ProblemStateDistribution()
        resolution = ResolutionStateDistribution()

        symptoms = []
        causes = []
        attempted_solutions = []
        evidence_list = []

        for ev in events:
            ev_type = ev.event_type

            if ev_type == "complaint":
                state.ACTIVE_PROBLEM += 0.5
                symptoms.append(ev.arguments.get("raw_trigger_text", ""))
                evidence_list.append(Evidence(
                    source_document=doc_id,
                    extracted_span=ev.arguments.get("raw_trigger_text", ""),
                    evidence_type="supports",
                    supports=["ACTIVE_PROBLEM"],
                    provenance=prov
                ))
            elif ev_type == "question":
                state.SEARCHING_FOR_SOLUTION += 0.6
                evidence_list.append(Evidence(
                    source_document=doc_id,
                    extracted_span=ev.arguments.get("raw_trigger_text", ""),
                    evidence_type="supports",
                    supports=["SEARCHING_FOR_SOLUTION"],
                    provenance=prov
                ))
            elif ev_type == "attempt":
                state.INVESTIGATING += 0.4
                attempted_solutions.append(ev.arguments.get("raw_trigger_text", ""))
            elif ev_type == "failure":
                state.FAILED += 0.7
                resolution.FAILED_SOLUTION += 0.6
                resolution.UNRESOLVED += 0.3
                evidence_list.append(Evidence(
                    source_document=doc_id,
                    extracted_span=ev.arguments.get("raw_trigger_text", ""),
                    evidence_type="supports",
                    supports=["FAILED_SOLUTION"],
                    provenance=prov
                ))
            elif ev_type == "search":
                state.SEARCHING_FOR_SOLUTION += 0.7
                resolution.UNRESOLVED += 0.4
            elif ev_type == "resolution":
                state.RESOLVED += 0.9
                resolution.RESOLVED += 0.9
                resolution.UNRESOLVED = 0.0
                evidence_list.append(Evidence(
                    source_document=doc_id,
                    extracted_span=ev.arguments.get("raw_trigger_text", ""),
                    evidence_type="supports",
                    supports=["RESOLVED"],
                    provenance=prov
                ))

        # Normalize state probabilities
        total_st = sum([
            state.UNKNOWN, state.LATENT_FRICTION, state.ACTIVE_PROBLEM, state.INVESTIGATING,
            state.SEARCHING_FOR_SOLUTION, state.COMPARING_SOLUTIONS, state.PROCUREMENT,
            state.RESOLVED, state.PARTIALLY_RESOLVED, state.FAILED, state.ABANDONED,
            state.RECURRED, state.ESCALATING
        ])
        if total_st > 0:
            state.ACTIVE_PROBLEM /= total_st
            state.SEARCHING_FOR_SOLUTION /= total_st
            state.INVESTIGATING /= total_st
            state.FAILED /= total_st
            state.RESOLVED /= total_st

        # Compute Open Loop score
        open_loop = (state.ACTIVE_PROBLEM + state.SEARCHING_FOR_SOLUTION + state.FAILED) * resolution.UNRESOLVED

        return Problem(
            canonical_description="Inferred Problem from Event Stream",
            semantic_cluster="general_cluster",
            symptoms=symptoms,
            attempted_solutions=attempted_solutions,
            evidence=evidence_list,
            state=state,
            resolution_state=resolution,
            open_loop_score=open_loop
        )
