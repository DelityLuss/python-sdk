from typing import List, Dict, Any
from .base import Resource

class PinterestResource(Resource):
    def boards(self, account_id: int) -> List[Dict[str, Any]]:
        """
        Get boards for a connected Pinterest account.

        Args:
            account_id (int): ID of the Pinterest connected account.
        """
        res = self.client.request("GET", "/pinterest/boards", params={"accountId": account_id})
        return res.get("data", [])
