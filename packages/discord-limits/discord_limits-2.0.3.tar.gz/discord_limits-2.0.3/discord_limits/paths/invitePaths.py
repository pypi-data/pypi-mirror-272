from typing import TYPE_CHECKING, Optional

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class InvitePaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def get_invite(
        self,
        invite_id: str,
        *,
        with_counts: bool = True,
        with_expiration: bool = True,
        guild_scheduled_event_id: Optional[int] = None,
    ) -> ClientResponse:
        """Get an invite.

        Parameters
        ----------
        invite_id : str
            The ID of the invite to get.
        with_counts : bool, optional
            Whether the invite should contain approximate member counts, by default True
        with_expiration : bool, optional
            Whether the invite should contain the expiration date, by default True
        guild_scheduled_event_id : int, optional
            The guild scheduled event to include with the invite, by default None

        Returns
        -------
        ClientResponse
            An invite object.
        """
        path = f"/invites/{invite_id}"
        params = {
            "with_counts": with_counts,
            "with_expiration": with_expiration,
        }

        if guild_scheduled_event_id:
            params["guild_scheduled_event_id"] = guild_scheduled_event_id  # type: ignore

        return await self._client._request("GET", path, params=params)

    async def delete_invite(
        self, invite_id: str, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete an invite.

        Parameters
        ----------
        invite_id : str
            The ID of the invite to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            An invite object.
        """
        path = f"/invites/{invite_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )
