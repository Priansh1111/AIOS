"""
Shared orchestrator - wires Person A's output into Person B's input,
branching on UnderstandingResult.response_mode to skip stages that a
trivial or task-continuation turn doesn't need.

TODO once real pieces exist (still stubs as of this file):
  understanding.understand()   - Person A
  retrieval.retrieve()          - Person A
  response_generator.generate_candidates()  - Person B, DONE
  response_filter.filter_and_select()        - Person B, DONE
  memory.log_conversation_turn()              - not yet built

This file is the natural owner of the conversation_log write (per the
plan's earlier note) - it's the last point where both the incoming
message and the final response are in scope together.
"""
from schemas import FinalResponse

# these imports will work once Person A's files are real; left here so
# the branching logic below is complete and reads correctly today
import understanding
import retrieval
import response_generator
import response_filter


def handle_message(text: str, recent_turns: list[str]) -> FinalResponse:
    # Understanding ALWAYS runs - it's the only stage cheap enough to run
    # on every turn, and it's the one that produces response_mode itself.
    result = understanding.understand(text, recent_turns)

    if result.response_mode == "passthrough":
        # Trivial acknowledgment - skip Retrieval, Candidate Generation,
        # and Filtering entirely. One cheap reply, no reasoning overhead.
        return FinalResponse(
            reply_text=_cheap_reply(text),
            speak=True,
            popup=None,
            action=None,
            pending_permission=None,
        )

    if result.response_mode == "task_continuation":
        # Resuming a paused task (e.g. "continue" mid-code-generation).
        # Skip the EMOTIONAL reasoning stages (ToM / candidate framing
        # doesn't make sense for "keep writing this function") but still
        # generate a real answer, using working_memory for what's being
        # resumed. No candidate generation, no filtering - there's no
        # meaningful "practical vs validating vs curious" framing here.
        return FinalResponse(
            reply_text=_continue_task(result),
            speak=False,  # code/task output - probably shouldn't be spoken aloud
            popup=None,
            action=None,
            pending_permission=None,
        )

    # response_mode == "full_pipeline" (also the safe fallback for any
    # unexpected/uncertain classification - see schemas.py note)
    memories = retrieval.retrieve(text, result)
    candidates = response_generator.generate_candidates(result, memories)
    final = response_filter.filter_and_select(candidates, result)

    # TODO: memory.log_conversation_turn(text, final.reply_text)
    return final


def _cheap_reply(text: str) -> str:
    raise NotImplementedError(
        "Trivial-turn reply - can be a tiny separate Groq call or even a "
        "hardcoded acknowledgment set, deliberately NOT the full candidate "
        "generation pipeline."
    )


def _continue_task(result) -> str:
    raise NotImplementedError(
        "Resume the paused task using result.working_memory - no ToM/candidate "
        "framing needed here, this is a plain completion, not a conversational reply."
    )