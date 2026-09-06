# TODO (from PLAN.pdf Section 5 - the six-endpoint API contract)
#
# POST /listen                  - audio -> transcribed text
# POST /message                  - main endpoint, calls agent_loop.handle_message
# POST /permission/respond        - approve/deny a pending action
# POST /screenshot/analyze         - screenshot -> description
# GET  /memory/snapshot             - debug: inspect current notebook state
# WS   /state                        - pushes listening/thinking/speaking/idle

from fastapi import FastAPI

app = FastAPI()


@app.post("/message")
def message(payload: dict):
    raise NotImplementedError("Call agent_loop.handle_message(payload['text'], recent_turns)")
