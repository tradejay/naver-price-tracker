"""
ScrapingBee & Proxy Collector with Exponential Backoff and Error Recovery.
"""
import time
import requests
from typing import Dict, Any, Optional

class ScrapingBeeClient:
    def __init__(self, api_key: str, base_url: str = "https://app.scrapingbee.com/api/v1/"):
        self.api_key = api_key
        self.base_url = base_url
        
    def fetch_page(self, target_url: str, render_js: bool = True, wait_ms: int = 2500, max_retries: int = 3) -> Optional[str]:
        """
        Fetches an anti-bot protected e-commerce page using ScrapingBee headless browser.
        """
        params = {
            'api_key': self.api_key,
            'url': target_url,
            'render_js': 'true' if render_js else 'false',
            'wait': str(wait_ms),
            'premium_proxy': 'true',
            'country_code': 'kr'
        }
        
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(self.base_url, params=params, timeout=120)
                if response.status_code == 200:
                    return response.text
                elif response.status_code in [429, 500, 502, 503, 504]:
                    wait_time = attempt * 3
                    time.sleep(wait_time)
                else:
                    return None
            except requests.exceptions.RequestException:
                time.sleep(attempt * 2)
                
        return None
