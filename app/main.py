from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.assistant import answer


app = FastAPI(title="Drug Discovery Research Assistant", version="1.0.0")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(response=answer(request.message))


@app.get("/", response_class=HTMLResponse)
def report() -> str:
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Drug Discovery AI Evaluation</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.55; margin: 40px auto; max-width: 860px; color: #202124; }
          h1, h2 { line-height: 1.2; }
          code, pre { background: #f5f7f9; border-radius: 4px; padding: 2px 4px; }
          section { margin-top: 28px; }
          .note { border-left: 4px solid #3858e9; padding-left: 14px; color: #333; }
        </style>
      </head>
      <body>
        <h1>Drug Discovery Research Assistant Evaluation</h1>
        <p class="note">
          This endpoint supports the Gates Foundation AI Fellows India technical assignment. It exposes
          <code>POST /chat</code> for conversational evaluation and this page as a live summary endpoint.
        </p>
        <section>
          <h2>Evaluation Focus</h2>
          <p>
            The test suite evaluates biomedical factuality, uncertainty handling, safety, evidence reasoning,
            prompt-injection resistance, user experience, and multilingual accessibility for India-context deployment.
          </p>
        </section>
        <section>
          <h2>Endpoint Contract</h2>
          <pre>POST /chat
Content-Type: application/json

{ "message": "What is target identification in drug discovery?" }</pre>
        </section>
        <section>
          <h2>Limitations</h2>
          <p>
            This is a deterministic evaluation target, not a production biomedical model. Its purpose is to make
            evaluation behavior reproducible while demonstrating how a domain-relevant conversational AI system
            should be tested before real deployment.
          </p>
        </section>
      </body>
    </html>
    """

