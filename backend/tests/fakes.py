"""
Fake llm_call injectable into generate_candidates() so Person B can test
and iterate on prompt/parsing logic without a Groq API key or network access.
Swap for the real groq_client.ask_brain_json once a key is available -
the function signature is identical, so nothing else needs to change.
"""


def fake_llm_call(system_prompt: str, user_prompt: str) -> dict:
    """
    Returns a canned, schema-correct response so tests can verify
    generate_candidates() parses and shapes output correctly.
    Reads the user_prompt a little so the fake feels responsive to input,
    but this is NOT a real model - only for wiring/shape tests.
    """
    frustrated = "frustrated" in user_prompt.lower()

    if frustrated:
        return {
            "candidates": [
                {
                    "reply_text": "Want to try a quick 3-question refresher on this before you keep going?",
                    "predicted_reaction": "Likely receptive - this person prefers practical next steps over sympathy",
                    "risk_flag": None,
                },
                {
                    "reply_text": "That sounds really frustrating - you've been putting in a lot of work on this.",
                    "predicted_reaction": "May feel slightly patronizing given this person's stated preference for directness",
                    "risk_flag": "too generic / may feel dismissive",
                },
                {
                    "reply_text": "What part of it is tripping you up specifically?",
                    "predicted_reaction": "Likely to engage, this person tends to respond well to being asked rather than told",
                    "risk_flag": None,
                },
            ]
        }

    return {
        "candidates": [
            {
                "reply_text": "Got it, noted.",
                "predicted_reaction": "Neutral acknowledgement, low risk either way",
                "risk_flag": None,
            },
            {
                "reply_text": "Nice - anything else on your mind?",
                "predicted_reaction": "Likely fine, keeps door open without being pushy",
                "risk_flag": None,
            },
            {
                "reply_text": "Cool. Want me to remember that for later?",
                "predicted_reaction": "Neutral, may be unnecessary if not clearly a fact worth storing",
                "risk_flag": "may feel over-eager to log everything",
            },
        ]
    }
