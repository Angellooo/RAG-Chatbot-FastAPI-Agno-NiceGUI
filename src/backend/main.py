from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
import asyncio
from src.agent.agent import create_agent


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
    is_final: bool = False


class ErrorResponse(BaseModel):
    """Generic error response model.

    Attributes:
        detail: Human-readable error message.
    """

    detail: str


# --- FastAPI App ---
app = FastAPI(title="RAG Chatbot Backend")


# --- Streaming Generator ---
async def stream_response(prompt: str, session_id: str | None):
    """
        Async generator that streams chat response chunks as newline-delimited JSON.

        This function wraps the agent's synchronous streaming output and yields each
        chunk as a serialized ChatChunk JSON object. It is designed for use with FastAPI's
        StreamingResponse to provide real-time, chunked output to the client.

        Parameters
        ----------
        prompt : str
            The user's prompt or question to send to the agent.
        session_id : str | None
            Optional session identifier to scope conversation history.

        Yields
        ------
        bytes
            Each yielded value is a newline-delimited JSON-encoded ChatChunk.
    """
    agent = create_agent(session_id)

    def sync_gen():
        for chunk in agent.run(prompt, stream=True):
            # Defensive extraction: prefer .content, fallback to .text or str(chunk)
            text = getattr(chunk, "content", None) or getattr(chunk, "text", None) or str(chunk)
            if text:
                # Wrap each chunk in ChatChunk and yield as JSON
                chat_chunk = ChatChunk(content=text, is_final=False)
                yield chat_chunk.json().encode("utf-8") + b"\n"
        # After all chunks, send a final chunk
        yield ChatChunk(content="", is_final=True).json().encode("utf-8") + b"\n"

    for chunk in await asyncio.to_thread(lambda: list(sync_gen())):
        yield chunk


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
        generator = stream_response(request.prompt, request.session_id)
        # Stream as NDJSON (newline-delimited JSON)
        return StreamingResponse(generator, media_type="application/x-ndjson")
    except Exception as e:
        return ErrorResponse(detail=str(e))
