"""
Thin wrapper around Groq calls. Isolate model names/params here so
response_generator.py never talks to the API directly - makes it
trivial to swap in a fake for testing (see tests/fakes.py).
"""
import json
import os

MODEL = "llama-3.3-70b-versatile"


def ask_brain_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Calls Groq with structured JSON output. Returns parsed dict.
    Requires GROQ_API_KEY in environment.
    """
    from groq import Groq  # imported lazily so tests don't need the package installed

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not set. For local testing without a key, "
            "inject a fake llm_call into response_generator.generate_candidates() instead."
        )

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.8,  # some variation across candidates is desirable here
    )
    return json.loads(completion.choices[0].message.content)
