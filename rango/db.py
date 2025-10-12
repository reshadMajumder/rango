#rango/db.py
from tortoise import Tortoise, run_async
import os
import sys
from pathlib import Path

# Add project root to path to import project settings
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

async def init_db():
    """Initialize database with project settings."""
    try:
        # Try to import project settings
        from myproject.project.settings import TORTOISE_ORM
        config = TORTOISE_ORM
        print(f"Using project settings: {config}")
    except ImportError as e:
        print(f"Could not import project settings: {e}")
        # Fallback to rango settings
        from rango.settings import TORTOISE_ORM
        config = TORTOISE_ORM
        print(f"Using rango settings: {config}")
    
    # Initialize Tortoise ORM
    print("Initializing Tortoise ORM...")
    await Tortoise.init(config=config)
    print("Generating database schema...")
    # Generate database schema
    await Tortoise.generate_schemas()
    print("Database schema generated!")

def init_db_sync():
    run_async(init_db)
