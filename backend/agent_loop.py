# TODO (SHARED - wires Person A's output into Person B's input)
#
# Sequence once all pieces exist:
#
#   understanding = understanding.understand(text, recent_turns)
#   memories       = retrieval.retrieve(text, understanding)
#   candidates     = response_generator.generate_candidates(understanding, memories)
#   final          = response_filter.filter_and_select(candidates, understanding)
#   memory.log_conversation_turn(text, final["reply_text"])   # the missing
#                                                              # "+ conversation_log"
#                                                              # box from the diagram
#   return final
#
# This file is the natural owner of the conversation_log write - it's the
# last point where both the incoming message and the final response are
# in scope together.
#
# Until Person A's understanding.py / retrieval.py are real, build and test
# this against tests/fakes.py-style fake inputs, same as response_generator.py's
# tests do.

from schemas import FinalResponse


def handle_message(text: str, recent_turns: list[str]) -> FinalResponse:
    raise NotImplementedError("Wire together once understanding.py, retrieval.py, response_filter.py exist")
