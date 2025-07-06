#!/usr/bin/env python3
"""Fix existing duplicate collection names in the CSV file."""

import csv
import sys
from src.utils.name_validator import deduplicate_collection_names


def fix_existing_collection_duplicates():
    """Fix duplicate collection names in the existing CSV file."""
    
    # Read existing collections
    collections = []
    with open('data/collections.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            collections.append(row)
    
    print(f"Loaded {len(collections)} collections from CSV")
    
    # Check for duplicates before fixing
    names = [collection['name'] for collection in collections]
    duplicates_before = {}
    for i, name in enumerate(names):
        if names.count(name) > 1:
            if name not in duplicates_before:
                duplicates_before[name] = []
            duplicates_before[name].append(i)
    
    if duplicates_before:
        print(f"Found {len(duplicates_before)} duplicate collection names before fixing:")
        for name, indices in duplicates_before.items():
            print(f"  - {name} (appears {len(indices)} times at rows {indices})")
    else:
        print("No duplicates found!")
        return
    
    # Fix duplicates
    print("\nFixing duplicates...")
    fixed_collections = deduplicate_collection_names(collections)
    
    # Check for duplicates after fixing
    names_after = [collection['name'] for collection in fixed_collections]
    duplicates_after = {}
    for i, name in enumerate(names_after):
        if names_after.count(name) > 1:
            if name not in duplicates_after:
                duplicates_after[name] = []
            duplicates_after[name].append(i)
    
    if duplicates_after:
        print(f"WARNING: Still found {len(duplicates_after)} duplicate names after fixing:")
        for name, indices in duplicates_after.items():
            print(f"  - {name} (appears {len(indices)} times at rows {indices})")
    else:
        print("✅ All duplicates fixed successfully!")
    
    # Write back to CSV
    print(f"\nWriting {len(fixed_collections)} collections back to CSV...")
    with open('data/collections.csv', 'w', newline='', encoding='utf-8') as csvfile:
        if fixed_collections:
            fieldnames = fixed_collections[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(fixed_collections)
    
    print("✅ CSV file updated successfully!")


if __name__ == "__main__":
    fix_existing_collection_duplicates() 