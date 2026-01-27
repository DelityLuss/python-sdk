import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from .exceptions import AuthenticationError, APIError
from .resources import (
    AccountResource, 
    TeamResource, 
    UploadResource, 
    WebhookResource,
    ShortLinkResource,
    WhiteLabelResource
)

class MultiUploadClient:
    DEFAULT_BASE_URL = "https://api.multi-upload-tool.com/api/v1"

    def __init__(self, api_token: str, base_url: Optional[str] = None):
        """
        Initialize the Multi Upload Tool API client.

        Args:
            api_token (str): Your API token.
            base_url (str, optional): Base URL for the API. Defaults to official API.
        """
        self.api_token = api_token
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_token,
            "User-Agent": "MultiUploadTool-Python/0.1.0"
        })

        # Resources
        self.accounts = AccountResource(self)
        self.teams = TeamResource(self)
        self.uploads = UploadResource(self)
        self.webhooks = WebhookResource(self)
        self.short_links = ShortLinkResource(self)
        self.whitelabel = WhiteLabelResource(self)

    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Make an authenticated request to the API.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint (e.g., '/accounts')
            **kwargs: Arguments passed to requests.request
        """
        # Ensure endpoint starts with / for joining, but logic below handles it
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
        
        if response.status_code == 401:
            raise AuthenticationError("Invalid API Token")
        
        if 400 <= response.status_code < 500:
            try:
                error_data = response.json()
                message = error_data.get('message') or error_data.get('error') or "Client Error"
            except ValueError:
                message = response.text
            raise APIError(message, status_code=response.status_code, response=response)
            
        if response.status_code >= 500:
            raise APIError("Server Error", status_code=response.status_code, response=response)

        try:
            return response.json()
        except ValueError:
            # Handle empty responses or non-JSON responses
            return {}

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
