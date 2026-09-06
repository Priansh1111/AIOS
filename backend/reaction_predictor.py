# TODO (Person B - PLAN_PersonB.md Step 2)
#
# By default, ToM reasoning is FOLDED INTO response_generator.py (each
# Candidate already carries a predicted_reaction field - see Step 1).
#
# Only build this as a real separate module - and a separate Groq call -
# if the human-graded eval in Step 4 shows the folded-in version isn't
# good enough. Until then, this can stay a thin pass-through.
#
# Function signature if/when split out for real:
#
#     def predict_reaction(understanding: UnderstandingResult,
#                           memories: list[MemoryEntry],
#                           candidate_text: str) -> str:
#         ...

from schemas import UnderstandingResult, MemoryEntry


def predict_reaction(understanding: UnderstandingResult, memories: list[MemoryEntry], candidate_text: str) -> str:
    raise NotImplementedError(
        "Folded into response_generator.py by default - see PLAN_PersonB.md Step 2. "
        "Only implement this for real if the eval in Step 4 says the folded-in version isn't enough."
    )
