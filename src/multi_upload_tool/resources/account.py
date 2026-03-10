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

    def linkedin_pages(self, account_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get LinkedIn Pages/Organizations for a connected account.

        Args:
            account_id (int, optional): Filter by a specific LinkedIn account ID.
        """
        params = {}
        if account_id is not None:
            params['accountId'] = account_id
        res = self.client.request("GET", "/accounts/linkedin/pages", params=params)
        return res.get("pages", [])

    def delete(self, account_id: int) -> Dict[str, Any]:
        """Disconnect a connected account."""
        return self.client.request("DELETE", f"/accounts/{account_id}")
