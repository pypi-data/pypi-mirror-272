from typing import TYPE_CHECKING, Optional

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class StickerPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def get_sticker(self, sticker_id: int) -> ClientResponse:
        """Get a sticker.

        Parameters
        ----------
        sticker_id : int
            The ID of the sticker to get.

        Returns
        -------
        ClientResponse
            A sticker object.
        """
        path = f"/stickers/{sticker_id}"
        return await self._client._request("GET", path)

    async def list_nitro_sticker_packs(self) -> ClientResponse:
        """List all nitro sticker packs.

        Returns
        -------
        ClientResponse
            A list of sticker pack objects.
        """
        path = "/sticker-packs"
        return await self._client._request("GET", path)

    async def list_guild_stickers(self, guild_id: int) -> ClientResponse:
        """List all stickers in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to list stickers for.

        Returns
        -------
        ClientResponse
            A list of sticker objects.
        """
        path = f"/guilds/{guild_id}/stickers"
        return await self._client._request("GET", path)

    async def get_guild_sticker(self, guild_id: int, sticker_id: int) -> ClientResponse:
        """Get a sticker in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the sticker for.
        sticker_id : int
            The ID of the sticker to get.

        Returns
        -------
        ClientResponse
            A sticker object.
        """
        path = f"/guilds/{guild_id}/stickers/{sticker_id}"
        return await self._client._request("GET", path)

    async def modify_guild_sticker(
        self,
        guild_id: int,
        sticker_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Modify a sticker in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to modify the sticker for.
        sticker_id : int
            The ID of the sticker to modify.
        name : str, optional
            Name of the sticker (2-30 characters), by default None
        description : str, optional
            Description of the sticker (2-100 characters), by default None
        tags : str, optional
            Autocomplete/suggestion tags for the sticker (max 200 characters), by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A sticker object.
        """
        path = f"/guilds/{guild_id}/stickers/{sticker_id}"
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if tags is not None:
            payload["tags"] = tags

        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_guild_sticker(
        self, guild_id: int, sticker_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete a sticker in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete the sticker for.
        sticker_id : int
            The ID of the sticker to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/stickers/{sticker_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )
