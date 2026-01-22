#!/usr/bin/env python3
"""
Quick test runner for TBomb Enhanced features
"""
import asyncio
import sys
import os

async def test_database():
    print("🗄️  Testing Database...")
    from database.models import DatabaseManager
    
    db = DatabaseManager("test.db")
    db.load_apis_from_json("apidata.json")
    apis = db.get_healthy_apis("91", "sms")
    print(f"✅ Found {len(apis)} APIs for India SMS")
    os.remove("test.db")

async def test_health_checker():
    print("🔍 Testing Health Checker...")
    from database.models import DatabaseManager
    from health.checker import AsyncHealthChecker
    
    db = DatabaseManager("test.db")
    db.load_apis_from_json("apidata.json")
    
    async with AsyncHealthChecker(db) as checker:
        results = await checker.check_all_endpoints("91", "sms")
        print(f"✅ Health checked {len(results)} healthy APIs")
    
    os.remove("test.db")

async def test_async_provider():
    print("⚡ Testing Async Provider...")
    from utils.async_provider import AsyncAPIProvider
    
    # Test with dummy data (won't actually send)
    async with AsyncAPIProvider("91", "0000000000", "sms", delay=0.1) as provider:
        print(f"✅ Provider initialized with {len(provider.healthy_apis)} APIs")

def test_original_compatibility():
    print("🔄 Testing Original Compatibility...")
    from utils.provider import APIProvider
    
    provider = APIProvider("91", "0000000000", "sms")
    print(f"✅ Original provider works with {len(provider.api_providers)} APIs")

async def main():
    print("🚀 TBomb Enhanced - Feature Testing\n")
    
    try:
        await test_database()
        await test_health_checker()
        await test_async_provider()
        test_original_compatibility()
        
        print("\n✅ All features working correctly!")
        print("\n📋 Next steps:")
        print("  • Run full tests: python3 -m pytest tests/ -v")
        print("  • Test async bomber: python3 bomber_async.py")
        print("  • Test health monitor: python3 health_monitor.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())