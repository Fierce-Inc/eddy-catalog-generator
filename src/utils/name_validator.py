"""Name validation utilities for ensuring unique product names."""

import re
from typing import List, Dict, Set, Optional
from collections import defaultdict


class NameValidator:
    """Validates and ensures unique product names."""
    
    def __init__(self):
        """Initialize the name validator."""
        self.used_names: Set[str] = set()
        self.name_patterns: Dict[str, int] = defaultdict(int)
    
    def add_name(self, name: str) -> None:
        """Add a name to the registry.
        
        Args:
            name: Product name to register
        """
        self.used_names.add(name.lower().strip())
        
        # Track naming patterns
        pattern = self._extract_pattern(name)
        self.name_patterns[pattern] += 1
    
    def is_unique(self, name: str) -> bool:
        """Check if a name is unique.
        
        Args:
            name: Product name to check
            
        Returns:
            True if name is unique, False otherwise
        """
        return name.lower().strip() not in self.used_names
    
    def get_used_names(self) -> Set[str]:
        """Get all used names.
        
        Returns:
            Set of all used names
        """
        return self.used_names.copy()
    
    def get_name_suggestions(self, base_name: str, category: str, gender: str, color: str) -> List[str]:
        """Generate unique name suggestions based on a base name.
        
        Args:
            base_name: Original name that needs to be made unique
            category: Product category
            gender: Target gender
            color: Primary color
            
        Returns:
            List of unique name suggestions
        """
        suggestions = []
        
        # Extract components from base name
        components = self._parse_name_components(base_name)
        
        # Strategy 1: Add descriptive modifiers
        modifiers = [
            "Classic", "Modern", "Premium", "Essential", "Signature", 
            "Heritage", "Contemporary", "Refined", "Elegant", "Casual"
        ]
        
        for modifier in modifiers:
            new_name = f"{modifier} {base_name}"
            if self.is_unique(new_name):
                suggestions.append(new_name)
                if len(suggestions) >= 5:
                    break
        
        # Strategy 2: Add style descriptors
        if len(suggestions) < 5:
            style_descriptors = [
                "Relaxed", "Slim", "Tailored", "Oversized", "Fitted",
                "Comfortable", "Structured", "Flexible", "Adaptive"
            ]
            
            for descriptor in style_descriptors:
                new_name = f"{color} {descriptor} {components.get('item_type', '')}"
                if self.is_unique(new_name):
                    suggestions.append(new_name)
                    if len(suggestions) >= 5:
                        break
        
        # Strategy 3: Add category-specific terms
        if len(suggestions) < 5:
            category_terms = {
                "Everyday Apparel": ["Daily", "Versatile", "Essential"],
                "Work & Evening Wear": ["Professional", "Polished", "Sophisticated"],
                "Active & Outdoor Layers": ["Performance", "Active", "Outdoor"],
                "Everyday Outerwear": ["Layered", "Protective", "Comfortable"],
                "Accessories": ["Stylish", "Functional", "Versatile"],
                "Footwear": ["Comfortable", "Durable", "Stylish"]
            }
            
            terms = category_terms.get(category, ["Classic"])
            for term in terms:
                new_name = f"{color} {term} {components.get('item_type', '')}"
                if self.is_unique(new_name):
                    suggestions.append(new_name)
                    if len(suggestions) >= 5:
                        break
        
        # Strategy 4: Add gender-specific terms
        if len(suggestions) < 5:
            gender_terms = {
                "men": ["Men's", "Masculine", "Gentleman's"],
                "women": ["Women's", "Feminine", "Lady's"],
                "unisex": ["Unisex", "Universal", "Gender-neutral"]
            }
            
            terms = gender_terms.get(gender, [])
            for term in terms:
                new_name = f"{term} {base_name}"
                if self.is_unique(new_name):
                    suggestions.append(new_name)
                    if len(suggestions) >= 5:
                        break
        
        return suggestions[:5]
    
    def get_brand_name_suggestions(self, base_name: str) -> List[str]:
        """Generate unique brand name suggestions based on a base name.
        
        Args:
            base_name: Original brand name that needs to be made unique
            
        Returns:
            List of unique brand name suggestions
        """
        suggestions = []
        
        # Strategy 1: Add descriptive modifiers
        brand_modifiers = [
            "Artisan", "Heritage", "Modern", "Eco", "Sustainable", 
            "Natural", "Organic", "Handcrafted", "Bespoke", "Premium"
        ]
        
        for modifier in brand_modifiers:
            new_name = f"{modifier} {base_name}"
            if self.is_unique(new_name):
                suggestions.append(new_name)
                if len(suggestions) >= 5:
                    break
        
        # Strategy 2: Add location-inspired terms
        if len(suggestions) < 5:
            location_terms = [
                "Pacific", "Coastal", "Mountain", "Valley", "Riverside",
                "Harbor", "Meadow", "Forest", "Canyon", "Summit"
            ]
            
            for term in location_terms:
                new_name = f"{term} {base_name}"
                if self.is_unique(new_name):
                    suggestions.append(new_name)
                    if len(suggestions) >= 5:
                        break
        
        # Strategy 3: Add nature-inspired terms
        if len(suggestions) < 5:
            nature_terms = [
                "Wild", "Natural", "Earth", "Sky", "Ocean",
                "Mountain", "River", "Forest", "Meadow", "Valley"
            ]
            
            for term in nature_terms:
                new_name = f"{term} {base_name}"
                if self.is_unique(new_name):
                    suggestions.append(new_name)
                    if len(suggestions) >= 5:
                        break
        
        return suggestions[:5]
    
    def get_collection_name_suggestions(self, base_name: str, season: str, category: str) -> List[str]:
        """Generate unique collection name suggestions based on a base name.
        
        Args:
            base_name: Original collection name that needs to be made unique
            season: Collection season
            category: Collection category
            
        Returns:
            List of unique collection name suggestions
        """
        suggestions = []
        
        # Strategy 1: Add seasonal modifiers
        seasonal_modifiers = {
            "Spring": ["Spring", "Bloom", "Renewal", "Awakening"],
            "Summer": ["Summer", "Solstice", "Coastal", "Breeze"],
            "Fall": ["Fall", "Autumn", "Harvest", "Golden"],
            "Winter": ["Winter", "Frost", "Alpine", "Cozy"],
            "All-Season": ["Year-Round", "Timeless", "Versatile", "Essential"]
        }
        
        season_terms = seasonal_modifiers.get(season, ["Classic"])
        for term in season_terms:
            new_name = f"{term} {base_name}"
            if self.is_unique(new_name):
                suggestions.append(new_name)
                if len(suggestions) >= 5:
                    break
        
        # Strategy 2: Add category-specific terms
        if len(suggestions) < 5:
            category_terms = {
                "Everyday": ["Daily", "Essential", "Core", "Basic"],
                "Work": ["Professional", "Office", "Business", "Corporate"],
                "Active": ["Performance", "Athletic", "Sport", "Dynamic"],
                "Outdoor": ["Adventure", "Exploration", "Wilderness", "Trail"]
            }
            
            terms = category_terms.get(category, ["Classic"])
            for term in terms:
                new_name = f"{term} {base_name}"
                if self.is_unique(new_name):
                    suggestions.append(new_name)
                    if len(suggestions) >= 5:
                        break
        
        # Strategy 3: Add descriptive modifiers
        if len(suggestions) < 5:
            descriptive_modifiers = [
                "Signature", "Limited", "Premium", "Exclusive", "Heritage",
                "Modern", "Contemporary", "Classic", "Refined", "Elegant"
            ]
            
            for modifier in descriptive_modifiers:
                new_name = f"{modifier} {base_name}"
                if self.is_unique(new_name):
                    suggestions.append(new_name)
                    if len(suggestions) >= 5:
                        break
        
        return suggestions[:5]
    
    def _extract_pattern(self, name: str) -> str:
        """Extract naming pattern from a product name.
        
        Args:
            name: Product name
            
        Returns:
            Naming pattern (e.g., "Color + Style + Item")
        """
        # Simple pattern extraction - can be enhanced
        words = name.split()
        if len(words) >= 3:
            return f"{words[0]} + {words[1]} + {words[2]}"
        elif len(words) == 2:
            return f"{words[0]} + {words[1]}"
        else:
            return name
    
    def _parse_name_components(self, name: str) -> Dict[str, str]:
        """Parse name into components.
        
        Args:
            name: Product name
            
        Returns:
            Dictionary of name components
        """
        words = name.split()
        components = {}
        
        if len(words) >= 1:
            components['color'] = words[0]
        if len(words) >= 2:
            components['style'] = words[1]
        if len(words) >= 3:
            components['item_type'] = ' '.join(words[2:])
        
        return components
    
    def get_duplicate_analysis(self, names: List[str]) -> Dict[str, List[str]]:
        """Analyze duplicates in a list of names.
        
        Args:
            names: List of product names
            
        Returns:
            Dictionary mapping duplicate names to their occurrences
        """
        name_counts = defaultdict(list)
        
        for i, name in enumerate(names):
            name_counts[name].append(i)
        
        duplicates = {name: indices for name, indices in name_counts.items() if len(indices) > 1}
        return duplicates


def deduplicate_product_names(products: List[Dict]) -> List[Dict]:
    """Deduplicate product names in a list of products.
    
    Args:
        products: List of product dictionaries
        
    Returns:
        List of products with unique names
    """
    validator = NameValidator()
    updated_products = []
    
    for product in products:
        original_name = product['name']
        
        if validator.is_unique(original_name):
            # Name is unique, keep it
            validator.add_name(original_name)
            updated_products.append(product)
        else:
            # Name is duplicate, generate new name
            suggestions = validator.get_name_suggestions(
                original_name,
                product.get('category', ''),
                product.get('gender', ''),
                product.get('colors', '').split('|')[0] if product.get('colors') else ''
            )
            
            if suggestions:
                new_name = suggestions[0]
                product['name'] = new_name
                validator.add_name(new_name)
                updated_products.append(product)
                print(f"Renamed duplicate: '{original_name}' -> '{new_name}'")
            else:
                # Fallback: add unique suffix
                new_name = f"{original_name} (Style {len(validator.used_names) + 1})"
                product['name'] = new_name
                validator.add_name(new_name)
                updated_products.append(product)
                print(f"Renamed duplicate with suffix: '{original_name}' -> '{new_name}'")
    
    return updated_products


def deduplicate_brand_names(brands: List[Dict]) -> List[Dict]:
    """Deduplicate brand names in a list of brands.
    
    Args:
        brands: List of brand dictionaries
        
    Returns:
        List of brands with unique names
    """
    validator = NameValidator()
    updated_brands = []
    
    for brand in brands:
        original_name = brand['name']
        
        if validator.is_unique(original_name):
            # Name is unique, keep it
            validator.add_name(original_name)
            updated_brands.append(brand)
        else:
            # Name is duplicate, generate new name
            suggestions = validator.get_brand_name_suggestions(original_name)
            
            if suggestions:
                new_name = suggestions[0]
                brand['name'] = new_name
                validator.add_name(new_name)
                updated_brands.append(brand)
                print(f"Renamed duplicate brand: '{original_name}' -> '{new_name}'")
            else:
                # Fallback: add unique suffix
                new_name = f"{original_name} (Brand {len(validator.used_names) + 1})"
                brand['name'] = new_name
                validator.add_name(new_name)
                updated_brands.append(brand)
                print(f"Renamed duplicate brand with suffix: '{original_name}' -> '{new_name}'")
    
    return updated_brands


def deduplicate_collection_names(collections: List[Dict]) -> List[Dict]:
    """Deduplicate collection names in a list of collections.
    
    Args:
        collections: List of collection dictionaries
        
    Returns:
        List of collections with unique names
    """
    validator = NameValidator()
    updated_collections = []
    
    for collection in collections:
        original_name = collection['name']
        
        if validator.is_unique(original_name):
            # Name is unique, keep it
            validator.add_name(original_name)
            updated_collections.append(collection)
        else:
            # Name is duplicate, generate new name
            suggestions = validator.get_collection_name_suggestions(
                original_name,
                collection.get('season', ''),
                collection.get('category', '')
            )
            
            if suggestions:
                new_name = suggestions[0]
                collection['name'] = new_name
                validator.add_name(new_name)
                updated_collections.append(collection)
                print(f"Renamed duplicate collection: '{original_name}' -> '{new_name}'")
            else:
                # Fallback: add unique suffix
                new_name = f"{original_name} (Collection {len(validator.used_names) + 1})"
                collection['name'] = new_name
                validator.add_name(new_name)
                updated_collections.append(collection)
                print(f"Renamed duplicate collection with suffix: '{original_name}' -> '{new_name}'")
    
    return updated_collections 