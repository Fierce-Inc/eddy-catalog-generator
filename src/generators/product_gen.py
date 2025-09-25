"""Product generation module."""

import json
import os
import random
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from tqdm import tqdm
from pydantic import SecretStr

from src.schema import Product
from src.prompts import (
    PRODUCT_GENERATION_PROMPT, 
    get_brand_constants
)
from src.utils.id_generator import IDGenerator
from src.utils.name_validator import NameValidator, deduplicate_product_names


class ProductGenerator:
    """Generates product profiles using OpenAI and LangChain."""
    
    def __init__(self, temperature: float = 0.7, batch_size: int = 50, max_retries: int = 3, brand_config_filename: str = "evergreen.json"):
        """Initialize the product generator.
        
        Args:
            temperature: Temperature for generation (0.0-1.0)
            batch_size: Number of products to generate per API call
            max_retries: Maximum retry attempts for failed generations
            brand_config_filename: Brand configuration JSON filename
        """
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            temperature=temperature,
            api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
        )
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.brand_config_filename = brand_config_filename
        self.brand_constants = get_brand_constants(brand_config_filename)
        self.id_generator = IDGenerator()
        self.name_validator = NameValidator()
    
    async def generate_products(
        self,
        brand_context: str,
        brands: List[Dict[str, Any]],
        collections: List[Dict[str, Any]],
        total_count: int = 10000
    ) -> List[Product]:
        """Generate product profiles in batches.
        
        Args:
            brand_context: Brand guide context
            brands: List of brand dictionaries
            collections: List of collection dictionaries
            total_count: Total number of products to generate
            
        Returns:
            List of generated Product objects
        """
        products = []
        brand_ids = [brand["id"] for brand in brands]
        collection_ids = [collection["id"] for collection in collections]
        
        # Calculate batches
        num_batches = (total_count + self.batch_size - 1) // self.batch_size
        
        with tqdm(total=total_count, desc="Generating products") as pbar:
            for batch_idx in range(num_batches):
                batch_count = min(self.batch_size, total_count - len(products))
                
                # Pre-generate unique product IDs for this batch
                batch_product_ids = self.id_generator.generate_product_ids(batch_count)
                
                # Select random brand and collection for this batch
                if not brand_ids:
                    print("Warning: No brand IDs available, using default")
                    brand_id = "default_brand"
                else:
                    brand_id = random.choice(brand_ids)
                    
                if not collection_ids:
                    print("Warning: No collection IDs available, using default")
                    collection_id = "default_collection"
                else:
                    collection_id = random.choice(collection_ids)
                
                # Determine gender distribution for this batch
                gender_distribution = self._get_gender_distribution(batch_count)
                
                # Select categories for this batch
                categories = self._select_categories(batch_count)
                
                # Generate batch with pre-generated IDs
                batch_products = await self._generate_batch_with_retry(
                    brand_context=brand_context,
                    brand_id=brand_id,
                    collection_id=collection_id,
                    gender_distribution=gender_distribution,
                    categories=categories,
                    batch_count=batch_count,
                    product_ids=batch_product_ids
                )
                
                products.extend(batch_products)
                pbar.update(len(batch_products))
                
                if len(products) >= total_count:
                    break
        
        print(f"Generated {len(products)} products with pre-generated unique IDs")
        
        # Final deduplication across all batches
        print("Performing final name deduplication...")
        products_dict = [product.dict() for product in products]
        final_deduplicated = deduplicate_product_names(products_dict)
        
        # Convert back to Product objects
        final_products = []
        for product_dict in final_deduplicated:
            try:
                product = Product(**product_dict)
                final_products.append(product)
            except (ValueError, TypeError) as e:
                print(f"Warning: Invalid product data in final deduplication: {e}, skipping product")
                continue
        
        print(f"Final product count after deduplication: {len(final_products)}")
        return final_products[:total_count]
    
    def _get_gender_distribution(self, batch_count: int) -> Dict[str, int]:
        """Calculate gender distribution for a batch."""
        distribution = {}
        for gender, ratio in self.brand_constants["GENDER_DISTRIBUTION"].items():
            count = int(batch_count * ratio)
            distribution[gender] = count
        
        # Adjust for rounding
        total = sum(distribution.values())
        if total < batch_count:
            distribution["women"] += batch_count - total
        
        return distribution
    
    def _select_categories(self, batch_count: int) -> List[str]:
        """Select product categories for a batch."""
        all_categories = list(self.brand_constants["PRODUCT_CATEGORIES"].keys())
        selected = []
        
        for _ in range(batch_count):
            category = random.choice(all_categories)
            selected.append(category)
        
        return selected
    
    async def _generate_batch_with_retry(
        self,
        brand_context: str,
        brand_id: str,
        collection_id: str,
        gender_distribution: Dict[str, int],
        categories: List[str],
        batch_count: int,
        product_ids: List[str]
    ) -> List[Product]:
        """Generate a batch of products with pre-generated IDs."""
        
        for attempt in range(self.max_retries):
            try:
                # Format prompt with all parameters including pre-generated product IDs
                messages = PRODUCT_GENERATION_PROMPT.format_messages(
                    brand_context=brand_context,
                    batch_size=batch_count,
                    gender_distribution=gender_distribution,
                    categories=categories,
                    collection_id=collection_id,
                    brand_id=brand_id,
                    brand_colors=self.brand_constants["BRAND_COLORS"],
                    min_price=self.brand_constants["PRICE_BANDS"]["budget"][0],
                    max_price=self.brand_constants["PRICE_BANDS"]["luxury"][1],
                    product_ids=product_ids
                )
                
                # Generate response
                response = await self.llm.ainvoke(messages)
                content = response.content
                
                print(f"DEBUG: LLM response for product batch (attempt {attempt+1}): {content[:200]}...")
                
                # Parse JSON response
                if isinstance(content, str):
                    products_data = json.loads(content)
                else:
                    products_data = content  # Already parsed
                
                # Validate and create Product objects with pre-generated IDs
                products = []
                
                for i, product_data in enumerate(products_data):
                    # Ensure the ID matches what we provided
                    expected_id = product_ids[i] if i < len(product_ids) else None
                    if expected_id and product_data.get("id") != expected_id:  # type: ignore
                        product_data["id"] = expected_id  # type: ignore
                    
                    try:
                        product = Product(**product_data)  # type: ignore
                        products.append(product)
                    except (ValueError, TypeError) as e:
                        print(f"Warning: Invalid product data: {e}, skipping product")
                        continue
                
                # Validate name uniqueness within this batch
                batch_products_dict = [product.dict() for product in products]
                deduplicated_batch = deduplicate_product_names(batch_products_dict)
                
                # Convert back to Product objects
                products = []
                for product_dict in deduplicated_batch:
                    try:
                        product = Product(**product_dict)
                        products.append(product)
                    except (ValueError, TypeError) as e:
                        print(f"Warning: Invalid product data after deduplication: {e}, skipping product")
                        continue
                
                print(f"Successfully generated {len(products)} products in batch")
                return products
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Batch generation attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    print(f"Failed to generate batch after {self.max_retries} attempts")
                    return []
        
        return [] 