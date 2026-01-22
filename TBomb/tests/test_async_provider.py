import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from utils.async_provider import AsyncAPIProvider

class TestAsyncAPIProvider:
    @pytest.mark.asyncio
    async def test_provider_initialization(self):
        with patch('utils.async_provider.DatabaseManager'):
            async with AsyncAPIProvider("91", "9876543210", "sms") as provider:
                assert provider.cc == "91"
                assert provider.target == "9876543210"
                assert provider.mode == "sms"
    
    @pytest.mark.asyncio
    async def test_format_config(self):
        with patch('utils.async_provider.DatabaseManager'):
            async with AsyncAPIProvider("91", "9876543210", "sms") as provider:
                config = {
                    "url": "https://api.com/{target}",
                    "data": {"phone": "{cc}{target}"}
                }
                formatted = provider.format_config(config)
                assert "9876543210" in formatted["url"]
                assert "919876543210" in str(formatted["data"])
    
    @pytest.mark.asyncio
    async def test_batch_hit(self):
        with patch('utils.async_provider.DatabaseManager'):
            with patch.object(AsyncAPIProvider, 'hit', new_callable=AsyncMock) as mock_hit:
                mock_hit.return_value = True
                
                async with AsyncAPIProvider("91", "9876543210", "sms") as provider:
                    results = await provider.batch_hit(5, 2)
                    
                    assert results['total'] == 5
                    assert results['success'] >= 0
                    assert mock_hit.call_count == 5