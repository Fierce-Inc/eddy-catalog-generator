"""CLI entry point for the catalog generator."""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline import main


if __name__ == "__main__":
    asyncio.run(main()) 