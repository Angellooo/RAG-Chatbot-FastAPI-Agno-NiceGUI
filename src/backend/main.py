from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
from asyncio import sleep


"""Backend streaming demo for the RAG Chatbot.

This module contains a minimal FastAPI app with a streaming endpoint
used during development. The streaming generator is a placeholder
that simulates token-by-token output; it will later be wired to
an Agno/OpenAI agent pipeline.
"""


# --- Shared Models ---
class ChatRequest(BaseModel):
    """Request model for the chat streaming endpoint.

    Attributes:
        prompt: The user's prompt or question to send to the agent.
        session_id: Optional session identifier to scope conversation history.
    """

    prompt: str
    session_id: str | None = None


class ChatChunk(BaseModel):
    """A single chunk of streamed chat output.

    The schema is intentionally minimal: downstream consumers may
    expand it with metadata such as `is_final`, `speaker`, or `tokens`.
    """

    content: str


class ErrorResponse(BaseModel):
    """Generic error response model.

    Attributes:
        detail: Human-readable error message.
    """

    detail: str


# --- FastAPI App ---
app = FastAPI(title="RAG Chatbot Backend")


# --- Streaming Generator ---
async def stream_response(prompt: str) -> AsyncGenerator[bytes, None]:
    """Asynchronously yield bytes representing streamed output.

    This helper simulates token-by-token (or word-by-word) streaming by
    yielding small byte chunks with a short async sleep between them.

    Parameters
    ----------
    prompt:
        The input prompt to stream a response for. In the real system this
        will be forwarded to an agent which returns a token stream.

    Returns
    -------
    AsyncGenerator[bytes, None]
        An async generator that yields byte payloads consumable by
        `StreamingResponse`.
    """

    words = prompt.split()
    for word in words:
        # yield a single word as bytes (space preserved)
        yield f"{word} ".encode("utf-8")
        # simulate async delay between chunks
        await sleep(0.1)


# --- Endpoint ---
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """HTTP POST endpoint that streams a chat response.

    The endpoint accepts a `ChatRequest` payload and returns an HTTP
    streaming response (plain text) that yields bytes produced by the
    `stream_response` async generator.

    Parameters
    ----------
    request:
        A `ChatRequest` Pydantic model containing the prompt and an optional
        session identifier used to scope conversation history.

    Returns
    -------
    StreamingResponse | ErrorResponse
        A `StreamingResponse` streaming bytes to the client on success, or
        an `ErrorResponse` with an error message if something fails.
    """

    try:
        generator = stream_response(request.prompt)
        return StreamingResponse(generator, media_type="text/plain")
    except Exception as e:
        # Return a JSON error model; FastAPI will serialize this
        return ErrorResponse(detail=str(e))
