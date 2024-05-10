from typing import TYPE_CHECKING, Any, List, Optional

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class InteractionsPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def create_interaction_response(
        self,
        interaction_id: int,
        interaction_token: str,
        type: int,
        data: Optional[dict] = None,
    ) -> ClientResponse:
        """Create an interaction response.

        Parameters
        ----------
        interaction_id : int
            The ID of the interaction to create the response for.
        interaction_token : str
            The token of the interaction to create the response for.
        type : int
            The type of response to create.
        data : Any, optional
            An optional response message, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/interactions/{interaction_id}/{interaction_token}/callback"
        payload = {"type": type}
        if data is not None:
            payload["data"] = data  # type: ignore
        return await self._client._request("POST", path, json=payload)

    async def get_original_interaction_response(
        self, application_id: int, interaction_token: str
    ) -> ClientResponse:
        """Get the original interaction response.

        Parameters
        ----------
        application_id : int
            The ID of the application to get the original interaction response for.
        interaction_token : str
            The token of the interaction to get the original interaction response for.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/webhooks/{application_id}/{interaction_token}/messages/@original"
        return await self._client._request("GET", path)

    async def edit_original_interaction_response(
        self,
        application_id: int,
        interaction_token: str,
        content: Optional[Optional[str]] = None,
        embeds: Optional[List[dict]] = None,
        allowed_mentions: Any = None,
        components: Optional[List[Any]] = None,
    ) -> ClientResponse:
        """Edit the original interaction response.

        Parameters
        ----------
        application_id : int
            The ID of the application to edit the original interaction response for.
        interaction_token : str
            The token of the interaction to edit the original interaction response for.
        content : str, optional
            The message contents (up to 2000 characters), by default None
        embeds : List[dict], optional
            Embedded rich content, by default None
        allowed_mentions : Any, optional
            Allowed mentions for the message, by default None
        components : List[Any], optional
            The components to include with the message, by default None

        Returns
        -------
        ClientResponse
            A message object.
        """
        path = f"/webhooks/{application_id}/{interaction_token}/messages/@original"

        payload = {
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
        }

        return await self._client._request("PATCH", path, json=payload)

    async def delete_original_interaction_response(
        self, application_id: int, interaction_token: str
    ) -> ClientResponse:
        """Delete the original interaction response.

        Parameters
        ----------
        application_id : int
            The ID of the application to delete the original interaction response for.
        interaction_token : str
            The token of the interaction to delete the original interaction response for.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/webhooks/{application_id}/{interaction_token}/messages/@original"
        return await self._client._request("DELETE", path)

    async def create_followup_message(
        self,
        application_id: int,
        interaction_token: str,
        content: Optional[str] = None,
        tts: Optional[bool] = None,
        embeds: Optional[List[dict]] = None,
        allowed_mentions: Any = None,
        components: Optional[List[Any]] = None,
    ) -> ClientResponse:
        """Create a followup message.

        Parameters
        ----------
        application_id : int
            The ID of the application to create the followup message for.
        interaction_token : str
            The token of the interaction to create the followup message for.
        content : str, optional
            The message contents (up to 2000 characters), by default None
        tts : bool, optional
            True if this is a TTS message, by default None
        embeds : List[dict], optional
            Embedded rich content, by default None
        allowed_mentions : Any, optional
            Allowed mentions for the message, by default None
        components : List[Any], optional
            The components to include with the message, by default None

        Returns
        -------
        ClientResponse
            A message object.
        """
        path = f"/webhooks/{application_id}/{interaction_token}"

        payload = {}

        if content is not None:
            payload["content"] = content
        if tts is not None:
            payload["tts"] = tts
        if embeds is not None:
            payload["embeds"] = embeds
        if allowed_mentions is not None:
            payload["allowed_mentions"] = allowed_mentions
        if components is not None:
            payload["components"] = components

        return await self._client._request("POST", path, json=payload)

    async def get_followup_message(
        self, application_id: int, interaction_token: str, message_id: int
    ) -> ClientResponse:
        """Get a followup message.

        Parameters
        ----------
        application_id : int
            The ID of the application to get the followup message for.
        interaction_token : str
            The token of the interaction to get the followup message for.
        message_id : int
            The ID of the message to get.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/webhooks/{application_id}/{interaction_token}/messages/{message_id}"
        return await self._client._request("GET", path)

    async def edit_followup_message(
        self,
        application_id: int,
        interaction_token: str,
        message_id: int,
        content: Optional[str] = None,
        embeds: Optional[List[dict]] = None,
        allowed_mentions: Any = None,
        components: Optional[List[Any]] = None,
    ) -> ClientResponse:
        """Edit a followup message.

        Parameters
        ----------
        application_id : int
            The ID of the application to edit the followup message for.
        interaction_token : str
            The token of the interaction to edit the followup message for.
        message_id : int
            The ID of the message to edit.
        content : str, optional
            The message contents (up to 2000 characters), by default None
        embeds : List[dict], optional
            Embedded rich content, by default None
        allowed_mentions : Any, optional
            Allowed mentions for the message, by default None
        components : List[Any], optional
            The components to include with the message, by default None

        Returns
        -------
        ClientResponse
            A message object.
        """
        path = f"/webhooks/{application_id}/{interaction_token}/messages/{message_id}"

        payload = {
            "content": content,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "components": components,
        }

        return await self._client._request("PATCH", path, json=payload)

    async def delete_followup_message(
        self,
        application_id: int,
        interaction_token: str,
        message_id: int,
        thread_id: Optional[int] = None,
    ) -> ClientResponse:
        """Delete a followup message.

        Parameters
        ----------
        application_id : int
            The ID of the application to delete the followup message for.
        interaction_token : str
            The token of the interaction to delete the followup message for.
        message_id : int
            The ID of the message to delete.
        thread_id : id, optional
            ID of the thread the message is in, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        payload = {}
        if thread_id is not None:
            payload["thread_id"] = thread_id
        path = f"/webhooks/{application_id}/{interaction_token}/messages/{message_id}"
        return await self._client._request("DELETE", path, json=payload)
