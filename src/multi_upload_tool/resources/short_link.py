from typing import List, Dict, Any, Optional, Union
from .base import Resource

class ShortLinkResource(Resource):
    def list(self) -> List[Dict[str, Any]]:
        """List all short links."""
        return self.client.request("GET", "/short-links").get("data", [])

    def get(self, link_id: int) -> Dict[str, Any]:
        """Get short link details."""
        response = self.client.request("GET", f"/short-links/{link_id}")
        # Response is the link object directly, not wrapped
        return response if isinstance(response, dict) else {}

    def create(self, url: str, slug: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new short link.
        
        Args:
            url (str): Destination URL.
            slug (str, optional): Custom alias.
            **kwargs: Additional parameters (title, description, rules, etc.)
        """
        data = {'url': url}
        if slug:
            data['slug'] = slug
        data.update(kwargs)
        return self.client.request("POST", "/short-links", json=data).get("data", {})

    def update(self, link_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update a short link.
        
        Args:
            link_id (int): ID of the link.
            **kwargs: Fields to update (destination, isActive, rules, etc.)
        """
        response = self.client.request("PUT", f"/short-links/{link_id}", json=kwargs)
        # Response is the link object directly, not wrapped
        return response if isinstance(response, dict) else {}

    def delete(self, link_id: int) -> Dict[str, Any]:
        """Delete a short link."""
        return self.client.request("DELETE", f"/short-links/{link_id}")
