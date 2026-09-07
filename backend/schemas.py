"""
schemas.py — the contract between Person A (understanding + retrieval)
and Person B (reaction prediction + candidate generation + filtering).

RULE: once both of you agree on this file, don't change it unilaterally.
If you need a new field mid-build, message the other person before you
push — this file is the seam the whole parallel-build plan depends on.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


# ---------------------------------------------------------------------
# Shared vocabularies. Pin these down TOGETHER on Day 1 — these are the
# exact strings both of your code will compare against, so a typo-level
# mismatch here (e.g. A writes "Frustrated", B checks for "frustrated")
# is the single easiest way to quietly break the pipeline.
#
# NOTE: kept as plain str, not Literal[...], on purpose. A strict Literal
# throws a hard validation error the moment the LLM emits anything
# outside the enumerated set - and LLMs don't always perfectly respect a
# closed vocabulary. Failing soft (unexpected value passes through,
# downstream code treats unknowns as "neutral"/"informational") is safer
# for a live voice interface than crashing mid-conversation. Use these
# lists in your PROMPT to bias the model, not as a runtime hard-gate.
# ---------------------------------------------------------------------

KNOWN_EMOTIONS = ["frustrated", "neutral", "excited", "anxious", "confident", "sad", "joking"]
KNOWN_INTENTS = ["seeking_advice", "seeking_comfort", "venting", "informational", "joking"]
Category = Literal["goal", "weak_topic", "win", "deadline", "preference"]


# ---------------------------------------------------------------------
# Person A produces this. Person B consumes it. Nothing else.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Routing flag. Decides which downstream stages agent_loop.py runs.
# Kept as a strict Literal (unlike emotion/intent above) because this one
# drives actual branching logic, not just prompt framing - an unexpected
# value here needs to fail loud, not silently pass through. The default
# fallback in understanding.py's prompt MUST be "full_pipeline" whenever
# the model is uncertain - a wrong guess toward "passthrough" risks
# giving someone a cheap, un-reasoned-about reply on a message that
# actually needed the full emotional pipeline. Cost savings are not
# worth that failure mode.
#
#   full_pipeline    - normal conversational turn, needs Retrieval +
#                       Candidate Generation + Filtering (default/fallback)
#   passthrough       - trivial acknowledgment ("ok thanks", "lol") -
#                        skip everything past Understanding, one cheap reply
#   task_continuation - resuming a paused task (code, a list, anything
#                        with in-progress state, e.g. user says "continue").
#                        Skips the EMOTIONAL reasoning stages, but still
#                        needs working_memory - which this same call
#                        already receives - to know what's being resumed.
# ---------------------------------------------------------------------
ResponseMode = Literal["full_pipeline", "passthrough", "task_continuation"]

class UnderstandingResult(BaseModel):
    emotion: str          # should be one of KNOWN_EMOTIONS, but not hard-enforced - see note above
    intent: str           # should be one of KNOWN_INTENTS, but not hard-enforced - see note above
    working_memory: list[str]
    response_mode: ResponseMode = "full_pipeline"
    # Routing flag classified from working_memory + the current message in
    # THIS SAME Understanding call - no separate history-lookup step
    # needed, since working_memory already carries the recent turns this
    # classification depends on (e.g. seeing an in-progress code block to
    # correctly classify "continue" as task_continuation).
    # last N turns of this session, condensed - cheap, no retrieval needed

    current_goals: list[str]
    # pulled from the notebook by A, not re-derived by B

    search_terms: list[str] = Field(default_factory=list)
    # Expanded query terms (e.g. "exam, failure, academic stress" instead
    # of the raw message "I failed my exam") so retrieval.py has
    # something real to search with. Generated in the SAME Groq call as
    # emotion/intent - costs nothing extra, solves the "raw message
    # retrieves nothing useful" gap.


# ---------------------------------------------------------------------
# Person A produces a list of these. Person B consumes them. Nothing else.
# ---------------------------------------------------------------------

class MemoryEntry(BaseModel):
    id: int
    category: Category
    content: str
    relevance_score: float
    last_confirmed_at: str   # ISO string - kept as str, not datetime, to match
                              # what SQLite actually round-trips without extra parsing

    supersedes_id: Optional[int] = None
    # Team 2's reflection layer is append-only (never overwrites - inserts
    # a new row on "update/supersede" instead). This field is how that
    # history stays usable: if a row updates an older one, it points back
    # to it, so response_generator.py can say "you were weak at X, now
    # improving" instead of just "weak at X" - the delta-awareness the
    # memory layer is supposed to deliver.


# ---------------------------------------------------------------------
# Person B produces a list of these. filter_and_select() consumes them.
# RESTORED from the original draft - do not drop this. response_generator.py
# (already built and tested) returns list[Candidate]; removing this model
# breaks working code.
# ---------------------------------------------------------------------

class Candidate(BaseModel):
    reply_text: str
    predicted_reaction: str     # ToM note: how this person will likely react to this reply
    risk_flag: Optional[str] = None   # e.g. "may feel dismissive", "too generic" - None if no risk noted


# ---------------------------------------------------------------------
# Unchanged shape - already matches the /message response from PLAN.pdf
# section 5. Kept typed (not collapsed to dict) since you already have
# the sub-models; costs nothing to keep the extra clarity.
# ---------------------------------------------------------------------

class Popup(BaseModel):
    type: str
    title: str
    questions: list[dict] = Field(default_factory=list)


class PendingPermission(BaseModel):
    id: str
    description: str


class FinalResponse(BaseModel):
    reply_text: str
    speak: bool
    popup: Optional[Popup] = None
    action: Optional[dict] = None
    pending_permission: Optional[PendingPermission] = None