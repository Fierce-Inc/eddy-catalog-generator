"""Prompt templates for catalog generation."""

from langchain.prompts import ChatPromptTemplate

# Generation constants
GENDER_DISTRIBUTION = {
    "women": 0.45,
    "men": 0.45,
    "unisex": 0.10,
}

# Product categories and subcategories based on brand guide
PRODUCT_CATEGORIES = {
    "Everyday Apparel": [
        "Relaxed Denim",
        "Stretch Chinos", 
        "Essential Tees",
        "Knit Polos",
        "Tunic Shirts",
        "Wrap Dresses"
    ],
    "Work & Evening Wear": [
        "Tailored Blazers",
        "Smart Joggers",
        "Polished Midi Dresses",
        "Stretch Dress Pants",
        "Button-Down Shirts"
    ],
    "Everyday Outerwear": [
        "City Trenches",
        "Commuter Rain Jackets",
        "Quilted Bombers",
        "Lightweight Jackets",
        "Cardigans"
    ],
    "Active & Outdoor Layers": [
        "Packable Anoraks",
        "Trail Leggings",
        "Merino Base Layers",
        "Brushed-Back Leggings",
        "Performance Tees"
    ],
    "Accessories": [
        "Beanies",
        "Crossbody Bags",
        "Scarves",
        "Sunglasses",
        "Belts",
        "Hats"
    ],
    "Footwear": [
        "Slip-On Sneakers",
        "Low Hikers",
        "Dressy Booties",
        "City Hikers",
        "Casual Loafers"
    ]
}

# Brand color palette from guide
BRAND_COLORS = [
    "Evergreen", "Ocean Blue", "Urban Mist", "Rust Peak",
    "Charcoal", "Cream", "Navy", "Olive", "Burgundy", "Sage"
]

# Size ranges
SIZE_RANGES = {
    "women": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X"],
    "men": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X"],
    "unisex": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X"]
}

# Price bands (in USD)
PRICE_BANDS = {
    "budget": (25, 75),
    "mid": (75, 150),
    "premium": (150, 300),
    "luxury": (300, 500)
}

# Fit descriptions
FIT_DESCRIPTIONS = [
    "relaxed", "tailored", "slim", "oversized", "regular", 
    "comfortable", "fitted", "loose", "modern", "classic"
]

# Sustainability features
SUSTAINABILITY_FEATURES = [
    "Recycled polyester", "Organic cotton", "Tencel lyocell",
    "Repreve fibers", "Piñatex", "Low-impact dyes",
    "Circular design", "Repair-friendly construction",
    "Biodegradable packaging", "Fair trade certified"
]


# Brand generation prompt
BRAND_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a brand strategist creating brand profiles for Fierce Evergreen Apparel.

{brand_context}

Generate a comprehensive brand profile that aligns with the Fierce Evergreen brand identity.
The brand should reflect the core values of sustainability, body positivity, empowerment, and transparency."""),
    ("human", """Create a COMPLETELY DIFFERENT brand profile (NOT Fierce Evergreen Apparel) with the following structure:

{{
    "id": "{brand_id}",
    "name": "Unique brand name",
    "description": "2-3 sentence brand description",
    "story": "Brand founding story (2-3 sentences)",
    "values": ["value1", "value2", "value3"],
    "target_audience": "Target customer description"
}}

Create a brand that COMPLEMENTS Fierce Evergreen Apparel but is completely distinct. Think of it as a partner brand or sister brand with its own unique identity, name, and story. Do NOT use "Fierce Evergreen" in the name.
IMPORTANT: Return ONLY valid JSON. Do not include any explanatory text, markdown formatting, or code blocks."""),
])


# Collection generation prompt
COLLECTION_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a fashion collection designer for Fierce Evergreen Apparel.

{brand_context}

Create collections that embody the brand's commitment to sustainability, inclusivity, and everyday versatility.
Collections should reflect the Pacific Northwest aesthetic and the brand's core values."""),
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

The collection should align with Fierce Evergreen's product portfolio focus and target audience.
IMPORTANT: Return ONLY valid JSON. Do not include any explanatory text, markdown formatting, or code blocks."""),
])


# Product generation prompt
PRODUCT_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a product designer for Fierce Evergreen Apparel.

{brand_context}

Create products that embody the brand's values: sustainability, body positivity, functionality, and timeless style.
Products should be versatile, comfortable, and suitable for everyday wear with a Pacific Northwest aesthetic."""),
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

IMPORTANT: Return ONLY valid JSON array. Do not include any explanatory text, markdown formatting, or code blocks."""),
])


# Review generation prompt
REVIEW_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a customer review generator for Fierce Evergreen Apparel.

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
- Mention sustainability, fit, comfort, versatility
- Include Pacific Northwest lifestyle references
- Vary review length and helpfulness
- Use realistic customer names
- Use the provided review IDs in the exact order they appear in the list

IMPORTANT: Return ONLY valid JSON array. Do not include any explanatory text, markdown formatting, or code blocks."""),
]) 