"""Pydantic data models for the catalog generator."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Brand(BaseModel):
    """Brand entity for the catalog."""
    
    id: str = Field(..., description="Unique brand identifier")
    name: str = Field(..., description="Brand name")
    description: str = Field(..., description="Brand description")
    story: str = Field(..., description="Brand founding story")
    values: List[str] = Field(..., description="Core brand values")
    target_audience: str = Field(..., description="Target customer description")
    
    def to_csv_row(self) -> dict:
        """Convert to CSV row format."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "story": self.story,
            "values": "|".join(self.values),
            "target_audience": self.target_audience,
        }


class Collection(BaseModel):
    """Collection entity for the catalog."""
    
    id: str = Field(..., description="Unique collection identifier")
    name: str = Field(..., description="Collection name")
    description: str = Field(..., description="Collection description")
    season: str = Field(..., description="Season (e.g., Spring, Fall, All-Season)")
    category: str = Field(..., description="Category (e.g., Everyday, Work, Active)")
    brand_id: str = Field(..., description="Associated brand ID")
    launch_date: str = Field(..., description="Launch date (YYYY-MM-DD)")
    theme: str = Field(..., description="Collection theme or inspiration")
    
    def to_csv_row(self) -> dict:
        """Convert to CSV row format."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "season": self.season,
            "category": self.category,
            "brand_id": self.brand_id,
            "launch_date": self.launch_date,
            "theme": self.theme,
        }


class Product(BaseModel):
    """Product entity for the catalog."""
    
    id: str = Field(..., description="Unique product identifier (SKU)")
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    category: str = Field(..., description="Product category")
    subcategory: str = Field(..., description="Product subcategory")
    gender: str = Field(..., description="Target gender (women, men, unisex)")
    collection_id: str = Field(..., description="Associated collection ID")
    brand_id: str = Field(..., description="Associated brand ID")
    price: float = Field(..., description="Product price in USD")
    colors: List[str] = Field(..., description="Available colors")
    sizes: List[str] = Field(..., description="Available sizes")
    materials: List[str] = Field(..., description="Materials used")
    fit: str = Field(..., description="Fit description (e.g., relaxed, tailored)")
    sustainability_features: List[str] = Field(..., description="Sustainability features")
    care_instructions: str = Field(..., description="Care instructions")
    features: List[str] = Field(..., description="Product features")
    
    def to_csv_row(self) -> dict:
        """Convert to CSV row format."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "gender": self.gender,
            "collection_id": self.collection_id,
            "brand_id": self.brand_id,
            "price": self.price,
            "colors": "|".join(self.colors) if self.colors else "N/A",
            "sizes": "|".join(self.sizes) if self.sizes else "One Size",
            "materials": "|".join(self.materials) if self.materials else "N/A",
            "fit": self.fit if self.fit else "Standard",
            "sustainability_features": "|".join(self.sustainability_features) if self.sustainability_features else "N/A",
            "care_instructions": self.care_instructions if self.care_instructions else "N/A",
            "features": "|".join(self.features) if self.features else "N/A",
        }


class Review(BaseModel):
    """Review entity for the catalog."""
    
    id: str = Field(..., description="Unique review identifier")
    product_id: str = Field(..., description="Associated product ID")
    customer_name: str = Field(..., description="Customer name (anonymized)")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5 stars)")
    title: str = Field(..., description="Review title")
    content: str = Field(..., description="Review content")
    verified_purchase: bool = Field(..., description="Whether purchase was verified")
    helpful_votes: int = Field(..., ge=0, description="Number of helpful votes")
    review_date: str = Field(..., description="Review date (YYYY-MM-DD)")
    size_worn: Optional[str] = Field(None, description="Size worn by reviewer")
    color_purchased: Optional[str] = Field(None, description="Color purchased")
    
    def to_csv_row(self) -> dict:
        """Convert to CSV row format."""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "customer_name": self.customer_name,
            "rating": self.rating,
            "title": self.title,
            "content": self.content,
            "verified_purchase": self.verified_purchase,
            "helpful_votes": self.helpful_votes,
            "review_date": self.review_date,
            "size_worn": self.size_worn if self.size_worn is not None else "N/A",
            "color_purchased": self.color_purchased if self.color_purchased is not None else "N/A",
        } 