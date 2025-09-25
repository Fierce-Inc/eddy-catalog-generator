"""Main pipeline orchestrator for catalog generation."""

import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd
from dotenv import load_dotenv

from src.utils.brand_context import get_brand_context
from src.generators.brand_gen import BrandGenerator
from src.generators.collection_gen import CollectionGenerator
from src.generators.product_gen import ProductGenerator
from src.generators.review_gen import ReviewGenerator
from src.schema import Brand, Collection, Product, Review


class CatalogPipeline:
    """Main pipeline for generating the complete catalog."""
    
    def __init__(self, output_dir: str = "data", brand_guide_filename: Optional[str] = None, brand_config_filename: Optional[str] = None):
        """Initialize the pipeline.
        
        Args:
            output_dir: Directory to save generated CSV files
            brand_guide_filename: Optional brand guide filename inside the hardcoded `docs` directory
            brand_config_filename: Optional brand configuration JSON filename inside the hardcoded `docs` directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.brand_guide_filename = brand_guide_filename
        self.brand_config_filename = brand_config_filename
        
        # Load environment variables
        load_dotenv()
        
        # Initialize generators
        self.brand_generator = BrandGenerator(
            temperature=float(os.getenv("TEMPERATURE_PRODUCT", "0.7"))
        )
        self.collection_generator = CollectionGenerator(
            temperature=float(os.getenv("TEMPERATURE_PRODUCT", "0.7"))
        )
        self.product_generator = ProductGenerator(
            temperature=float(os.getenv("TEMPERATURE_PRODUCT", "0.7")),
            batch_size=int(os.getenv("BATCH_SIZE", "50")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            brand_config_filename=self.brand_config_filename or "evergreen.json"
        )
        self.review_generator = ReviewGenerator(
            temperature=float(os.getenv("TEMPERATURE_REVIEW", "0.5")),
            batch_size=int(os.getenv("BATCH_SIZE", "20")),
            max_retries=int(os.getenv("MAX_RETRIES", "3"))
        )
    
    async def run(self, total_products: int = 10000) -> Dict[str, str]:
        """Run the complete catalog generation pipeline.
        
        Args:
            total_products: Total number of products to generate
            
        Returns:
            Dictionary mapping entity types to their CSV file paths
        """
        # Calculate entity counts based on product count
        brand_count = max(2, (total_products + 99) // 100)  # products / 100 rounded up, minimum 2
        # Minimum 2 collections per brand, max 100 products per collection
        min_collections = brand_count * 2  # At least 2 collections per brand
        max_collections = (total_products + 99) // 100  # Max 100 products per collection
        collection_count = max(min_collections, max_collections)
        reviews_per_product = max(2, min(5, 10000 // total_products))  # 2-5 reviews per product
        total_reviews = total_products * reviews_per_product
        
        print("🚀 Starting Catalog Generation")
        print("=" * 60)
        print(f"📊 Generation Plan:")
        print(f"   • Brands: {brand_count}")
        print(f"   • Collections: {collection_count}")
        print(f"   • Products: {total_products}")
        print(f"   • Reviews: {total_reviews} ({reviews_per_product} per product)")
        print("=" * 60)
        
        # Step 1: Load brand context
        print("📖 Loading brand context...")
        brand_context = get_brand_context(brand_guide_filename=self.brand_guide_filename)
        print(f"✅ Brand context loaded ({len(brand_context)} characters)")
        
        # Step 2: Generate brands
        print(f"\n🏷️  Generating {brand_count} brands...")
        brands = await self.brand_generator.generate_brands(brand_context, count=brand_count)
        print(f"✅ Generated {len(brands)} brands")
        
        # Step 3: Generate collections
        print(f"\n📦 Generating {collection_count} collections...")
        brand_ids = [brand.id for brand in brands]
        collections = await self.collection_generator.generate_collections(
            brand_context, brand_ids, count=collection_count
        )
        print(f"✅ Generated {len(collections)} collections")
        
        # Step 4: Generate products
        print(f"\n👕 Generating {total_products} products...")
        brands_dict = [brand.dict() for brand in brands]
        collections_dict = [collection.dict() for collection in collections]
        
        products = await self.product_generator.generate_products(
            brand_context, brands_dict, collections_dict, total_products
        )
        print(f"✅ Generated {len(products)} products")
        
        # Step 5: Generate reviews
        print(f"\n⭐ Generating {total_reviews} reviews ({reviews_per_product} per product)...")
        reviews = await self.review_generator.generate_reviews(
            brand_context, products, reviews_per_product=reviews_per_product
        )
        print(f"✅ Generated {len(reviews)} reviews")
        
        # Step 6: Export to CSV
        print("\n💾 Exporting to CSV...")
        csv_paths = await self._export_to_csv(brands, collections, products, reviews)
        
        print("\n🎉 Catalog generation complete!")
        print("=" * 60)
        for entity_type, path in csv_paths.items():
            print(f"📄 {entity_type}: {path}")
        
        return csv_paths
    
    async def _export_to_csv(
        self,
        brands: List[Brand],
        collections: List[Collection],
        products: List[Product],
        reviews: List[Review]
    ) -> Dict[str, str]:
        """Export all entities to CSV files.
        
        Args:
            brands: List of Brand objects
            collections: List of Collection objects
            products: List of Product objects
            reviews: List of Review objects
            
        Returns:
            Dictionary mapping entity types to CSV file paths
        """
        csv_paths = {}
        
        # Export brands
        brands_df = pd.DataFrame([brand.to_csv_row() for brand in brands])
        brands_path = self.output_dir / "brands.csv"
        brands_df.to_csv(brands_path, index=False)
        csv_paths["brands"] = str(brands_path)
        
        # Export collections
        collections_df = pd.DataFrame([collection.to_csv_row() for collection in collections])
        collections_path = self.output_dir / "collections.csv"
        collections_df.to_csv(collections_path, index=False)
        csv_paths["collections"] = str(collections_path)
        
        # Export products
        products_df = pd.DataFrame([product.to_csv_row() for product in products])
        products_path = self.output_dir / "products.csv"
        products_df.to_csv(products_path, index=False)
        csv_paths["products"] = str(products_path)
        
        # Export reviews
        reviews_df = pd.DataFrame([review.to_csv_row() for review in reviews])
        reviews_path = self.output_dir / "reviews.csv"
        reviews_df.to_csv(reviews_path, index=False)
        csv_paths["reviews"] = str(reviews_path)
        
        return csv_paths


async def main():
    """Main entry point for the pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic catalog")
    parser.add_argument(
        "--out", 
        default="data", 
        help="Output directory for CSV files (default: data)"
    )
    parser.add_argument(
        "--products", 
        type=int, 
        default=10000, 
        help="Number of products to generate (default: 10000)"
    )
    parser.add_argument(
        "--brand-guide",
        default="brand_guide.md",
        help="Brand guide filename inside docs/ (default: brand_guide.md)"
    )
    parser.add_argument(
        "--brand-config",
        default="evergreen.json",
        help="Brand configuration JSON filename inside docs/ (default: evergreen.json)"
    )
    
    args = parser.parse_args()
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("Please set it in your .env file or environment")
        return
    
    # Run pipeline
    pipeline = CatalogPipeline(
        output_dir=args.out, 
        brand_guide_filename=args.brand_guide,
        brand_config_filename=args.brand_config
    )
    await pipeline.run(total_products=args.products)


if __name__ == "__main__":
    asyncio.run(main()) 