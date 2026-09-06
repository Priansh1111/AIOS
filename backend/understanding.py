# TODO (Person A - PLAN_PersonA.md Step 1)
#
# One Groq call, structured JSON output, extracting emotion + intent +
# working_memory + current_goals in a SINGLE call (not four separate ones -
# latency budget matters for the voice interface).
#
# Function signature to implement:
#
#     def understand(text: str, recent_turns: list[str]) -> UnderstandingResult:
#         ...
#
# Test standalone first: 15-20 hand-written example messages (neutral,
# frustrated, joking, vague) with expected emotion/intent, before anything
# downstream depends on this.

from schemas import UnderstandingResult


def understand(text: str, recent_turns: list[str]) -> UnderstandingResult:
    raise NotImplementedError("See PLAN_PersonA.md Step 1")
