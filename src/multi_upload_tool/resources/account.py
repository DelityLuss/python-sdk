from typing import List, Optional, Dict, Any
from .base import Resource

class AccountResource(Resource):
    def list(self, platform: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List connected accounts.
        
        Args:
            platform (str, optional): Filter by platform ('tiktok', 'youtube').
            status (str, optional): Filter by status ('active', 'revoked').
        """
        params = {}
        if platform:
            params['platform'] = platform
        if status:
            params['status'] = status
            
        return self.client.request("GET", "/accounts", params=params).get("data", [])

    def get(self, account_id: int) -> Dict[str, Any]:
        """Get account details."""
        return self.client.request("GET", f"/accounts/{account_id}").get("data", {})

    def get_preferences(self) -> Dict[str, Any]:
        """Get notification preferences."""
        return self.client.request("GET", "/accounts/preferences")
