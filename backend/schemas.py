"""
Shared contract between Person A (understanding + retrieval) and
Person B (reaction prediction + candidate generation + filtering).

Do not change these shapes without notifying the other person.
"""
from typing import TypedDict, Optional, Literal


class UnderstandingResult(TypedDict):
    emotion: str                # e.g. "frustrated", "neutral", "excited"
    intent: str                 # e.g. "seeking_advice", "venting", "informational", "joking"
    working_memory: list[str]   # last N turns, condensed
    current_goals: list[str]    # pulled from notebook, not re-derived


class MemoryEntry(TypedDict):
    id: int
    category: Literal["goal", "weak_topic", "win", "deadline", "preference"]
    content: str
    relevance_score: float
    last_confirmed_at: str


class Candidate(TypedDict):
    reply_text: str
    predicted_reaction: str     # ToM note: how this person will likely react to this reply
    risk_flag: Optional[str]    # e.g. "may feel dismissive", "too generic" - None if no risk noted


class Popup(TypedDict, total=False):
    type: str
    title: str
    questions: list[dict]


class PendingPermission(TypedDict, total=False):
    id: str
    description: str


class FinalResponse(TypedDict):
    reply_text: str
    speak: bool
    popup: Optional[Popup]
    action: Optional[dict]
    pending_permission: Optional[PendingPermission]
