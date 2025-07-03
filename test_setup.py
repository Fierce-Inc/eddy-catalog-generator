#!/usr/bin/env python3
"""Test script to verify the catalog generator setup."""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        # Test core imports
        from src.schema import Brand, Collection, Product, Review
        print("✅ Schema imports successful")
        
        from src.utils.brand_context import get_brand_context
        print("✅ Brand context import successful")
        
        from src.prompts import BRAND_GENERATION_PROMPT
        print("✅ Prompts import successful")
        
        from src.generators.brand_gen import BrandGenerator
        from src.generators.collection_gen import CollectionGenerator
        from src.generators.product_gen import ProductGenerator
        from src.generators.review_gen import ReviewGenerator
        print("✅ Generator imports successful")
        
        from src.pipeline import CatalogPipeline
        print("✅ Pipeline import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_brand_guide():
    """Test that the brand guide can be loaded."""
    print("\n📖 Testing brand guide loading...")
    
    try:
        from src.utils.brand_context import get_brand_context
        
        # Test loading brand context
        context = get_brand_context(max_tokens=100)
        print(f"✅ Brand context loaded ({len(context)} characters)")
        print(f"   Preview: {context[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Brand guide error: {e}")
        return False

def test_schema():
    """Test that schema objects can be created."""
    print("\n🏗️  Testing schema creation...")
    
    try:
        from src.schema import Brand, Collection, Product, Review
        
        # Test Brand creation
        brand = Brand(
            id="test_brand_001",
            name="Test Brand",
            description="A test brand for validation",
            story="Founded in 2024 for testing purposes",
            values=["Quality", "Sustainability", "Innovation"],
            target_audience="Test users"
        )
        print("✅ Brand creation successful")
        
        # Test CSV conversion
        csv_row = brand.to_csv_row()
        print(f"✅ CSV conversion successful: {list(csv_row.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Eddy Catalog Generator - Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_brand_guide,
        test_schema
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The catalog generator is ready to use.")
        print("\nNext steps:")
        print("1. Copy env.example to .env")
        print("2. Add your OpenAI API key to .env")
        print("3. Run: python -m src --out data/ --products 100")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 