from typing import TYPE_CHECKING, Any, Optional

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class StagePaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def create_stage_instance(
        self, *, reason: Optional[str] = None, **payload: Any
    ) -> ClientResponse:
        """Create a stage instance.

        Parameters
        ----------
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        payload : Any
            The params for the JSON payload.

        Returns
        -------
        ClientResponse
            A stage instance object.
        """
        path = "/stage-instances"
        valid_keys = (
            "channel_id",
            "topic",
            "privacy_level",
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_stage_instance(self, channel_id: int) -> ClientResponse:
        """Get a stage instance.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get the stage instance for.

        Returns
        -------
        ClientResponse
            A stage instance object.
        """
        path = f"/stage-instances/{channel_id}"
        return await self._client._request("GET", path)

    async def edit_stage_instance(
        self, channel_id: int, *, reason: Optional[str] = None, **payload: Any
    ) -> ClientResponse:
        """Edit a stage instance.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to edit the stage instance for.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        payload : Any
            The params for the JSON payload.

        Returns
        -------
        ClientResponse
            A stage instance object.
        """
        path = f"/stage-instances/{channel_id}"
        valid_keys = (
            "topic",
            "privacy_level",
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_stage_instance(
        self, channel_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete a stage instance.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to delete the stage instance for.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/stage-instances/{channel_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )
