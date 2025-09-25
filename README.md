# Eddy Catalog Generator

A synthetic catalog generator that creates realistic product data using OpenAI and LangChain, ensuring all content aligns with the provided brand guide.

## 🎯 Overview

This tool generates a complete synthetic catalog with:
- **Brands**: 5 unique brand profiles
- **Collections**: 20 seasonal collections
- **Products**: 10,000 SKUs with realistic details
- **Reviews**: 50,000 customer reviews (5 per product)

All content is generated using the provided brand guide to ensure consistency with the brand's values, tone, and target audience.

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd eddy-catalog-generator

# Install dependencies
pip install -e .

# Copy environment template
cp env.example .env

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

### 2. Run Generation

```bash
# Generate full catalog (10,000 products)
python -m src --out data/

# Generate smaller catalog for testing
python -m src --out data/ --products 100

# Use a specific brand guide and configuration
python -m src --out data/evergreen --brand-guide brand_guide_evergreen.md --brand-config evergreen.json
```

## 📁 Project Structure

```
eddy-catalog-generator/
├── docs/
│   ├── brand_guide_evergreen.md # Example brand guide
│   ├── brand_guide_vera_lux.md  # Example brand guide
│   └── evergreen.json           # Brand configuration (colors, categories, etc.)
├── src/
│   ├── schema.py               # Pydantic data models
│   ├── utils/
│   │   └── brand_context.py    # Brand guide loader & summarizer
│   ├── prompts.py              # LangChain prompt templates & config loader
│   ├── generators/
│   │   ├── brand_gen.py        # Brand generation
│   │   ├── collection_gen.py   # Collection generation
│   │   ├── product_gen.py      # Product generation
│   │   └── review_gen.py       # Review generation
│   ├── pipeline.py             # Main orchestration
│   └── __main__.py             # CLI entry point
├── pyproject.toml              # Project configuration
└── env.example                 # Environment variables template
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `TEMPERATURE_PRODUCT` | `0.7` | Creativity for products/collections |
| `TEMPERATURE_REVIEW` | `0.5` | Creativity for reviews |
| `BATCH_SIZE` | `50` | Products per API call |
| `MAX_RETRIES` | `3` | Retry attempts on failure |

### Generation Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--out` | `data/` | Output directory for CSVs |
| `--products` | `10000` | Number of products to generate |
| `--brand-guide` | `brand_guide.md` | Brand guide filename inside docs/ directory |
| `--brand-config` | `evergreen.json` | Brand configuration JSON filename inside docs/ directory |

### Brand Configuration

The `--brand-config` parameter specifies a JSON file containing brand-specific constants:

- **Gender Distribution**: Target audience breakdown (women/men/unisex percentages)
- **Product Categories**: Main categories and subcategories for products
- **Brand Colors**: Color palette for products
- **Size Ranges**: Available sizes for different genders
- **Price Bands**: Budget, mid, premium, and luxury price ranges
- **Fit Descriptions**: Available fit options
- **Sustainability Features**: Eco-friendly features to include

Example configuration structure:
```json
{
  "gender_distribution": {
    "women": 0.45,
    "men": 0.45,
    "unisex": 0.10
  },
  "product_categories": {
    "Everyday Apparel": ["Relaxed Denim", "Essential Tees"],
    "Work & Evening Wear": ["Tailored Blazers", "Smart Joggers"]
  },
  "brand_colors": ["Evergreen", "Ocean Blue", "Urban Mist"],
  "price_bands": {
    "budget": [25, 75],
    "premium": [150, 300]
  }
}
```

## 📋 Brand Configuration Format

The brand configuration JSON file defines all brand-specific parameters used during generation. Here's the complete structure:

```json
{
  "gender_distribution": {
    "women": 0.45,
    "men": 0.45,
    "unisex": 0.10
  },
  "product_categories": {
    "Everyday Apparel": [
      "Relaxed Denim",
      "Stretch Chinos", 
      "Essential Tees",
      "Knit Polos",
      "Tunic Shirts",
      "Wrap Dresses"
    ],
    "Work & Evening Wear": [
      "Tailored Blazers",
      "Smart Joggers",
      "Polished Midi Dresses",
      "Stretch Dress Pants",
      "Button-Down Shirts"
    ]
  },
  "brand_colors": [
    "Evergreen", "Ocean Blue", "Urban Mist", "Rust Peak",
    "Charcoal", "Cream", "Navy", "Olive", "Burgundy", "Sage"
  ],
  "size_ranges": {
    "women": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X"],
    "men": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X"],
    "unisex": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X"]
  },
  "price_bands": {
    "budget": [25, 75],
    "mid": [75, 150],
    "premium": [150, 300],
    "luxury": [300, 500]
  },
  "fit_descriptions": [
    "relaxed", "tailored", "slim", "oversized", "regular", 
    "comfortable", "fitted", "loose", "modern", "classic"
  ],
  "sustainability_features": [
    "Recycled polyester", "Organic cotton", "Tencel lyocell",
    "Repreve fibers", "Piñatex", "Low-impact dyes",
    "Circular design", "Repair-friendly construction",
    "Biodegradable packaging", "Fair trade certified"
  ]
}
```

## 📊 Output Files

The generator creates four CSV files:

### 1. `brands.csv`
- Brand ID, name, description, story
- Core values, target audience

### 2. `collections.csv`
- Collection ID, name, description
- Season, category, brand association
- Launch date, theme

### 3. `products.csv`
- Product ID (SKU), name, description
- Category, subcategory, gender
- Price, colors, sizes, materials
- Fit, sustainability features
- Care instructions, features

### 4. `reviews.csv`
- Review ID, product association
- Customer name, rating, title, content
- Verification status, helpful votes
- Review date, size/color purchased

## 🎨 Brand Integration

The generator uses both the brand guide and configuration to ensure:

- **Brand Consistency**: All content aligns with brand values and identity
- **Target Audience Alignment**: Products and messaging match brand positioning
- **Aesthetic Coherence**: Visual and tonal elements reflect brand guidelines
- **Value Integration**: Core brand values are embedded throughout the catalog
- **Authentic Voice**: Content maintains the brand's unique personality and tone
- **Configurable Parameters**: Colors, categories, pricing, and features match brand specifications

### Creating Custom Brand Configurations

1. **Copy the example**: Start with `docs/evergreen.json` as a template
2. **Modify values**: Update colors, categories, pricing, and other brand-specific elements
3. **Test configuration**: Use `--brand-config your_brand.json` to test your setup
4. **Create brand guide**: Write a corresponding brand guide markdown file
5. **Run generation**: Use both `--brand-guide` and `--brand-config` parameters

Example for a luxury brand:
```bash
python -m src --out data/luxury \
  --brand-guide brand_guide_luxury.md \
  --brand-config luxury.json \
  --products 5000
```

## 🔧 Development

### Adding New Features

1. **New Entity Types**: Add to `schema.py` with `to_csv_row()` method
2. **Custom Prompts**: Extend `prompts.py` with new templates
3. **Generation Logic**: Create new generator in `generators/`
4. **Pipeline Integration**: Update `pipeline.py` orchestration
5. **Brand Configurations**: Add new JSON configs in `docs/` directory

### Brand Configuration Schema

When creating new brand configurations, ensure your JSON includes all required fields:

- `gender_distribution`: Object with women/men/unisex percentages
- `product_categories`: Object with category names and subcategory arrays
- `brand_colors`: Array of color names
- `size_ranges`: Object with gender-specific size arrays
- `price_bands`: Object with band names and [min, max] price arrays
- `fit_descriptions`: Array of fit description strings
- `sustainability_features`: Array of sustainability feature strings

### Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/
```

## 📈 Performance

- **Brand Context**: Cached with `@lru_cache` for efficiency
- **Batch Processing**: 50 products per API call
- **Retry Logic**: Automatic retry on JSON parse errors
- **Progress Tracking**: tqdm progress bars for long operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Ensure your `.env` file exists and contains the API key
- Check that `python-dotenv` is installed

**JSON Parse Errors**
- The generator includes retry logic for failed generations
- Check your API key and rate limits

**Memory Issues with Large Catalogs**
- Reduce batch size in environment variables
- Generate smaller catalogs for testing

**Brand Configuration Errors**
- Ensure JSON file exists in `docs/` directory
- Validate JSON syntax using a JSON validator
- Check that all required fields are present in configuration
- Verify price bands use arrays `[min, max]` not objects

### Getting Help

- Check the logs for detailed error messages
- Verify your OpenAI API key has sufficient credits
- Ensure all dependencies are installed correctly 