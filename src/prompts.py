"""Prompt templates for catalog generation."""

import json
from pathlib import Path
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate


def load_brand_config(config_filename: str = "evergreen.json") -> Dict[str, Any]:
    """Load brand configuration from JSON file in docs directory.
    
    Args:
        config_filename: Name of the JSON configuration file in docs/
        
    Returns:
        Dictionary containing brand configuration
    """
    config_path = Path(__file__).parent.parent / "docs" / config_filename
    if not config_path.exists():
        raise FileNotFoundError(f"Brand configuration not found at {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_brand_constants(config_filename: str = "evergreen.json") -> Dict[str, Any]:
    """Get brand constants from configuration file.
    
    Args:
        config_filename: Name of the JSON configuration file in docs/
        
    Returns:
        Dictionary containing all brand constants
    """
    config = load_brand_config(config_filename)
    
    # Convert price bands from lists to tuples for consistency
    price_bands = {}
    for band, values in config["price_bands"].items():
        price_bands[band] = tuple(values)
    
    return {
        "GENDER_DISTRIBUTION": config["gender_distribution"],
        "PRODUCT_CATEGORIES": config["product_categories"],
        "BRAND_COLORS": config["brand_colors"],
        "SIZE_RANGES": config["size_ranges"],
        "PRICE_BANDS": price_bands,
        "FIT_DESCRIPTIONS": config["fit_descriptions"],
        "SUSTAINABILITY_FEATURES": config["sustainability_features"]
    }


# Brand generation prompt
BRAND_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a brand strategist creating brand profiles.

{brand_context}

Generate a comprehensive brand profile that aligns with the provided brand identity.
The brand should reflect the core values and characteristics defined in the brand guide."""),
    ("human", """Create a COMPLETELY DIFFERENT brand profile with the following structure:

{{
    "id": "{brand_id}",
    "name": "Unique brand name",
    "description": "2-3 sentence brand description",
    "story": "Brand founding story (2-3 sentences)",
    "values": ["value1", "value2", "value3"],
    "target_audience": "Target customer description"
}}

Create a brand that COMPLEMENTS the main brand but is completely distinct. Think of it as a partner brand or sister brand with its own unique identity, name, and story.

CRITICAL REQUIREMENTS:
- The brand name must be completely unique and different from any existing brands
- Avoid generic naming patterns - be creative and specific
- Use distinctive words that reflect the brand's unique identity and values
- Consider using location-inspired names, nature elements, or unique descriptors
- Ensure the name is memorable and aligns with the brand's story and values

IMPORTANT: Return ONLY valid JSON. Do not include any explanatory text, markdown formatting, or code blocks."""),
])


# Collection generation prompt
COLLECTION_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a fashion collection designer.

{brand_context}

Create collections that embody the brand's core values and aesthetic.
Collections should reflect the brand's identity and target audience."""),
    ("human", """Create a collection profile with the following structure:

{{
    "id": "{collection_id}",
    "name": "Collection name",
    "description": "Collection description (2-3 sentences)",
    "season": "Spring|Summer|Fall|Winter|All-Season",
    "category": "Everyday|Work|Active|Outdoor",
    "brand_id": "{brand_id}",
    "launch_date": "YYYY-MM-DD",
    "theme": "Collection theme or inspiration"
}}

The collection should align with the brand's product portfolio focus and target audience.

CRITICAL REQUIREMENTS:
- The collection name must be completely unique and different from any existing collections
- Avoid generic naming patterns - be creative and specific with each collection name
- Use descriptive modifiers, seasonal themes, or unique concepts to differentiate collections
- Consider using location-inspired names, nature elements, or distinctive descriptors
- Ensure the name reflects the collection's theme, season, and target audience
- Each collection should have a distinct identity while maintaining brand consistency

IMPORTANT: Return ONLY valid JSON. Do not include any explanatory text, markdown formatting, or code blocks."""),
])


# Product generation prompt
PRODUCT_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a product designer.

{brand_context}

Create products that embody the brand's values and aesthetic.
Products should align with the brand's identity and target audience."""),
    ("human", """Generate {batch_size} products with the following specifications:

Gender distribution: {gender_distribution}
Categories: {categories}
Product IDs to use: {product_ids}

Each product should follow this JSON structure, using the provided IDs in order:

{{
    "id": "use_next_id_from_product_ids_list",
    "name": "Product name",
    "description": "Detailed product description",
    "category": "Product category",
    "subcategory": "Product subcategory", 
    "gender": "women|men|unisex",
    "collection_id": "{collection_id}",
    "brand_id": "{brand_id}",
    "price": float,
    "colors": ["color1", "color2"],
    "sizes": ["size1", "size2", "size3"],
    "materials": ["material1", "material2"],
    "fit": "fit description",
    "sustainability_features": ["feature1", "feature2"],
    "care_instructions": "Care instructions",
    "features": ["feature1", "feature2", "feature3"]
}}

Guidelines:
- Use brand colors: {brand_colors}
- Price range: ${min_price}-${max_price}
- Include sustainability features
- Ensure size inclusivity
- Focus on versatility and comfort
- Use the provided product IDs in the exact order they appear in the list
- CRITICAL: Each product name must be completely unique and different from all others
- Avoid generic naming patterns - be creative and specific with each name
- Use descriptive modifiers, style variations, or unique features to differentiate similar items

IMPORTANT SIZING GUIDELINES:
- For clothing items: Provide specific sizes (e.g., ["S", "M", "L", "XL"] or ["6", "7", "8", "9", "10"] or ["30", "32", "34", "36"])
- For accessories (scarves, bags, beanies, caps, gloves, flasks, sunglasses): Use ["One Size"] for sizes
- For footwear: Provide specific sizes (e.g., ["6", "7", "8", "9", "10"] or ["8", "9", "10", "11", "12"])
- For belts: Use ["S", "M", "L"] for sizes

IMPORTANT FIT GUIDELINES:
- For clothing items: Provide specific fit descriptions (e.g., "Regular fit", "Relaxed fit", "Tailored fit")
- For accessories: Use "Standard" for fit
- For footwear: Use "True to size" for fit

IMPORTANT: Return ONLY valid JSON array. Do not include any explanatory text, markdown formatting, or code blocks."""),
])


# Review generation prompt
REVIEW_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a customer review generator.

{brand_context}

Generate authentic, diverse customer reviews that reflect the brand's target audience and values.
Reviews should be realistic, varied in tone and rating, and mention specific product features."""),
    ("human", """Generate {batch_size} customer reviews for the product:

Product: {product_name}
Category: {product_category}
Price: ${product_price}
Review IDs to use: {review_ids}

Each review should follow this JSON structure, using the provided IDs in order:

{{
    "id": "use_next_id_from_review_ids_list",
    "product_id": "{product_id}",
    "customer_name": "Customer name",
    "rating": 1-5,
    "title": "Review title",
    "content": "Detailed review content (2-3 sentences)",
    "verified_purchase": true/false,
    "helpful_votes": 0-50,
    "review_date": "YYYY-MM-DD",
    "size_worn": "size or null",
    "color_purchased": "color or null"
}}

Guidelines:
- Mix of ratings (mostly 4-5 stars, some 3, few 1-2)
- Mention fit, comfort, versatility, sustainability, etc.
- Include lifestyle references or anecdotes appropriate to the brand's target audience
- Vary review length and helpfulness
- Use realistic customer names
- Use the provided review IDs in the exact order they appear in the list
- For size_worn: Use actual size (e.g., "M", "L", "10") or null if not applicable
- For color_purchased: Use actual color name (e.g., "Charcoal", "Ocean Blue") or null if not applicable
- Do not use empty strings - use null for missing values

IMPORTANT: Return ONLY valid JSON array. Do not include any explanatory text, markdown formatting, or code blocks."""),
]) 