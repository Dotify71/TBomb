import asyncio
import aiohttp
import time
import json
from typing import Dict, List, Optional
from database.models import DatabaseManager

class AsyncHealthChecker:
    def __init__(self, db_manager: DatabaseManager, timeout: int = 10):
        self.db = db_manager
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_endpoint_health(self, endpoint: Dict) -> Dict:
        start_time = time.time()
        try:
            # Parse JSON fields
            headers = json.loads(endpoint.get('headers', '{}'))
            params = json.loads(endpoint.get('params', '{}'))
            data = json.loads(endpoint.get('data', '{}'))
            cookies = json.loads(endpoint.get('cookies', '{}'))
            
            # Add default headers
            headers.update({
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
            })
            
            # Make test request
            async with self.session.request(
                method=endpoint['method'],
                url=endpoint['url'],
                headers=headers,
                params=params,
                data=data if endpoint['method'] != 'GET' else None,
                cookies=cookies
            ) as response:
                response_time = time.time() - start_time
                is_healthy = 200 <= response.status < 400
                
                return {
                    'endpoint_id': endpoint['id'],
                    'status_code': response.status,
                    'response_time': response_time,
                    'is_healthy': is_healthy,
                    'error_message': None
                }
                
        except Exception as e:
            response_time = time.time() - start_time
            return {
                'endpoint_id': endpoint['id'],
                'status_code': 0,
                'response_time': response_time,
                'is_healthy': False,
                'error_message': str(e)
            }
    
    async def check_all_endpoints(self, country_code: str, service_type: str) -> List[Dict]:
        endpoints = self.db.get_healthy_apis(country_code, service_type)
        
        tasks = [self.check_endpoint_health(endpoint) for endpoint in endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Update database with results
        for result in results:
            if isinstance(result, dict):
                self.db.update_api_health(**result)
        
        return [r for r in results if isinstance(r, dict) and r['is_healthy']]