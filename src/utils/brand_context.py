"""Brand context utility for loading and processing the brand guide."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import SecretStr

# Load environment variables
load_dotenv()


def _read_brand_guide() -> str:
    """Read the brand guide markdown file."""
    guide_path = Path(__file__).parent.parent.parent / "docs" / "brand_guide.md"
    if not guide_path.exists():
        raise FileNotFoundError(f"Brand guide not found at {guide_path}")
    
    with open(guide_path, "r", encoding="utf-8") as f:
        return f.read()


def _count_tokens(text: str) -> int:
    """Rough token count estimation (4 chars per token)."""
    return len(text) // 4


def _summarize_brand_guide(content: str, max_tokens: int) -> str:
    """Summarize brand guide to fit within token limit."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
    )
    
    system_prompt = f"""You are a brand strategist tasked with summarizing a brand guide.
    
Your task is to create a concise, comprehensive summary of the brand guide that captures:
- Core brand identity and values
- Target audience and positioning
- Product portfolio focus
- Brand personality and tone
- Key differentiators

The summary must be {max_tokens} tokens or less while preserving all essential brand information.
Focus on actionable details that will guide product and content generation."""

    user_prompt = f"""Please summarize this brand guide to {max_tokens} tokens or less:

{content}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    
    response = llm.invoke(messages)
    return str(response.content)  # type: ignore


@lru_cache(maxsize=1)
def get_brand_context(max_tokens: Optional[int] = 300) -> str:
    """Get brand context from the guide, optionally summarized.
    
    Args:
        max_tokens: Maximum tokens for the context. If None, returns full guide.
                   If guide exceeds this limit, it will be summarized.
    
    Returns:
        Brand context string suitable for inclusion in prompts.
    """
    content = _read_brand_guide()
    
    if max_tokens is None:
        return content
    
    token_count = _count_tokens(content)
    
    if token_count <= max_tokens:
        return content
    
    return _summarize_brand_guide(content, max_tokens) 