"""ID generation utilities for ensuring unique entity IDs."""

import uuid
from typing import List, Dict, Any


class IDGenerator:
    """Generates unique IDs for different entity types."""
    
    def __init__(self):
        """Initialize the ID generator."""
        self.used_ids = set()
    
    def generate_brand_ids(self, count: int) -> List[str]:
        """Generate unique brand IDs.
        
        Args:
            count: Number of brand IDs to generate
            
        Returns:
            List of unique brand IDs
        """
        ids = []
        for i in range(count):
            brand_id = f"brand_{uuid.uuid4().hex[:8]}"
            while brand_id in self.used_ids:
                brand_id = f"brand_{uuid.uuid4().hex[:8]}"
            ids.append(brand_id)
            self.used_ids.add(brand_id)
        return ids
    
    def generate_collection_ids(self, count: int) -> List[str]:
        """Generate unique collection IDs.
        
        Args:
            count: Number of collection IDs to generate
            
        Returns:
            List of unique collection IDs
        """
        ids = []
        for i in range(count):
            collection_id = f"collection_{uuid.uuid4().hex[:8]}"
            while collection_id in self.used_ids:
                collection_id = f"collection_{uuid.uuid4().hex[:8]}"
            ids.append(collection_id)
            self.used_ids.add(collection_id)
        return ids
    
    def generate_product_ids(self, count: int) -> List[str]:
        """Generate unique product IDs.
        
        Args:
            count: Number of product IDs to generate
            
        Returns:
            List of unique product IDs
        """
        ids = []
        for i in range(count):
            product_id = f"product_{uuid.uuid4().hex[:8]}"
            while product_id in self.used_ids:
                product_id = f"product_{uuid.uuid4().hex[:8]}"
            ids.append(product_id)
            self.used_ids.add(product_id)
        return ids
    
    def generate_review_ids(self, count: int) -> List[str]:
        """Generate unique review IDs.
        
        Args:
            count: Number of review IDs to generate
            
        Returns:
            List of unique review IDs
        """
        ids = []
        for i in range(count):
            review_id = f"review_{uuid.uuid4().hex[:8]}"
            while review_id in self.used_ids:
                review_id = f"review_{uuid.uuid4().hex[:8]}"
            ids.append(review_id)
            self.used_ids.add(review_id)
        return ids
    
    def get_id_batch(self, entity_type: str, count: int) -> List[str]:
        """Get a batch of IDs for a specific entity type.
        
        Args:
            entity_type: Type of entity ('brand', 'collection', 'product', 'review')
            count: Number of IDs to generate
            
        Returns:
            List of unique IDs
        """
        if entity_type == "brand":
            return self.generate_brand_ids(count)
        elif entity_type == "collection":
            return self.generate_collection_ids(count)
        elif entity_type == "product":
            return self.generate_product_ids(count)
        elif entity_type == "review":
            return self.generate_review_ids(count)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
    
    def reserve_ids(self, entity_type: str, count: int) -> List[str]:
        """Reserve IDs without generating them (for future use).
        
        Args:
            entity_type: Type of entity
            count: Number of IDs to reserve
            
        Returns:
            List of reserved IDs
        """
        return self.get_id_batch(entity_type, count) 