#!/usr/bin/env python3
"""Fix null values in reviews.csv file."""

import csv


def fix_review_nulls():
    """Fix null values in reviews.csv by replacing empty strings with 'N/A'."""
    
    # Read existing reviews
    reviews = []
    with open('data/reviews.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reviews.append(row)
    
    print(f"Loaded {len(reviews)} reviews from CSV")
    
    # Count null values before fixing
    null_count_before = 0
    for row in reviews:
        for field, value in row.items():
            if not value or value.strip() == "":
                null_count_before += 1
    
    print(f"Found {null_count_before} null/empty values before fixing")
    
    # Fix null values
    fixed_count = 0
    for row in reviews:
        for field in ['size_worn', 'color_purchased']:
            if not row[field] or row[field].strip() == "":
                row[field] = "N/A"
                fixed_count += 1
    
    print(f"Fixed {fixed_count} null values")
    
    # Write back to CSV
    print(f"Writing {len(reviews)} reviews back to CSV...")
    with open('data/reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
        if reviews:
            fieldnames = reviews[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reviews)
    
    print("✅ Reviews CSV file updated successfully!")
    
    # Verify fix
    null_count_after = 0
    with open('data/reviews.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for field, value in row.items():
                if not value or value.strip() == "":
                    null_count_after += 1
    
    print(f"Null values after fixing: {null_count_after}")
    
    if null_count_after == 0:
        print("✅ All null values have been successfully fixed!")
    else:
        print(f"⚠️  Still found {null_count_after} null values")


if __name__ == "__main__":
    fix_review_nulls() 