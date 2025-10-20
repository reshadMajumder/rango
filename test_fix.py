#!/usr/bin/env python3
"""
Test script to verify database initialization works
"""
import asyncio
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

async def test_db_init():
    """Test database initialization"""
    try:
        from rango_api.db import init_db
        print("Testing database initialization...")
        await init_db()
        print("✅ Database initialization successful!")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

async def test_app_init():
    """Test RangoApp initialization"""
    try:
        from rango_api.core import RangoApp
        print("Testing RangoApp initialization...")
        app = RangoApp(debug=True)
        print("✅ RangoApp initialization successful!")
        return True
    except Exception as e:
        print(f"❌ RangoApp initialization failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Testing Rango Framework...")
    
    # Test 1: Database initialization
    db_success = await test_db_init()
    
    # Test 2: App initialization
    app_success = await test_app_init()
    
    if db_success and app_success:
        print("\n🎉 All tests passed! The framework should work correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
