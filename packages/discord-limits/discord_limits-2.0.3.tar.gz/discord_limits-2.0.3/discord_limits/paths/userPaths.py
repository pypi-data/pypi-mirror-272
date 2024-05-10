from typing import TYPE_CHECKING, List, Optional

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class UserPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def get_current_user(self) -> ClientResponse:
        """Get the current user.

        Returns
        -------
        ClientResponse
            A user object.
        """
        path = "/users/@me"
        return await self._client._request("GET", path)

    async def get_user(self, user_id: int) -> ClientResponse:
        """Get a user.

        Parameters
        ----------
        user_id : int
            The ID of the user to get.

        Returns
        -------
        ClientResponse
            A user object.
        """
        path = f"/users/{user_id}"
        return await self._client._request("GET", path)

    async def edit_current_user(self, username: str) -> ClientResponse:
        """Edit the current user.

        Parameters
        ----------
        username : str
            The new username.

        Returns
        -------
        ClientResponse
            A user object.
        """
        path = "/users/@me"
        payload = {"username": username}
        return await self._client._request("PATCH", path, json=payload)

    async def get_current_user_guilds(
        self,
        limit: int = 200,
        before: Optional[int] = None,
        after: Optional[int] = None,
    ) -> ClientResponse:
        """Get the current user's guilds.

        Parameters
        ----------
        limit : int, optional
            Max number of guilds to return (1-200), by default 200
        before : int, optional
            Get guilds before this guild ID, by default None
        after : int, optional
            Get guilds after this guild ID, by default None

        Returns
        -------
        ClientResponse
            A list of partial guild objects.

        Raises
        ------
        InvalidParams
            If the limit is not between 1 and 200.
        """
        path = "/users/@me/guilds"
        if 1 > limit or limit > 200:
            raise InvalidParams("limit must be between 1 and 200")

        params = {
            "limit": limit,
        }

        if before is not None:
            params["before"] = before
        if after is not None:
            params["after"] = after

        return await self._client._request("GET", path, params=params)

    async def get_current_user_guild_member(self, guild_id: int) -> ClientResponse:
        """Get the current user's guild member.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the member for.

        Returns
        -------
        ClientResponse
            A guild member object.
        """
        path = f"/users/@me/guilds/{guild_id}/member"
        return await self._client._request("GET", path)

    async def leave_guild(self, guild_id: int) -> ClientResponse:
        """Leave a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to leave.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/users/@me/guilds/{guild_id}"
        return await self._client._request("DELETE", path)

    async def create_DM(self, recipient_id: int) -> ClientResponse:
        """Open a DM.

        Parameters
        ----------
        recipient_id : int
            The ID of the user to open a DM with.

        Returns
        -------
        ClientResponse
            A DM channel object.
        """
        payload = {
            "recipient_id": recipient_id,
        }
        path = f"/users/@me/channels"

        return await self._client._request("POST", path, json=payload)

    async def create_group_DM(
        self, access_tokens: List[str], nicks: Optional[dict[int, str]] = None
    ) -> ClientResponse:
        """Open a group DM.

        Parameters
        ----------
        access_tokens : List[str]
            Access tokens of users that have granted your app the gdm.join scope
        nicks : Dict[int, str], optional
            A dictionary of user ids to their respective nicknames, by default None

        Returns
        -------
        ClientResponse
            A DM channel object.
        """
        payload = {
            "access_tokens": access_tokens,
        }
        path = f"/users/@me/channels"

        return await self._client._request("POST", path, json=payload)

    async def get_connections(self) -> ClientResponse:
        """Get the current user's connections.

        Returns
        -------
        ClientResponse
            A list of connection objects.
        """
        path = "/users/@me/connections"
        return await self._client._request("GET", path)
