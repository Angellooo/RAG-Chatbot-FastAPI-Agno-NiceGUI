from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.shared.config import settings

def create_agent(session_id: str | None = None) -> Agent:
    """
    Create and configure an Agno agent with OpenAI backend.
    Uses session_id to persist conversation history.
    """
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in environment")

    # Configure the OpenAI model
    model = OpenAIChat(
        id="gpt-4.1-nano",   # lightweight model for streaming
        api_key=settings.openai_api_key,
    )

    # Create agent with session_id (Agno manages memory internally)
    agent = Agent(
        model=model,
        session_id=session_id or "default",
        add_history_to_context=True,  # ensures past messages are included
        name="RAGChatbotAgent",
    )
    return agent
