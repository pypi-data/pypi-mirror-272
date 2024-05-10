from typing import TYPE_CHECKING

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class AuditPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def get_audit_logs(
        self, guild_id: int, limit=50, before=None, user_id=None, action_type=None
    ) -> ClientResponse:
        """Get the audit logs for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild.
        limit : int
            The number of entries to return.
        before : int
            Entries that preceded a specific audit log entry ID
        user_id : int
            The ID of the user to filter the logs by.
        action_type : int
            The type of action to filter the logs by.

        Returns
        -------
        ClientResponse
            A list of audit logs.

        Raises
        ------
        InvalidParams
            The limit is not between 1 and 100.
        """
        if 1 > limit or limit > 100:
            raise InvalidParams("limit must be between 1 and 100")

        path = f"/guilds/{guild_id}/audit-logs"

        params = {"limit": limit}
        if before is not None:
            params["before"] = before
        if user_id is not None:
            params["user_id"] = user_id
        if action_type is not None:
            params["action_type"] = action_type

        return await self._client._request("GET", path, params=params)
