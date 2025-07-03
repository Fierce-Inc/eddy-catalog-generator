"""Brand generation module."""

import json
import os
from typing import List

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import SecretStr

from src.schema import Brand
from src.prompts import BRAND_GENERATION_PROMPT


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
    
    async def generate_brands(self, brand_context: str, count: int = 5) -> List[Brand]:
        """Generate brand profiles.
        
        Args:
            brand_context: Brand guide context
            count: Number of brands to generate
            
        Returns:
            List of generated Brand objects
        """
        brands = []
        generated_names = set()
        generated_ids = set()
        
        for i in range(count):
            max_attempts = 3  # Try up to 3 times for uniqueness
            for attempt in range(max_attempts):
                try:
                    # Format prompt with brand context
                    messages = BRAND_GENERATION_PROMPT.format_messages(
                        brand_context=brand_context
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
                    
                    # Check for uniqueness
                    brand_name = brand_data.get("name", "").strip()  # type: ignore
                    brand_id = brand_data.get("id", "").strip()  # type: ignore
                    
                    if brand_name in generated_names:
                        print(f"Warning: Duplicate brand name '{brand_name}', retrying...")
                        continue
                    
                    if brand_id in generated_ids:
                        print(f"Warning: Duplicate brand ID '{brand_id}', retrying...")
                        continue
                    
                    # Validate and create Brand object
                    brand = Brand(**brand_data)  # type: ignore
                    brands.append(brand)
                    generated_names.add(brand_name)
                    generated_ids.add(brand_id)
                    break  # Success, move to next brand
                    
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error generating brand {i+1} (attempt {attempt+1}): {e}")
                    if attempt == max_attempts - 1:
                        print(f"Failed to generate brand {i+1} after {max_attempts} attempts")
                    continue
        
        return brands 