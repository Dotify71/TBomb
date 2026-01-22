#!/usr/bin/env python3
"""
TBomb Enhanced Setup Script
Initializes database and sets up the enhanced TBomb environment
"""

import asyncio
import os
import sys
from database.models import DatabaseManager

async def setup_tbomb():
    print("🚀 Setting up Enhanced TBomb...")
    
    # Initialize database
    print("📊 Initializing database...")
    db = DatabaseManager()
    
    # Load API data if available
    if os.path.exists("apidata.json"):
        print("📡 Loading API endpoints...")
        db.load_apis_from_json("apidata.json")
        print("✅ API endpoints loaded successfully")
    else:
        print("⚠️  apidata.json not found - database initialized empty")
    
    # Create directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    print("✅ Setup completed successfully!")
    print("\n📋 Usage:")
    print("  • Interactive mode: python bomber_async.py")
    print("  • CLI mode: python bomber_async.py --sms")
    print("  • Health monitor: python health_monitor.py")
    print("  • Docker: docker-compose up")

if __name__ == "__main__":
    asyncio.run(setup_tbomb())