import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from schemas import UnderstandingResult, MemoryEntry
from response_generator import generate_candidates
from tests.fakes import fake_llm_call


def make_understanding(emotion="frustrated", intent="seeking_advice") -> UnderstandingResult:
    return UnderstandingResult(
        emotion=emotion,
        intent=intent,
        working_memory=["I keep messing up binary tree traversal"],
        current_goals=["clear placements by Dec"],
    )


def make_memories() -> list[MemoryEntry]:
    return [
        MemoryEntry(
            id=1,
            category="weak_topic",
            content="tree traversal",
            relevance_score=0.91,
            last_confirmed_at="2026-09-04",
        ),
        MemoryEntry(
            id=2,
            category="preference",
            content="prefers practical next steps over sympathy",
            relevance_score=0.85,
            last_confirmed_at="2026-08-20",
        ),
    ]


def test_generates_three_distinct_candidates():
    understanding = make_understanding()
    memories = make_memories()

    candidates = generate_candidates(understanding, memories, llm_call=fake_llm_call)

    assert len(candidates) == 3, "should generate exactly 3 candidates"
    reply_texts = [c["reply_text"] for c in candidates]
    assert len(set(reply_texts)) == 3, "candidates should be textually distinct"


def test_each_candidate_has_predicted_reaction():
    understanding = make_understanding()
    memories = make_memories()

    candidates = generate_candidates(understanding, memories, llm_call=fake_llm_call)

    for c in candidates:
        assert c["predicted_reaction"], "every candidate must carry a ToM prediction (folded-in, not a separate call)"


def test_risk_flag_present_when_relevant():
    understanding = make_understanding()
    memories = make_memories()

    candidates = generate_candidates(understanding, memories, llm_call=fake_llm_call)

    flagged = [c for c in candidates if c["risk_flag"]]
    assert len(flagged) >= 1, "expected at least one candidate to carry a risk flag in this scenario"


def test_neutral_scenario_still_produces_three():
    understanding = make_understanding(emotion="neutral", intent="informational")
    candidates = generate_candidates(understanding, [], llm_call=fake_llm_call)
    assert len(candidates) == 3


def test_raises_on_empty_candidates():
    def broken_llm_call(system_prompt, user_prompt):
        return {"candidates": []}

    understanding = make_understanding()
    try:
        generate_candidates(understanding, [], llm_call=broken_llm_call)
        assert False, "should have raised ValueError on zero candidates"
    except ValueError:
        pass
