"""Review generation module."""

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from tqdm import tqdm
from pydantic import SecretStr

from src.schema import Product, Review
from src.prompts import REVIEW_GENERATION_PROMPT


class ReviewGenerator:
    """Generates customer reviews using OpenAI and LangChain."""
    
    def __init__(self, temperature: float = 0.5, batch_size: int = 20, max_retries: int = 3):
        """Initialize the review generator.
        
        Args:
            temperature: Temperature for generation (0.0-1.0)
            batch_size: Number of reviews to generate per API call
            max_retries: Maximum retry attempts for failed generations
        """
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            temperature=temperature,
            api_key=SecretStr(os.getenv("OPENAI_API_KEY", "")),
        )
        self.batch_size = batch_size
        self.max_retries = max_retries
    
    async def generate_reviews(
        self,
        brand_context: str,
        products: List[Product],
        reviews_per_product: int = 5
    ) -> List[Review]:
        """Generate customer reviews for products.
        
        Args:
            brand_context: Brand guide context
            products: List of Product objects
            reviews_per_product: Number of reviews per product
            
        Returns:
            List of generated Review objects
        """
        reviews = []
        
        with tqdm(total=len(products), desc="Generating reviews") as pbar:
            for product in products:
                product_reviews = await self._generate_product_reviews(
                    brand_context=brand_context,
                    product=product,
                    count=reviews_per_product
                )
                reviews.extend(product_reviews)
                pbar.update(1)
        
        return reviews
    
    async def _generate_product_reviews(
        self,
        brand_context: str,
        product: Product,
        count: int
    ) -> List[Review]:
        """Generate reviews for a specific product."""
        
        # Split into batches if needed
        batches = []
        for i in range(0, count, self.batch_size):
            batch_count = min(self.batch_size, count - i)
            batches.append(batch_count)
        
        product_reviews = []
        
        for batch_count in batches:
            batch_reviews = await self._generate_batch_with_retry(
                brand_context=brand_context,
                product=product,
                batch_count=batch_count
            )
            product_reviews.extend(batch_reviews)
        
        return product_reviews
    
    async def _generate_batch_with_retry(
        self,
        brand_context: str,
        product: Product,
        batch_count: int
    ) -> List[Review]:
        """Generate a batch of reviews with retry logic."""
        
        for attempt in range(self.max_retries):
            try:
                # Format prompt with product details
                messages = REVIEW_GENERATION_PROMPT.format_messages(
                    brand_context=brand_context,
                    batch_size=batch_count,
                    product_name=product.name,
                    product_category=product.category,
                    product_price=product.price,
                    product_id=product.id
                )
                
                # Generate response
                response = await self.llm.ainvoke(messages)
                content = response.content
                
                print(f"DEBUG: LLM response for review batch: {content[:200]}...")
                
                # Parse JSON response
                if isinstance(content, str):
                    reviews_data = json.loads(content)
                else:
                    reviews_data = content  # Already parsed
                
                # Validate and create Review objects
                reviews = []
                for review_data in reviews_data:
                    # Add realistic review date
                    if "review_date" not in review_data:
                        review_data["review_date"] = self._generate_review_date()  # type: ignore
                    
                    review = Review(**review_data)  # type: ignore
                    reviews.append(review)
                
                return reviews
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Review batch generation attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    print(f"Failed to generate review batch after {self.max_retries} attempts")
                    return []
        
        return []
    
    def _generate_review_date(self) -> str:
        """Generate a realistic review date within the last 2 years."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)  # 2 years ago
        
        random_days = random.randint(0, 730)
        review_date = start_date + timedelta(days=random_days)
        
        return review_date.strftime("%Y-%m-%d") 