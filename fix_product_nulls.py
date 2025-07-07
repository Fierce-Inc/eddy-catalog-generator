#!/usr/bin/env python3
"""Fix null values in products.csv by replacing empty fields with appropriate defaults."""

import csv
import sys
from pathlib import Path

def fix_product_nulls():
    """Fix null values in products.csv."""
    products_file = Path("data/products.csv")
    
    if not products_file.exists():
        print("Error: products.csv not found")
        return
    
    # Read the original file
    products = []
    with open(products_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    
    # Fix null values
    fixed_count = 0
    for product in products:
        # Fix empty sizes
        if not product['sizes'] or product['sizes'].strip() == '':
            product['sizes'] = 'One Size'
            fixed_count += 1
        
        # Fix empty fit
        if not product['fit'] or product['fit'].strip() == '':
            product['fit'] = 'Standard'
            fixed_count += 1
        
        # Fix empty colors
        if not product['colors'] or product['colors'].strip() == '':
            product['colors'] = 'N/A'
            fixed_count += 1
        
        # Fix empty materials
        if not product['materials'] or product['materials'].strip() == '':
            product['materials'] = 'N/A'
            fixed_count += 1
        
        # Fix empty sustainability_features
        if not product['sustainability_features'] or product['sustainability_features'].strip() == '':
            product['sustainability_features'] = 'N/A'
            fixed_count += 1
        
        # Fix empty care_instructions
        if not product['care_instructions'] or product['care_instructions'].strip() == '':
            product['care_instructions'] = 'N/A'
            fixed_count += 1
        
        # Fix empty features
        if not product['features'] or product['features'].strip() == '':
            product['features'] = 'N/A'
            fixed_count += 1
    
    # Write the fixed data back
    with open(products_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = products[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    
    print(f"Fixed {fixed_count} null values in products.csv")
    print("Products file has been updated successfully!")

if __name__ == "__main__":
    fix_product_nulls() 