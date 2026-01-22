import pytest
import tempfile
import os
from database.models import DatabaseManager

class TestDatabaseManager:
    @pytest.fixture
    def temp_db(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
            db_path = f.name
        db = DatabaseManager(db_path)
        yield db
        os.unlink(db_path)
    
    def test_database_initialization(self, temp_db):
        assert os.path.exists(temp_db.db_path)
    
    def test_load_apis_from_json(self, temp_db):
        # Create test JSON data
        test_data = {
            "sms": {
                "91": [
                    {
                        "name": "test_api",
                        "method": "POST",
                        "url": "https://test.com/api",
                        "identifier": "success"
                    }
                ]
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump(test_data, f)
            json_path = f.name
        
        temp_db.load_apis_from_json(json_path)
        apis = temp_db.get_healthy_apis("91", "sms")
        
        assert len(apis) == 1
        assert apis[0]['name'] == 'test_api'
        
        os.unlink(json_path)
    
    def test_get_healthy_apis(self, temp_db):
        apis = temp_db.get_healthy_apis("91", "sms")
        assert isinstance(apis, list)
    
    def test_update_api_health(self, temp_db):
        # First load some test data
        test_data = {
            "sms": {
                "91": [{"name": "test", "method": "GET", "url": "http://test.com", "identifier": "ok"}]
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump(test_data, f)
            json_path = f.name
        
        temp_db.load_apis_from_json(json_path)
        apis = temp_db.get_healthy_apis("91", "sms")
        
        if apis:
            temp_db.update_api_health(apis[0]['id'], 200, 0.5, True)
        
        os.unlink(json_path)