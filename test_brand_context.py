#!/usr/bin/env python3
"""Test brand context loading."""

from src.utils.brand_context import get_brand_context

def main():
    print("Testing brand context loading...")
    try:
        context = get_brand_context(max_tokens=100)
        print(f"✅ Success! Brand context loaded ({len(context)} characters)")
        print(f"Preview: {context[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 