import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any


class APIClient:    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, 
                 timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        
        # Default headers
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if headers:
            self.headers.update(headers)
        
        # Setup session with retry policy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith('/'):
            return f"{self.base_url}{endpoint}"
        return f"{self.base_url}/{endpoint}"
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.get(url, params=params, headers=self.headers, timeout=self.timeout, **kwargs)
    
    def post(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.post(url, json=json, headers=self.headers, timeout=self.timeout, **kwargs)
    
    def put(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.put(url, json=json, headers=self.headers, timeout=self.timeout, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.delete(url, headers=self.headers, timeout=self.timeout, **kwargs)
    
    def close(self):
        self.session.close()
