import pytest
from unittest.mock import AsyncMock, patch
from health.checker import AsyncHealthChecker
from database.models import DatabaseManager

class TestAsyncHealthChecker:
    @pytest.fixture
    def mock_db(self):
        return AsyncMock(spec=DatabaseManager)
    
    @pytest.mark.asyncio
    async def test_health_checker_initialization(self, mock_db):
        async with AsyncHealthChecker(mock_db) as checker:
            assert checker.db == mock_db
            assert checker.timeout == 10
    
    @pytest.mark.asyncio
    async def test_check_endpoint_health_success(self, mock_db):
        endpoint = {
            'id': 1,
            'method': 'GET',
            'url': 'https://httpbin.org/status/200',
            'headers': '{}',
            'params': '{}',
            'data': '{}',
            'cookies': '{}'
        }
        
        async with AsyncHealthChecker(mock_db) as checker:
            result = await checker.check_endpoint_health(endpoint)
            
            assert result['endpoint_id'] == 1
            assert isinstance(result['response_time'], float)
            assert isinstance(result['is_healthy'], bool)
    
    @pytest.mark.asyncio
    async def test_check_endpoint_health_failure(self, mock_db):
        endpoint = {
            'id': 1,
            'method': 'GET',
            'url': 'https://invalid-url-that-does-not-exist.com',
            'headers': '{}',
            'params': '{}',
            'data': '{}',
            'cookies': '{}'
        }
        
        async with AsyncHealthChecker(mock_db) as checker:
            result = await checker.check_endpoint_health(endpoint)
            
            assert result['endpoint_id'] == 1
            assert result['is_healthy'] is False
            assert result['error_message'] is not None