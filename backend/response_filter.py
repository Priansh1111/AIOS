"""
Step 3 of Person B's plan: response filtering.

Scores each Candidate from response_generator.py against:
  - risk (does the candidate itself flag a likely-bad reaction)
  - goal alignment (does it engage with what the understanding layer says
    the user actually cares about right now)
  - daily_mentions (don't repeat a topic already surfaced today - avoids
    nagging, per PLAN.pdf's existing schema)

Picks the highest-scoring candidate, formats it into FinalResponse -
the same shape as the existing /message response from PLAN.pdf section 5.

NOTE on scoring: this is intentionally a simple, transparent heuristic,
not a second LLM call. Per PLAN_PersonB.md Step 4, the real test of
whether filtering is worth its cost is the human-graded eval comparing
filtered output against the unfiltered first candidate - don't over-build
the scoring function before that eval says it's needed.
"""
from typing import Optional
from schemas import Candidate, UnderstandingResult, FinalResponse

RISK_PENALTY = 0.5
DAILY_MENTION_PENALTY = 1.0
GOAL_ALIGNMENT_BONUS = 0.2


def _mentions_goal(reply_text: str, goals: list[str]) -> bool:
    lowered = reply_text.lower()
    return any(goal.lower() in lowered or _word_overlap(goal, reply_text) for goal in goals)


def _word_overlap(goal: str, reply_text: str) -> bool:
    goal_words = set(goal.lower().split())
    reply_words = set(reply_text.lower().split())
    return len(goal_words & reply_words) > 0


def _already_mentioned(reply_text: str, already_mentioned_today: list[str]) -> bool:
    lowered = reply_text.lower()
    return any(topic.lower() in lowered for topic in already_mentioned_today)


def _score(candidate: Candidate, understanding: UnderstandingResult, already_mentioned_today: list[str]) -> float:
    score = 1.0

    if candidate.risk_flag:
        score -= RISK_PENALTY

    if _already_mentioned(candidate.reply_text, already_mentioned_today):
        score -= DAILY_MENTION_PENALTY

    if _mentions_goal(candidate.reply_text, understanding.current_goals):
        score += GOAL_ALIGNMENT_BONUS

    return score


def filter_and_select(
    candidates: list[Candidate],
    understanding: UnderstandingResult,
    already_mentioned_today: Optional[list[str]] = None,
) -> FinalResponse:
    """
    already_mentioned_today: topics already surfaced today, from
    memory.py's daily_mentions table. Optional so this is testable before
    memory.py is real - defaults to "nothing mentioned yet."
    """
    if already_mentioned_today is None:
        already_mentioned_today = []

    if not candidates:
        raise ValueError("filter_and_select() received zero candidates - nothing to select from")

    scored = [(c, _score(c, understanding, already_mentioned_today)) for c in candidates]
    # stable sort: on a tie, earlier candidate in the list wins - this
    # respects response_generator.py's own ordering as a tiebreak signal
    winner, _ = max(scored, key=lambda pair: pair[1])

    return FinalResponse(
        reply_text=winner.reply_text,
        speak=True,
        popup=None,
        action=None,
        pending_permission=None,
    )