"""Collection generation module."""

import json
import os
from typing import List

from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.schema import Collection
from src.prompts import COLLECTION_GENERATION_PROMPT


class CollectionGenerator:
    """Generates collection profiles using OpenAI and LangChain."""
    
    def __init__(self, temperature: float = 0.7):
        """Initialize the collection generator.
        
        Args:
            temperature: Temperature for generation (0.0-1.0)
        """
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            temperature=temperature,
            api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
        )
    
    async def generate_collections(
        self, 
        brand_context: str, 
        brand_ids: List[str], 
        count: int = 20
    ) -> List[Collection]:
        """Generate collection profiles.
        
        Args:
            brand_context: Brand guide context
            brand_ids: List of brand IDs to associate with
            count: Number of collections to generate
            
        Returns:
            List of generated Collection objects
        """
        collections = []
        
        for i in range(count):
            try:
                # Select brand ID for this collection
                if not brand_ids:
                    print("Warning: No brand IDs available, skipping collection generation")
                    break
                brand_id = brand_ids[i % len(brand_ids)]
                
                # Format prompt with brand context and brand ID
                messages = COLLECTION_GENERATION_PROMPT.format_messages(
                    brand_context=brand_context,
                    brand_id=brand_id
                )
                
                # Generate response
                response = await self.llm.ainvoke(messages)
                content = response.content
                
                print(f"DEBUG: LLM response for collection {i+1}: {content[:200]}...")
                
                # Parse JSON response
                if isinstance(content, str):
                    collection_data = json.loads(content)
                else:
                    collection_data = content  # Already parsed
                
                # Validate and create Collection object
                collection = Collection(**collection_data)  # type: ignore
                collections.append(collection)
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error generating collection {i+1}: {e}")
                continue
        
        return collections 