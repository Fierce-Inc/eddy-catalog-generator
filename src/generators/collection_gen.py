"""Collection generation module."""

import json
import os
from typing import List

from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.schema import Collection
from src.prompts import COLLECTION_GENERATION_PROMPT
from src.utils.id_generator import IDGenerator


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
        self.id_generator = IDGenerator()
    
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
        # Pre-generate unique collection IDs
        collection_ids = self.id_generator.generate_collection_ids(count)
        collections = []
        
        for i, collection_id in enumerate(collection_ids):
            max_attempts = 3  # Reduced attempts since IDs are pre-generated
            collection_generated = False
            
            for attempt in range(max_attempts):
                try:
                    # Select brand ID for this collection
                    if not brand_ids:
                        print("Warning: No brand IDs available, skipping collection generation")
                        break
                    brand_id = brand_ids[i % len(brand_ids)]
                    
                    # Format prompt with brand context, brand ID, and pre-generated collection ID
                    messages = COLLECTION_GENERATION_PROMPT.format_messages(
                        brand_context=brand_context,
                        brand_id=brand_id,
                        collection_id=collection_id
                    )
                    
                    # Generate response
                    response = await self.llm.ainvoke(messages)
                    content = response.content
                    
                    print(f"DEBUG: LLM response for collection {i+1} (attempt {attempt+1}): {content[:200]}...")
                    
                    # Parse JSON response
                    if isinstance(content, str):
                        collection_data = json.loads(content)
                    else:
                        collection_data = content  # Already parsed
                    
                    # Validate required fields
                    collection_name = collection_data.get("name", "").strip()  # type: ignore
                    if not collection_name:
                        print(f"Warning: Missing name for collection {i+1} (attempt {attempt+1}), retrying...")
                        continue
                    
                    # Ensure the ID matches what we provided
                    if collection_data.get("id") != collection_id:  # type: ignore
                        collection_data["id"] = collection_id  # type: ignore
                    
                    # Validate and create Collection object
                    collection = Collection(**collection_data)  # type: ignore
                    collections.append(collection)
                    collection_generated = True
                    print(f"Successfully generated collection {i+1}: {collection_name} (ID: {collection_id})")
                    break  # Success, move to next collection
                    
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error generating collection {i+1} (attempt {attempt+1}): {e}")
                    if attempt == max_attempts - 1:
                        print(f"Failed to generate collection {i+1} after {max_attempts} attempts")
                    continue
            
            if not collection_generated:
                print(f"Warning: Could not generate collection {i+1} after {max_attempts} attempts")
        
        print(f"Generated {len(collections)} collections with pre-generated unique IDs")
        return collections 