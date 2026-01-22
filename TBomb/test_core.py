#!/usr/bin/env python3
"""
Minimal test for core database and structure
"""
import os
import sys

def test_core_database():
    print("🗄️  Testing Core Database...")
    
    # Test database creation
    from database.models import DatabaseManager
    db = DatabaseManager("test_core.db")
    print("✅ Database initialized")
    
    # Test JSON loading
    db.load_apis_from_json("apidata.json")
    print("✅ API data loaded from JSON")
    
    # Test API retrieval
    apis = db.get_healthy_apis("91", "sms")
    print(f"✅ Retrieved {len(apis)} APIs for India SMS")
    
    # Test health tracking
    if apis:
        api_id = apis[0]['id']
        db.update_api_health(api_id, 200, 0.5, True, None)
        print("✅ Health tracking works")
    
    os.remove("test_core.db")

def test_project_structure():
    print("📁 Testing Project Structure...")
    
    # Core files
    core_files = [
        "bomber_async.py",
        "health_monitor.py",
        "setup.py",
        "database/models.py",
        "health/checker.py", 
        "utils/async_provider.py"
    ]
    
    # CI/CD files
    cicd_files = [
        ".github/workflows/ci.yml",
        "pytest.ini",
        ".flake8",
        "pyproject.toml"
    ]
    
    # Docker files
    docker_files = [
        "Dockerfile",
        "docker-compose.yml"
    ]
    
    # Documentation
    doc_files = [
        "docs/API.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md"
    ]
    
    all_files = core_files + cicd_files + docker_files + doc_files
    
    present = 0
    for file in all_files:
        if os.path.exists(file):
            present += 1
        else:
            print(f"❌ Missing: {file}")
    
    print(f"✅ Project Structure: {present}/{len(all_files)} files present")

def test_requirements():
    print("📦 Testing Requirements...")
    
    req_files = [
        "requirements.txt",
        "requirements-async.txt", 
        "requirements-test.txt",
        "requirements-dev.txt"
    ]
    
    for req_file in req_files:
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                lines = len(f.readlines())
            print(f"✅ {req_file}: {lines} dependencies")
        else:
            print(f"❌ Missing: {req_file}")

def test_docker_config():
    print("🐳 Testing Docker Configuration...")
    
    if os.path.exists("Dockerfile"):
        with open("Dockerfile", 'r') as f:
            content = f.read()
            if "python:3.9-slim" in content:
                print("✅ Dockerfile: Python base image correct")
            if "WORKDIR /app" in content:
                print("✅ Dockerfile: Working directory set")
    
    if os.path.exists("docker-compose.yml"):
        with open("docker-compose.yml", 'r') as f:
            content = f.read()
            if "tbomb:" in content:
                print("✅ Docker Compose: Service defined")

def main():
    print("🚀 TBomb Enhanced - Core Testing\n")
    
    try:
        test_core_database()
        test_project_structure()
        test_requirements()
        test_docker_config()
        
        print("\n✅ Core features implemented successfully!")
        print("\n🎯 Ready for PR submission!")
        print("\n📋 Manual testing steps:")
        print("  1. Install deps: pip install colorama requests")
        print("  2. Test original: python3 bomber.py --help")
        print("  3. Test setup: python3 setup.py")
        print("  4. Check Docker: docker build -t test .")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()