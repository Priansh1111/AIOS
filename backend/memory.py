# TODO (from PLAN.pdf Section 6 - not scoped to Person A or B specifically,
# but Person A's embeddings.py + retrieval.py depend on this existing first)
#
# SQLite setup + read/write helpers for the schema below, plus the nightly
# reflection job (owned by Team 2 - see aios-companion memory notes).
#
# CREATE TABLE notebook (
#     id INTEGER PRIMARY KEY,
#     category TEXT,          -- 'goal', 'weak_topic', 'win', 'deadline', 'preference'
#     content TEXT,
#     created_at TEXT,
#     last_confirmed_at TEXT
# );
#
# CREATE TABLE daily_mentions (
#     id INTEGER PRIMARY KEY,
#     date TEXT,
#     topic TEXT
# );
#
# CREATE TABLE conversation_log (
#     id INTEGER PRIMARY KEY,
#     timestamp TEXT,
#     role TEXT,               -- 'user' or 'agent'
#     text TEXT
# );
#
# CREATE TABLE action_log (
#     id INTEGER PRIMARY KEY,
#     timestamp TEXT,
#     description TEXT,
#     approved INTEGER,
#     executed INTEGER
# );

def log_conversation_turn(user_text: str, agent_text: str) -> None:
    raise NotImplementedError("See PLAN.pdf Section 6")


def get_notebook_entries() -> list[dict]:
    raise NotImplementedError("See PLAN.pdf Section 6")
