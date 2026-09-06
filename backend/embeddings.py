# TODO (Person A - PLAN_PersonA.md Step 2)
#
# Wrap sentence-transformers (all-MiniLM-L6-v2) for LOCAL/CPU embeddings -
# no per-call API cost, keeps Groq quota and retrieval latency down.
#
# Called on:
#   (a) every new notebook row write (memory.py should call this on insert)
#   (b) every incoming retrieval query (retrieval.py calls this before search)
#
# Function signature to implement:
#
#     def embed(text: str) -> list[float]:
#         ...

def embed(text: str) -> list[float]:
    raise NotImplementedError("See PLAN_PersonA.md Step 2")
