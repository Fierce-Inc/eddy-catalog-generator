# Eddy Catalog Generator

A synthetic catalog generator for Fierce Evergreen Apparel that creates realistic product data using OpenAI and LangChain, ensuring all content aligns with the brand guide.

## 🎯 Overview

This tool generates a complete synthetic catalog with:
- **Brands**: 5 unique brand profiles
- **Collections**: 20 seasonal collections
- **Products**: 10,000 SKUs with realistic details
- **Reviews**: 50,000 customer reviews (5 per product)

All content is generated using the Fierce Evergreen Apparel brand guide to ensure consistency with the brand's values, tone, and target audience.

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
```

## 📁 Project Structure

```
eddy-catalog-generator/
├── docs/
│   └── brand_guide.md          # Brand identity and guidelines
├── src/
│   ├── schema.py               # Pydantic data models
│   ├── utils/
│   │   └── brand_context.py    # Brand guide loader & summarizer
│   ├── prompts.py              # LangChain prompt templates
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

The generator uses the Fierce Evergreen Apparel brand guide to ensure:

- **Sustainability Focus**: Recycled materials, eco-friendly features
- **Body Positivity**: Inclusive sizing (XS-4X), unretouched imagery
- **Pacific Northwest Aesthetic**: Evergreen, Ocean Blue, Urban Mist colors
- **Everyday Versatility**: Desk-to-dinner adaptability
- **Empowerment**: Confidence-building messaging

## 🔧 Development

### Adding New Features

1. **New Entity Types**: Add to `schema.py` with `to_csv_row()` method
2. **Custom Prompts**: Extend `prompts.py` with new templates
3. **Generation Logic**: Create new generator in `generators/`
4. **Pipeline Integration**: Update `pipeline.py` orchestration

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

### Getting Help

- Check the logs for detailed error messages
- Verify your OpenAI API key has sufficient credits
- Ensure all dependencies are installed correctly 