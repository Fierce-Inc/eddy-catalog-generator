#!/usr/bin/env python3
"""Analyze null values in CSV files."""

import csv


def analyze_nulls():
    """Analyze null values in products.csv."""
    
    with open('data/products.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    print("Analyzing null values in products.csv:")
    print("=" * 50)
    
    # Check each row for empty fields
    for i, row in enumerate(rows):
        empty_fields = []
        for field, value in row.items():
            if not value or value.strip() == "":
                empty_fields.append(field)
        
        if empty_fields:
            print(f"Row {i+1}: Empty fields: {empty_fields}")
            print(f"  Product: {row.get('name', 'N/A')}")
            print(f"  ID: {row.get('id', 'N/A')}")
            print()
    
    # Check reviews.csv as well
    print("\nAnalyzing null values in reviews.csv:")
    print("=" * 50)
    
    try:
        with open('data/reviews.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
        
        for i, row in enumerate(rows):
            empty_fields = []
            for field, value in row.items():
                if not value or value.strip() == "":
                    empty_fields.append(field)
            
            if empty_fields:
                print(f"Row {i+1}: Empty fields: {empty_fields}")
                print(f"  Review ID: {row.get('id', 'N/A')}")
                print(f"  Product ID: {row.get('product_id', 'N/A')}")
                print()
                
    except FileNotFoundError:
        print("reviews.csv not found")


if __name__ == "__main__":
    analyze_nulls() 