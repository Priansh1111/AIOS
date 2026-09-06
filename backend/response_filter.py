# TODO (Person B - PLAN_PersonB.md Step 3) <-- NEXT TO BUILD
#
# Scores each Candidate from response_generator.py against:
#   - emotional fit (does it match predicted_reaction / avoid risk_flag)
#   - goal alignment (understanding.current_goals)
#   - daily_mentions check (don't repeat something already said today -
#     avoids nagging, per PLAN.pdf's existing schema)
#
# Picks the winner, formats into FinalResponse (matches the existing
# /message response shape from PLAN.pdf section 5 - don't invent a new one).
#
# Function signature to implement:
#
#     def filter_and_select(candidates: list[Candidate],
#                            understanding: UnderstandingResult) -> FinalResponse:
#         ...

from schemas import Candidate, UnderstandingResult, FinalResponse


def filter_and_select(candidates: list[Candidate], understanding: UnderstandingResult) -> FinalResponse:
    raise NotImplementedError("See PLAN_PersonB.md Step 3")
