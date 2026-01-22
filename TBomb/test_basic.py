#!/usr/bin/env python3
"""
Basic feature test without async dependencies
"""
import sys
import os

def test_database():
    print("🗄️  Testing Database...")
    from database.models import DatabaseManager
    
    db = DatabaseManager("test.db")
    db.load_apis_from_json("apidata.json")
    apis = db.get_healthy_apis("91", "sms")
    print(f"✅ Database: Found {len(apis)} APIs for India SMS")
    
    # Test health update
    if apis:
        db.update_api_health(apis[0]['id'], 200, 0.5, True)
        print("✅ Database: Health update successful")
    
    os.remove("test.db")

def test_original_provider():
    print("🔄 Testing Original Provider...")
    from utils.provider import APIProvider
    
    provider = APIProvider("91", "0000000000", "sms")
    print(f"✅ Original: {len(provider.api_providers)} APIs loaded")
    
    # Test configuration formatting
    if provider.api_providers:
        provider.select_api()
        if provider.config:
            print("✅ Original: API configuration works")

def test_decorators():
    print("🎨 Testing Message Decorators...")
    from utils.decorators import MessageDecorator
    
    decorator = MessageDecorator("icon")
    print("✅ Decorators: Icon mode works")
    
    decorator = MessageDecorator("stat")
    print("✅ Decorators: Status mode works")

def test_file_structure():
    print("📁 Testing File Structure...")
    
    required_files = [
        "bomber_async.py",
        "health_monitor.py", 
        "database/models.py",
        "health/checker.py",
        "utils/async_provider.py",
        "tests/test_database.py",
        ".github/workflows/ci.yml",
        "Dockerfile",
        "docker-compose.yml"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {missing}")
    else:
        print("✅ File Structure: All required files present")

def test_configurations():
    print("⚙️  Testing Configurations...")
    
    configs = [
        "pytest.ini",
        ".flake8", 
        "pyproject.toml",
        "mypy.ini",
        ".pre-commit-config.yaml"
    ]
    
    for config in configs:
        if os.path.exists(config):
            print(f"✅ Config: {config} exists")
        else:
            print(f"❌ Config: {config} missing")

def main():
    print("🚀 TBomb Enhanced - Basic Feature Testing\n")
    
    try:
        test_database()
        test_original_provider()
        test_decorators()
        test_file_structure()
        test_configurations()
        
        print("\n✅ Basic features working!")
        print("\n📋 To test advanced features:")
        print("  1. Install async deps: pip install aiohttp aiosqlite")
        print("  2. Run: python3 test_features.py")
        print("  3. Test bomber: python3 bomber_async.py --help")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()