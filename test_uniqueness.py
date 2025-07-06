#!/usr/bin/env python3
"""Test script to verify no duplicate IDs exist in generated CSV files."""

import csv
import os
import sys
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def load_csv_ids(file_path: str, id_column: str = "id") -> List[str]:
    """Load all IDs from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        id_column: Name of the ID column (default: "id")
        
    Returns:
        List of IDs from the file
    """
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist")
        return []
    
    ids = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if id_column in row and row[id_column].strip():
                    ids.append(row[id_column].strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    return ids


def load_csv_names(file_path: str, name_column: str = "name") -> List[str]:
    """Load all names from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        name_column: Name of the name column (default: "name")
        
    Returns:
        List of names from the file
    """
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} does not exist")
        return []
    
    names = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if name_column in row and row[name_column].strip():
                    names.append(row[name_column].strip())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    return names


def find_duplicates(items: List[str]) -> List[str]:
    """Find duplicate items in a list.
    
    Args:
        items: List of items to check
        
    Returns:
        List of duplicate items found
    """
    seen = set()
    duplicates = set()
    
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return list(duplicates)


def check_file_uniqueness(file_path: str, entity_type: str, id_column: str = "id") -> Tuple[bool, List[str], int]:
    """Check if a single CSV file has unique IDs.
    
    Args:
        file_path: Path to the CSV file
        entity_type: Type of entity (for reporting)
        id_column: Name of the ID column
        
    Returns:
        Tuple of (is_unique, duplicate_ids, total_count)
    """
    print(f"\nChecking {entity_type} file: {file_path}")
    
    ids = load_csv_ids(file_path, id_column)
    if not ids:
        print(f"  ⚠️  No IDs found in {file_path}")
        return True, [], 0
    
    duplicates = find_duplicates(ids)
    total_count = len(ids)
    unique_count = len(set(ids))
    
    print(f"  📊 Total records: {total_count}")
    print(f"  🔢 Unique IDs: {unique_count}")
    
    if duplicates:
        print(f"  ❌ Found {len(duplicates)} duplicate IDs:")
        for dup in sorted(duplicates):
            count = ids.count(dup)
            print(f"     - {dup} (appears {count} times)")
        return False, duplicates, total_count
    else:
        print(f"  ✅ All IDs are unique!")
        return True, [], total_count


def check_file_name_uniqueness(file_path: str, entity_type: str, name_column: str = "name") -> Tuple[bool, List[str], int]:
    """Check if a single CSV file has unique names.
    
    Args:
        file_path: Path to the CSV file
        entity_type: Type of entity (for reporting)
        name_column: Name of the name column
        
    Returns:
        Tuple of (is_unique, duplicate_names, total_count)
    """
    names = load_csv_names(file_path, name_column)
    if not names:
        print(f"  ⚠️  No names found in {file_path}")
        return True, [], 0
    
    duplicates = find_duplicates(names)
    total_count = len(names)
    unique_count = len(set(names))
    
    print(f"  📊 Total records: {total_count}")
    print(f"  🔢 Unique names: {unique_count}")
    
    if duplicates:
        print(f"  ⚠️  Found {len(duplicates)} duplicate names:")
        for dup in sorted(duplicates):
            count = names.count(dup)
            print(f"     - {dup} (appears {count} times)")
        return False, duplicates, total_count
    else:
        print(f"  ✅ All names are unique!")
        return True, [], total_count


def check_cross_file_uniqueness(all_ids: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
    """Check for duplicate IDs across different entity types.
    
    Args:
        all_ids: Dictionary mapping entity types to their ID lists
        
    Returns:
        Tuple of (is_unique, duplicate_ids)
    """
    print(f"\n🔍 Checking for cross-file duplicates...")
    
    # Combine all IDs with their source
    id_sources = defaultdict(list)
    for entity_type, ids in all_ids.items():
        for id_val in ids:
            id_sources[id_val].append(entity_type)
    
    # Find IDs that appear in multiple entity types
    cross_duplicates = []
    for id_val, sources in id_sources.items():
        if len(sources) > 1:
            cross_duplicates.append((id_val, sources))
    
    if cross_duplicates:
        print(f"  ❌ Found {len(cross_duplicates)} IDs that appear across multiple entity types:")
        for id_val, sources in cross_duplicates:
            print(f"     - {id_val} appears in: {', '.join(sources)}")
        return False, [dup[0] for dup in cross_duplicates]
    else:
        print(f"  ✅ No cross-file duplicates found!")
        return True, []


def check_cross_file_name_uniqueness(all_names: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
    """Check for duplicate names across different entity types.
    
    Args:
        all_names: Dictionary mapping entity types to their name lists
        
    Returns:
        Tuple of (is_unique, duplicate_names)
    """
    print(f"\n🔍 Checking for cross-file name duplicates...")
    
    # Combine all names with their source
    name_sources = defaultdict(list)
    for entity_type, names in all_names.items():
        for name_val in names:
            name_sources[name_val].append(entity_type)
    
    # Find names that appear in multiple entity types
    cross_duplicates = []
    for name_val, sources in name_sources.items():
        if len(sources) > 1:
            cross_duplicates.append((name_val, sources))
    
    if cross_duplicates:
        print(f"  ⚠️  Found {len(cross_duplicates)} names that appear across multiple entity types:")
        for name_val, sources in cross_duplicates:
            print(f"     - {name_val} appears in: {', '.join(sources)}")
        return False, [dup[0] for dup in cross_duplicates]
    else:
        print(f"  ✅ No cross-file name duplicates found!")
        return True, []


def main():
    """Main test function."""
    print("🧪 Testing ID and name uniqueness in generated CSV files")
    print("=" * 60)
    
    # Define expected CSV files and their entity types
    expected_files = {
        "data/brands.csv": "Brand",
        "data/collections.csv": "Collection", 
        "data/products.csv": "Product",
        "data/reviews.csv": "Review"
    }
    
    # Check each file individually for ID uniqueness
    all_ids = {}
    file_results = {}
    total_records = 0
    
    print("🔍 ID UNIQUENESS CHECK")
    print("-" * 30)
    
    for filename, entity_type in expected_files.items():
        is_unique, duplicates, count = check_file_uniqueness(filename, entity_type)
        file_results[filename] = {
            "is_unique": is_unique,
            "duplicates": duplicates,
            "count": count
        }
        all_ids[entity_type] = load_csv_ids(filename)
        total_records += count
    
    # Check for cross-file ID duplicates
    cross_unique, cross_duplicates = check_cross_file_uniqueness(all_ids)
    
    # Check each file individually for name uniqueness
    all_names = {}
    name_results = {}
    
    print("\n🔍 NAME UNIQUENESS CHECK")
    print("-" * 30)
    
    for filename, entity_type in expected_files.items():
        # Skip reviews as they don't have names
        if entity_type == "Review":
            continue
            
        is_unique, duplicates, count = check_file_name_uniqueness(filename, entity_type)
        name_results[filename] = {
            "is_unique": is_unique,
            "duplicates": duplicates,
            "count": count
        }
        all_names[entity_type] = load_csv_names(filename)
    
    # Check for cross-file name duplicates
    cross_name_unique, cross_name_duplicates = check_cross_file_name_uniqueness(all_names)
    
    # Summary
    print(f"\n📋 SUMMARY")
    print("=" * 60)
    
    all_files_unique = all(file_results[file]["is_unique"] for file in file_results)
    all_names_unique = all(name_results.get(file, {}).get("is_unique", True) for file in name_results)
    overall_unique = all_files_unique and cross_unique
    
    print(f"Total records processed: {total_records}")
    print(f"Files checked: {len(expected_files)}")
    
    if overall_unique:
        print(f"🎉 SUCCESS: All IDs are unique across all files!")
    else:
        print(f"❌ FAILURE: Duplicate IDs found!")
        
        # Report file-specific issues
        for filename, result in file_results.items():
            if not result["is_unique"]:
                print(f"  - {filename}: {len(result['duplicates'])} duplicate IDs")
        
        # Report cross-file issues
        if not cross_unique:
            print(f"  - Cross-file: {len(cross_duplicates)} IDs appear in multiple entity types")
    
    # Report name issues
    if not all_names_unique or not cross_name_unique:
        print(f"\n⚠️  NAME DUPLICATES FOUND (Warnings):")
        
        # Report file-specific name issues
        for filename, result in name_results.items():
            if not result["is_unique"]:
                print(f"  - {filename}: {len(result['duplicates'])} duplicate names")
        
        # Report cross-file name issues
        if not cross_name_unique:
            print(f"  - Cross-file: {len(cross_name_duplicates)} names appear in multiple entity types")
    
    return 0 if overall_unique else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 