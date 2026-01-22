#!/usr/bin/env python3
import asyncio
import argparse
import sys
import os
from typing import Dict
from database.models import DatabaseManager
from utils.async_provider import AsyncAPIProvider
from utils.decorators import MessageDecorator

class AsyncTBomb:
    def __init__(self):
        self.db = DatabaseManager()
        self.mesgdcrt = MessageDecorator("icon")
        
    async def initialize_database(self):
        """Initialize database with API data"""
        if os.path.exists("apidata.json"):
            self.db.load_apis_from_json("apidata.json")
            self.mesgdcrt.SuccessMessage("Database initialized with API data")
        else:
            self.mesgdcrt.WarningMessage("apidata.json not found, using empty database")
    
    def get_target_info(self, mode: str) -> tuple:
        """Get target information based on mode"""
        if mode in ["sms", "call"]:
            cc = input(self.mesgdcrt.CommandMessage("Enter country code (without +): ")).strip()
            target = input(self.mesgdcrt.CommandMessage(f"Enter target number: +{cc} ")).strip()
            return cc, target
        elif mode == "mail":
            target = input(self.mesgdcrt.CommandMessage("Enter target email: ")).strip()
            return None, target
        return None, None
    
    def get_bombing_params(self, mode: str) -> Dict:
        """Get bombing parameters"""
        max_limits = {"sms": 500, "call": 15, "mail": 200}
        limit = max_limits.get(mode, 100)
        
        while True:
            try:
                count = int(input(self.mesgdcrt.CommandMessage(f"Enter number of {mode.upper()} (Max {limit}): ")).strip())
                if count > limit:
                    self.mesgdcrt.WarningMessage(f"Capping to maximum limit: {limit}")
                    count = limit
                
                delay = float(input(self.mesgdcrt.CommandMessage("Enter delay (seconds): ")).strip())
                concurrent = int(input(self.mesgdcrt.CommandMessage("Enter concurrent requests (1-20): ")).strip())
                concurrent = max(1, min(20, concurrent))
                
                return {
                    'count': count,
                    'delay': delay,
                    'concurrent': concurrent
                }
            except ValueError:
                self.mesgdcrt.FailureMessage("Invalid input. Please enter numbers only.")
    
    async def execute_bombing(self, cc: str, target: str, mode: str, params: Dict):
        """Execute bombing with async provider"""
        self.mesgdcrt.SectionMessage("Starting bombing operation...")
        
        async with AsyncAPIProvider(cc or "", target, mode, params['delay']) as provider:
            # Check if APIs are available
            if not provider.healthy_apis:
                self.mesgdcrt.FailureMessage("No healthy APIs available for this target")
                return
            
            self.mesgdcrt.GeneralMessage(f"Found {len(provider.healthy_apis)} healthy APIs")
            self.mesgdcrt.GeneralMessage(f"Target: {cc or ''} {target}")
            self.mesgdcrt.GeneralMessage(f"Count: {params['count']}")
            self.mesgdcrt.GeneralMessage(f"Concurrent: {params['concurrent']}")
            
            # Execute bombing
            results = await provider.batch_hit(params['count'], params['concurrent'])
            
            # Display results
            self.mesgdcrt.SectionMessage("Bombing completed!")
            self.mesgdcrt.GeneralMessage(f"Total requests: {results['total']}")
            self.mesgdcrt.GeneralMessage(f"Successful: {results['success']}")
            self.mesgdcrt.GeneralMessage(f"Failed: {results['failed']}")
            self.mesgdcrt.GeneralMessage(f"Errors: {results['errors']}")
    
    async def run_interactive(self):
        """Run interactive mode"""
        await self.initialize_database()
        
        modes = {"1": "sms", "2": "call", "3": "mail"}
        
        print("\nAvailable Options:")
        for key, value in modes.items():
            print(f"[ {key} ] {value.upper()} BOMB")
        
        choice = input(self.mesgdcrt.CommandMessage("Enter choice: ")).strip()
        
        if choice not in modes:
            self.mesgdcrt.FailureMessage("Invalid choice")
            return
        
        mode = modes[choice]
        cc, target = self.get_target_info(mode)
        
        if not target:
            self.mesgdcrt.FailureMessage("Invalid target")
            return
        
        params = self.get_bombing_params(mode)
        await self.execute_bombing(cc, target, mode, params)
    
    async def run_cli(self, args):
        """Run CLI mode"""
        await self.initialize_database()
        
        mode = None
        if args.sms:
            mode = "sms"
        elif args.call:
            mode = "call"
        elif args.mail:
            mode = "mail"
        
        if not mode:
            self.mesgdcrt.FailureMessage("Please specify mode: --sms, --call, or --mail")
            return
        
        cc, target = self.get_target_info(mode)
        if not target:
            return
        
        params = self.get_bombing_params(mode)
        await self.execute_bombing(cc, target, mode, params)

async def main():
    parser = argparse.ArgumentParser(description="TBomb Async - Enhanced SMS/Call/Email Bomber")
    parser.add_argument("--sms", action="store_true", help="SMS bombing mode")
    parser.add_argument("--call", action="store_true", help="Call bombing mode")
    parser.add_argument("--mail", action="store_true", help="Email bombing mode")
    parser.add_argument("--init-db", action="store_true", help="Initialize database only")
    
    args = parser.parse_args()
    
    tbomb = AsyncTBomb()
    
    if args.init_db:
        await tbomb.initialize_database()
        return
    
    try:
        if any([args.sms, args.call, args.mail]):
            await tbomb.run_cli(args)
        else:
            await tbomb.run_interactive()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())