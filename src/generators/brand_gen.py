"""Brand generation module."""

import json
import os
from typing import List

from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.schema import Brand
from src.prompts import BRAND_GENERATION_PROMPT
from src.utils.id_generator import IDGenerator
from src.utils.name_validator import deduplicate_brand_names


class BrandGenerator:
    """Generates brand profiles using OpenAI and LangChain."""
    
    def __init__(self, temperature: float = 0.7):
        """Initialize the brand generator.
        
        Args:
            temperature: Temperature for generation (0.0-1.0)
        """
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            temperature=temperature,
            api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
        )
        self.id_generator = IDGenerator()
    
    async def generate_brands(self, brand_context: str, count: int = 5) -> List[Brand]:
        """Generate brand profiles.
        
        Args:
            brand_context: Brand guide context
            count: Number of brands to generate
            
        Returns:
            List of generated Brand objects
        """
        # Pre-generate unique brand IDs
        brand_ids = self.id_generator.generate_brand_ids(count)
        brands = []
        
        for i, brand_id in enumerate(brand_ids):
            max_attempts = 3  # Reduced attempts since IDs are pre-generated
            brand_generated = False
            
            for attempt in range(max_attempts):
                try:
                    # Format prompt with brand context and pre-generated ID
                    messages = BRAND_GENERATION_PROMPT.format_messages(
                        brand_context=brand_context,
                        brand_id=brand_id
                    )
                    
                    # Generate response
                    response = await self.llm.ainvoke(messages)
                    content = response.content
                    
                    print(f"DEBUG: LLM response for brand {i+1} (attempt {attempt+1}): {content[:200]}...")
                    
                    # Parse JSON response
                    if isinstance(content, str):
                        brand_data = json.loads(content)
                    else:
                        brand_data = content  # Already parsed
                    
                    # Validate required fields
                    brand_name = brand_data.get("name", "").strip()  # type: ignore
                    if not brand_name:
                        print(f"Warning: Missing name for brand {i+1} (attempt {attempt+1}), retrying...")
                        continue
                    
                    # Ensure the ID matches what we provided
                    if brand_data.get("id") != brand_id:  # type: ignore
                        brand_data["id"] = brand_id  # type: ignore
                    
                    # Validate and create Brand object
                    brand = Brand(**brand_data)  # type: ignore
                    brands.append(brand)
                    brand_generated = True
                    print(f"Successfully generated brand {i+1}: {brand_name} (ID: {brand_id})")
                    break  # Success, move to next brand
                    
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error generating brand {i+1} (attempt {attempt+1}): {e}")
                    if attempt == max_attempts - 1:
                        print(f"Failed to generate brand {i+1} after {max_attempts} attempts")
                    continue
            
            if not brand_generated:
                print(f"Warning: Could not generate brand {i+1} after {max_attempts} attempts")
        
        print(f"Generated {len(brands)} brands with pre-generated unique IDs")
        
        # Final deduplication of brand names
        print("Performing final brand name deduplication...")
        brands_dict = [brand.dict() for brand in brands]
        final_deduplicated = deduplicate_brand_names(brands_dict)
        
        # Convert back to Brand objects
        final_brands = []
        for brand_dict in final_deduplicated:
            try:
                brand = Brand(**brand_dict)
                final_brands.append(brand)
            except (ValueError, TypeError) as e:
                print(f"Warning: Invalid brand data in final deduplication: {e}, skipping brand")
                continue
        
        print(f"Final brand count after deduplication: {len(final_brands)}")
        return final_brands 