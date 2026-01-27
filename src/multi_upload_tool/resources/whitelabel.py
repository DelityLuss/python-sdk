from typing import List, Dict, Any, Optional, Union
from .base import Resource

class WhiteLabelResource(Resource):
    def list(self) -> List[Dict[str, Any]]:
        """List active white label connection links."""
        return self.client.request("GET", "/whitelabel/links").get("data", [])

    def create(self, platform: Optional[str] = None, expires_in_hours: int = 24, **kwargs) -> Dict[str, Any]:
        """
        Create a new white-label connection link.
        
        Args:
            platform (str, optional): 'tiktok' or 'youtube'.
            expires_in_hours (int): Expiration in hours. Default 24.
            **kwargs: Additional parameters (logoUrl, title, redirectUrl, tags).
        """
        data = {
            "expiresInHours": expires_in_hours
        }
        if platform:
            data['platform'] = platform
        
        data.update(kwargs)
        return self.client.request("POST", "/whitelabel/links", json=data).get("data", {})

    def delete(self, link_id: Union[int, str]) -> Dict[str, Any]:
        """Delete/Revoke a white label link."""
        return self.client.request("DELETE", f"/whitelabel/links/{link_id}")
