# TODO (Person A - PLAN_PersonA.md Step 3)
#
# Vector search (sqlite-vec, or plain numpy cosine similarity if row count
# stays low) against the notebook table, re-ranked by:
#   semantic similarity + recency (last_confirmed_at) + category weight
# (a 'goal' should generally outrank a 'win' for most queries).
#
# Cap output at a fixed token/count budget - don't dump the whole notebook.
#
# Function signature to implement:
#
#     def retrieve(query: str, understanding: UnderstandingResult) -> list[MemoryEntry]:
#         ...
#
# Test standalone first: seed 30-50 fake notebook rows (mix of goals/
# weak_topics/wins, some old, some recent, some contradictory) and check
# by hand that the right entries surface and irrelevant ones don't -
# before this needs to talk to understanding.py at all.

from schemas import UnderstandingResult, MemoryEntry


def retrieve(query: str, understanding: UnderstandingResult) -> list[MemoryEntry]:
    raise NotImplementedError("See PLAN_PersonA.md Step 3")
