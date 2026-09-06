"""
Step 1 of Person B's plan: candidate generation.

Design decision (per PLAN_PersonB.md Step 1): Theory-of-Mind / reaction
prediction is FOLDED into this same call, not a separate Groq round-trip.
The model is asked to reason about how this specific person will react,
then generate candidates accounting for that - one call instead of two,
which matters for the voice-interface latency budget.
"""
from typing import Callable, Optional
from schemas import UnderstandingResult, MemoryEntry, Candidate

SYSTEM_PROMPT = """You are the reasoning core of a personal AI companion. \
You will be given the current understanding of what the user said (emotion, \
intent, goals) and a set of relevant memories about this specific person.

Before writing any reply, privately reason about how THIS person is likely \
to react to different kinds of responses, based on the memories provided \
(especially any 'preference' category memories - these describe how this \
person likes to be responded to).

Then generate exactly 3 distinct candidate replies that differ in APPROACH \
(e.g. one practical/action-oriented, one validating/emotional, one \
curious/clarifying) - not just rephrasings of the same idea.

Respond ONLY with a JSON object of this exact shape, no other text:
{
  "candidates": [
    {
      "reply_text": "...",
      "predicted_reaction": "one line: how this person will likely react to this reply",
      "risk_flag": "one line naming a risk, or null if none"
    }
  ]
}
"""


def _build_user_prompt(understanding: UnderstandingResult, memories: list[MemoryEntry]) -> str:
    memory_lines = "\n".join(
        f"- [{m.category}] {m.content} (relevance {m.relevance_score:.2f})"
        for m in memories
    ) or "(no relevant memories found)"

    goals_lines = ", ".join(understanding.current_goals) or "(none stated)"

    search_terms_line = ", ".join(understanding.search_terms) or "(none - retrieval used raw message)"

    return f"""Emotion: {understanding.emotion}
Intent: {understanding.intent}
Current goals: {goals_lines}
Search terms used for retrieval: {search_terms_line}

Relevant memories about this person:
{memory_lines}

Generate the 3 candidates now."""


def generate_candidates(
    understanding: UnderstandingResult,
    memories: list[MemoryEntry],
    llm_call: Optional[Callable[[str, str], dict]] = None,
) -> list[Candidate]:
    """
    llm_call: injected dependency, signature (system_prompt, user_prompt) -> dict.
    Defaults to the real Groq client. Tests should inject a fake instead
    (see tests/fakes.py) so this runs with no API key or network access.
    """
    if llm_call is None:
        from groq_client import ask_brain_json
        llm_call = ask_brain_json

    user_prompt = _build_user_prompt(understanding, memories)
    result = llm_call(SYSTEM_PROMPT, user_prompt)

    candidates: list[Candidate] = []
    for c in result.get("candidates", []):
        candidates.append(
            Candidate(
                reply_text=c["reply_text"],
                predicted_reaction=c.get("predicted_reaction", ""),
                risk_flag=c.get("risk_flag"),
            )
        )

    if not candidates:
        raise ValueError("LLM returned zero candidates - check prompt/response_format")

    return candidates