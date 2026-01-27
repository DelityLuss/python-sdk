from typing import List, Dict, Any, Optional
from .base import Resource

class TeamResource(Resource):
    def get_current(self) -> Dict[str, Any]:
        """Get details of the current team context."""
        return self.client.request("GET", "/teams").get("data", {})

    def list_members(self) -> List[Dict[str, Any]]:
        """List members of the current team."""
        return self.client.request("GET", "/teams/members").get("data", [])

    def invite(self, email: Optional[str] = None, role: str = "MEMBER") -> Dict[str, Any]:
        """
        Invite a new member to the team.
        
        Args:
            email (str): Email of the user to invite.
            role (str): Role ('MEMBER' or 'ADMIN').
        """
        data = {
            "role": role
        }
        if email:
            data["email"] = email
        return self.client.request("POST", "/teams/invites", json=data).get("data", {})
    
    def update_member_role(self, member_id: int, role: str, isActive: bool) -> Dict[str, Any]:
        """
        Update the role of a team member.
        
        Args:
            member_id (int): ID of the team member.
            role (str): New role ('MEMBER' or 'ADMIN').
            isActive (bool): Whether the member is active.
        """
        data = {
            "role": role,
            "isActive": isActive
        }
        return self.client.request("PUT", f"/teams/members/{member_id}", json=data)
    
    def remove_member(self, member_id: int) -> Dict[str, Any]:
        """
        Remove a member from the team.
        
        Args:
            member_id (int): ID of the team member to remove.
        """
        return self.client.request("DELETE", f"/teams/members/{member_id}")