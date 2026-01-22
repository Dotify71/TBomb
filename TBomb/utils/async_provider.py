import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional
from database.models import DatabaseManager
from health.checker import AsyncHealthChecker

class AsyncAPIProvider:
    def __init__(self, cc: str, target: str, mode: str, delay: float = 0):
        self.cc = cc
        self.target = target
        self.mode = mode
        self.delay = delay
        self.db = DatabaseManager()
        self.session = None
        self.healthy_apis = []
        self.current_index = 0
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        await self.refresh_healthy_apis()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def refresh_healthy_apis(self):
        """Get healthy APIs from database and verify them"""
        async with AsyncHealthChecker(self.db) as checker:
            self.healthy_apis = await checker.check_all_endpoints(self.cc, self.mode)
    
    def format_config(self, config: Dict) -> Dict:
        """Format API configuration with target values"""
        config_str = json.dumps(config)
        config_str = config_str.replace("{target}", self.target)
        config_str = config_str.replace("{cc}", self.cc)
        return json.loads(config_str)
    
    async def make_request(self, config: Dict) -> bool:
        """Make async API request"""
        try:
            # Parse configuration
            headers = json.loads(config.get('headers', '{}'))
            params = json.loads(config.get('params', '{}'))
            data = json.loads(config.get('data', '{}'))
            cookies = json.loads(config.get('cookies', '{}'))
            
            # Format with target values
            formatted_config = self.format_config({
                'headers': headers,
                'params': params,
                'data': data,
                'cookies': cookies
            })
            
            # Add default headers
            formatted_config['headers'].update({
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
            })
            
            # Make request
            async with self.session.request(
                method=config['method'],
                url=config['url'].replace("{target}", self.target).replace("{cc}", self.cc),
                headers=formatted_config['headers'],
                params=formatted_config['params'],
                data=formatted_config['data'] if config['method'] != 'GET' else None,
                cookies=formatted_config['cookies']
            ) as response:
                response_text = await response.text()
                identifier = config.get('identifier', '').lower()
                
                # Check if request was successful based on identifier
                if identifier and identifier in response_text.lower():
                    return True
                return 200 <= response.status < 400
                
        except Exception:
            return False
    
    async def hit(self) -> Optional[bool]:
        """Execute single API hit with health check"""
        if not self.healthy_apis:
            await self.refresh_healthy_apis()
            if not self.healthy_apis:
                return None
        
        # Apply delay
        if self.delay > 0:
            await asyncio.sleep(self.delay)
        
        # Get next API
        api_config = self.healthy_apis[self.current_index % len(self.healthy_apis)]
        self.current_index += 1
        
        # Make request
        success = await self.make_request(api_config)
        
        # Update health status in database
        self.db.update_api_health(
            api_config['endpoint_id'],
            200 if success else 400,
            0.5,  # Approximate response time
            success
        )
        
        return success
    
    async def batch_hit(self, count: int, max_concurrent: int = 10) -> Dict[str, int]:
        """Execute multiple hits concurrently"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def limited_hit():
            async with semaphore:
                return await self.hit()
        
        tasks = [limited_hit() for _ in range(count)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success = sum(1 for r in results if r is True)
        failed = sum(1 for r in results if r is False)
        errors = sum(1 for r in results if r is None or isinstance(r, Exception))
        
        return {
            'success': success,
            'failed': failed,
            'errors': errors,
            'total': len(results)
        }