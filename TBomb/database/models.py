import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "tbomb.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS api_endpoints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    method TEXT NOT NULL,
                    url TEXT NOT NULL,
                    country_code TEXT,
                    service_type TEXT NOT NULL,
                    data TEXT,
                    headers TEXT,
                    params TEXT,
                    cookies TEXT,
                    identifier TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    success_rate REAL DEFAULT 0.0,
                    last_checked TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS api_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint_id INTEGER,
                    status_code INTEGER,
                    response_time REAL,
                    is_healthy BOOLEAN,
                    error_message TEXT,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (endpoint_id) REFERENCES api_endpoints (id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_endpoints_country_service 
                ON api_endpoints(country_code, service_type, is_active);
            ''')
    
    def load_apis_from_json(self, json_path: str):
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        with sqlite3.connect(self.db_path) as conn:
            for service_type, countries in data.items():
                if service_type in ['sms', 'call', 'mail']:
                    for country_code, apis in countries.items():
                        for api in apis:
                            conn.execute('''
                                INSERT OR REPLACE INTO api_endpoints 
                                (name, method, url, country_code, service_type, data, headers, params, cookies, identifier)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                api['name'], api['method'], api['url'], 
                                country_code if country_code != 'multi' else None,
                                service_type, 
                                json.dumps(api.get('data', {})),
                                json.dumps(api.get('headers', {})),
                                json.dumps(api.get('params', {})),
                                json.dumps(api.get('cookies', {})),
                                api.get('identifier', '')
                            ))
    
    def get_healthy_apis(self, country_code: str, service_type: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM api_endpoints 
                WHERE (country_code = ? OR country_code IS NULL) 
                AND service_type = ? AND is_active = 1
                ORDER BY success_rate DESC
            ''', (country_code, service_type))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def update_api_health(self, endpoint_id: int, status_code: int, response_time: float, is_healthy: bool, error_message: str = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO api_health (endpoint_id, status_code, response_time, is_healthy, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (endpoint_id, status_code, response_time, is_healthy, error_message))
            
            conn.execute('''
                UPDATE api_endpoints SET last_checked = CURRENT_TIMESTAMP WHERE id = ?
            ''', (endpoint_id,))