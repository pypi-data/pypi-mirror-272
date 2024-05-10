from typing import TYPE_CHECKING, List, Optional

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class EmojiPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def get_guild_emojis(self, guild_id: int) -> ClientResponse:
        """Gets all emojis in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get emojis from.

        Returns
        -------
        ClientResponse
            A list of emoji objects.
        """
        path = f"/guilds/{guild_id}/emojis"
        return await self._client._request("GET", path)

    async def get_guild_emoji(self, guild_id: int, emoji_id: int) -> ClientResponse:
        """Gets an emoji in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get an emoji from.
        emoji_id : int
            The ID of the emoji to get.

        Returns
        -------
        ClientResponse
            An emoji object.
        """
        path = f"/guilds/{guild_id}/emojis/{emoji_id}"
        return await self._client._request("GET", path)

    """
    async def create_guild_emoji(self, guild_id: int, name, image, *, roles = None, reason: str = None) -> ClientResponse:
        payload = {
            'name': name,
            'image': image,
            'roles': roles or [],
        }

        r = Route('POST', '/guilds/{guild_id}/emojis', guild_id=guild_id: int)
        return await self._client._request(r, json=payload, reason=reason)
    """

    async def edit_custom_emoji(
        self,
        guild_id: int,
        emoji_id: int,
        name: Optional[str] = None,
        roles: Optional[List[int]] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Edits a custom emoji.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit an emoji from.
        emoji_id : int
            The ID of the emoji to edit.
        name : str, optional
            Name of the emoji, by default None
        roles : List[int], optional
            A Llst of roles allowed to use this emoji, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            An emoji object.
        """
        path = f"/guilds/{guild_id}/emojis/{emoji_id}"
        payload = {}
        if name is not None:
            payload["name"] = name
        if roles is not None:
            payload["roles"] = roles
        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_custom_emoji(
        self, guild_id: int, emoji_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Deletes a custom emoji.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete an emoji from.
        emoji_id : int
            The ID of the emoji to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/emojis/{emoji_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )
