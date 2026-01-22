#!/usr/bin/env python3
import asyncio
import time
from database.models import DatabaseManager
from health.checker import AsyncHealthChecker

class HealthMonitor:
    def __init__(self, check_interval: int = 3600):  # 1 hour
        self.db = DatabaseManager()
        self.check_interval = check_interval
        self.running = False
    
    async def monitor_all_apis(self):
        """Monitor all APIs for all countries and services"""
        print("Starting API health monitoring...")
        
        # Get all unique country codes and service types
        service_types = ['sms', 'call', 'mail']
        country_codes = ['91', '977', '218', None]  # None for multi-country APIs
        
        async with AsyncHealthChecker(self.db) as checker:
            for service_type in service_types:
                for country_code in country_codes:
                    if country_code:
                        print(f"Checking {service_type} APIs for country {country_code}")
                    else:
                        print(f"Checking multi-country {service_type} APIs")
                    
                    try:
                        healthy_apis = await checker.check_all_endpoints(
                            country_code or 'multi', service_type
                        )
                        print(f"Found {len(healthy_apis)} healthy APIs")
                    except Exception as e:
                        print(f"Error checking APIs: {e}")
                    
                    # Small delay between checks
                    await asyncio.sleep(1)
    
    async def run_continuous(self):
        """Run continuous monitoring"""
        self.running = True
        print(f"Health monitor started. Checking every {self.check_interval} seconds.")
        
        while self.running:
            try:
                await self.monitor_all_apis()
                print(f"Health check completed. Next check in {self.check_interval} seconds.")
                await asyncio.sleep(self.check_interval)
            except KeyboardInterrupt:
                print("Health monitor stopped by user")
                break
            except Exception as e:
                print(f"Error in health monitor: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    def stop(self):
        """Stop the monitor"""
        self.running = False

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="TBomb Health Monitor")
    parser.add_argument("--interval", type=int, default=3600, 
                       help="Check interval in seconds (default: 3600)")
    parser.add_argument("--once", action="store_true", 
                       help="Run once and exit")
    
    args = parser.parse_args()
    
    monitor = HealthMonitor(args.interval)
    
    try:
        if args.once:
            await monitor.monitor_all_apis()
        else:
            await monitor.run_continuous()
    except KeyboardInterrupt:
        print("\nHealth monitor stopped")

if __name__ == "__main__":
    asyncio.run(main())