from typing import List, Dict, Any, Optional
from .base import Resource

class WebhookResource(Resource):
    def list(self) -> List[Dict[str, Any]]:
        """List all webhooks."""
        return self.client.request("GET", "/webhooks").get("webhooks", [])

    def create(self, url: str, events: List[str], description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new webhook.
        
        Args:
            url (str): The URL to deliver webhooks to.
            events (List[str]): List of events to subscribe to (e.g., ['upload.completed']).
            description (str, optional): A description for the webhook.
        """
        data = {
            "url": url,
            "events": events
        }
        if description:
            data["description"] = description
            
        return self.client.request("POST", "/webhooks", json=data).get("data", {})
    
    def test(self, webhook_id: int) -> Dict[str, Any]:
        """Send a test payload to the specified webhook."""
        return self.client.request("POST", f"/webhooks/{webhook_id}/test")

    def delete(self, webhook_id: int) -> Dict[str, Any]:
        """Delete a webhook by ID."""
        return self.client.request("DELETE", f"/webhooks/{webhook_id}")
