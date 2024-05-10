from typing import TYPE_CHECKING, Any, List, Optional, TypeVar

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient

import datetime
from discord_limits import helpers

ISO8601_timestamp = TypeVar("ISO8601_timestamp", str, bytes)


class ChannelPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def get_channel(self, channel_id: int) -> ClientResponse:
        """Get a channel by ID.

        Parameters
        ----------
        channel_id : int
            The ID of the channel you wish to get information about.

        Returns
        -------
        ClientResponse
            Channel information.
        """
        path = f"/channels/{channel_id}"
        return await self._client._request("GET", path)

    async def edit_channel(
        self, channel_id: int, *, reason: Optional[str] = None, **options: Any
    ) -> ClientResponse:
        """Update a channel's settings.

        Parameters
        ----------
        channel_id : int
            The ID of the channel you wish to edit.
        reason : Optional[str], optional
            A reason for this edit that will be displayed in the audit log, by default None
        options : Any
            The params required to update the required aspects of the channel.

        Returns
        -------
        ClientResponse
            A dict containing a channel object.
        """
        path = f"/channels/{channel_id}"
        valid_keys = (
            "name",
            "parent_id",
            "topic",
            "bitrate",
            "nsfw",
            "user_limit",
            "position",
            "permission_overwrites",
            "rate_limit_per_user",
            "type",
            "rtc_region",
            "video_quality_mode",
            "archived",
            "auto_archive_duration",
            "locked",
            "invitable",
            "default_auto_archive_duration",
            "flags",
        )
        payload = {k: v for k, v in options.items() if k in valid_keys}
        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_channel(
        self, channel_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete a channel, or close a private message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to be deleted/closed.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The responce from Discord.
        """
        path = f"/channels/{channel_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_channel_messages(
        self,
        channel_id: int,
        limit=50,
        before: Optional[int] = None,
        after: Optional[int] = None,
        around: Optional[int] = None,
    ) -> ClientResponse:
        """Get messages from a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get message from
        limit : int, optional
            Max number of messages to return (1-100), by default 50
        before : int, optional
            Get messages before this message ID, by default None
        after : int, optional
            Get messages after this message ID, by default None
        around : int, optional
            Get messages around this message ID, by default None

        Returns
        -------
        ClientResponse
            A list of message objects.

        Raises
        ------
        InvalidParams
            The limit is not between 1 and 100.
        """
        if 1 > limit or limit > 100:
            raise InvalidParams("limit must be between 1 and 100")
        path = f"/channels/{channel_id}/messages"

        params = {
            "limit": limit,
        }

        if before is not None:
            params["before"] = before
        if after is not None:
            params["after"] = after
        if around is not None:
            params["around"] = around

        return await self._client._request("GET", path, params=params)

    async def get_message(self, channel_id: int, message_id: int) -> ClientResponse:
        """Get a message from a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get message from.
        message_id : int
            The ID of the message that is to be retrieved.

        Returns
        -------
        ClientResponse
            A message object.
        """
        path = f"/channels/{channel_id}/messages/{message_id}"
        return await self._client._request("GET", path)

    async def create_message(
        self,
        channel_id: int,
        content: Optional[str] = None,
        tts: Optional[bool] = None,
        embeds: Optional[List[dict]] = None,
        allowed_mentions: Optional[dict] = None,
        message_reference: Optional[dict] = None,
        components: Optional[List[dict]] = None,
        sticker_ids: Optional[List[int]] = None,
    ) -> ClientResponse:
        """Post a message to a guild text or DM channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to send a message to.
        content : str, optional
            Message contents (up to 2000 characters), by default None
        tts : bool, optional
            true if this is a TTS message, by default None
        embeds : List[dict], optional
            An array of dicts containing embed data, by default None
        allowed_mentions : Any, optional
            Allowed mentions for the message, by default None
        message_reference : Any, optional
            Include to make your message a reply, by default None
        components : List[Any], optional
            An array of components to include with the message, by default None
        sticker_ids : List[int], optional
            IDs of up to 3 stickers in the server to send in the message, by default None

        Returns
        -------
        ClientResponse
            A message object

        Raises
        ------
        InvalidParams
            content, embeds or sticker_ids must be provided.
        """
        if content is None and embeds is None and sticker_ids is None:
            raise InvalidParams("content, embeds or sticker_ids must be provided")
        path = f"/channels/{channel_id}/messages"

        payload = {}

        if content is not None:
            payload["content"] = content
        if tts is not None:
            payload["tts"] = tts
        if embeds is not None:
            payload["embeds"] = embeds
        if allowed_mentions is not None:
            payload["allowed_mentions"] = allowed_mentions
        if message_reference is not None:
            payload["message_reference"] = message_reference
        if components is not None:
            payload["components"] = components
        if sticker_ids is not None:
            payload["sticker_ids"] = sticker_ids

        return await self._client._request("POST", path, json=payload)

    async def crosspost_message(
        self, channel_id: int, message_id: int
    ) -> ClientResponse:
        """Crosspost a message in a News Channel to following channels.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message to be corssposted is in.
        message_id : int
            The ID of the message to be crossposted.

        Returns
        -------
        ClientResponse
            A message object.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/crosspost"
        return await self._client._request("POST", path)

    async def add_reaction(
        self, channel_id: int, message_id: int, emoji: str
    ) -> ClientResponse:
        """Create a reaction for a message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to add a reaction to.
        emoji : str
            The emoji to react with.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        return await self._client._request("PUT", path)

    async def remove_own_reaction(
        self, channel_id: int, message_id: int, emoji: str
    ) -> ClientResponse:
        """Remove a reaction from a message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to remove a reaction from.
        emoji : str
            The emoji to remove.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        return await self._client._request("DELETE", path)

    async def remove_reaction(
        self, channel_id: int, message_id: int, emoji: str, member_id: int
    ) -> ClientResponse:
        """Remove a users reaction from a message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to remove a reaction from.
        emoji : str
            The emoji to remove.
        member_id : int
            The ID of the member thats reaction will be removed.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{member_id}"
        return await self._client._request("DELETE", path)

    async def get_reactions(
        self,
        channel_id: int,
        message_id: int,
        emoji: str,
        limit: int = 25,
        after: Optional[int] = None,
    ) -> ClientResponse:
        """Get a list of users that reacted with this emoji.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to get reactions from.
        emoji : str
            The emoji to get reactions for.
        limit : int, optional
            Max number of users to return (1-100), by default 25
        after : int, optional
            Get users after this user ID, by default None

        Returns
        -------
        ClientResponse
            A list of user objects.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
        params = {
            "limit": limit,
        }
        if after is not None:
            params["after"] = after

        return await self._client._request("GET", path, params=params)

    async def clear_reactions(self, channel_id: int, message_id: int) -> ClientResponse:
        """Deletes all reactions on a message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to clear reactions from.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/reactions"
        return await self._client._request("DELETE", path)

    async def clear_single_reaction(
        self, channel_id: int, message_id: int, emoji: str
    ) -> ClientResponse:
        """Deletes all the reactions for a given emoji on a message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to clear reactions from.
        emoji : str
            The emoji to clear reactions for.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
        return await self._client._request("DELETE", path)

    async def edit_message(
        self,
        channel_id: int,
        message_id: int,
        content: Optional[str] = None,
        embeds: Optional[List[dict]] = None,
        allowed_mentions: Optional[dict] = None,
        components: Optional[List[Any]] = None,
    ) -> ClientResponse:
        """Edit a previously sent message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to edit.
        content : str, optional
            Message contents (up to 2000 characters), by default None
        embeds : List[dict], optional
            An array of dicts containing embed data, by default None
        allowed_mentions : Any, optional
            Allowed mentions for the message, by default None
        components : List[Any], optional
            An array of components to include with the message, by default None

        Returns
        -------
        ClientResponse
            _description_
        """
        path = f"/channels/{channel_id}/messages/{message_id}"
        payload = {}

        if content is not None:
            payload["content"] = content
        if embeds is not None:
            payload["embeds"] = embeds
        if allowed_mentions is not None:
            payload["allowed_mentions"] = allowed_mentions
        if components is not None:
            payload["components"] = components

        return await self._client._request("PATCH", path, json=payload)

    async def delete_message(
        self, channel_id: int, message_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete a message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the message is in.
        message_id : int
            The ID of the message to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/messages/{message_id}"

        # Special case certain sub-rate limits
        # https://github.com/discord/discord-api-docs/issues/1092
        # https://github.com/discord/discord-api-docs/issues/1295
        difference = datetime.datetime.now(datetime.timezone.utc) - helpers.snowflake_time(
            int(message_id)
        )
        metadata = None
        if difference <= datetime.timedelta(seconds=10):
            metadata = "sub-10-seconds"
        elif difference >= datetime.timedelta(days=14):
            metadata = "older-than-two-weeks"

        return await self._client._request(
            "DELETE",
            path,
            headers={"X-Audit-Log-Reason": reason},
            metadata=metadata,
        )

    async def bulk_delete_messages(
        self, channel_id: int, message_ids: List[int], reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete multiple messages.

        Parameters
        ----------
        channel_id : int
            The ID of the channel the messages are in.
        message_ids : List[int]
            The IDs of the messages to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        helpers.check_bulk_delete_ids(message_ids)
        path = f"/channels/{channel_id}/messages/bulk-delete"
        payload = {
            "messages": message_ids,
        }
        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def edit_channel_permissions(
        self,
        channel_id: int,
        overwrite_id: int,
        allow: str,
        deny: str,
        type: int,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Edit the channel permission overwrites for a user or role in a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to edit permissions for.
        overwrite_id : int
            The ID of the user or role to edit permissions for.
        allow : str
            The bitwise value of all allowed permissions.
        deny : str
            The bitwise value of all disallowed permissions.
        type : int
            0 for a role or 1 for a member
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/permissions/{overwrite_id}"
        payload = {"allow": allow, "deny": deny, "type": type}
        return await self._client._request(
            "PUT", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_channel_invites(self, channel_id: int) -> ClientResponse:
        """Get a list of invites for a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get invites for.

        Returns
        -------
        ClientResponse
            A list of invite objects
        """
        path = f"/channels/{channel_id}/invites"
        return await self._client._request("GET", path)

    async def create_channel_invite(
        self,
        channel_id: int,
        *,
        reason: Optional[str] = None,
        max_age: int = 0,
        max_uses: int = 0,
        temporary: bool = False,
        unique: bool = True,
        target_type: Optional[int] = None,
        target_user_id: Optional[int] = None,
        target_application_id: Optional[int] = None,
    ) -> ClientResponse:
        """Create a new invite for a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to create an invite for.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        max_age : int, optional
            Duration of invite in seconds before expiry, by default 0
        max_uses : int, optional
            Max number of uses or 0 for unlimited, by default 0
        temporary : bool, optional
            Whether this invite only grants temporary membership, by default False
        unique : bool, optional
            If true, don't try to reuse a similar invite, by default True
        target_type : int, optional
            The type of target for this voice channel invite, by default None
        target_user_id : int, optional
            The id of the user whose stream to display for this invite, by default None
        target_application_id : int, optional
            The id of the embedded application to open for this invite, by default None

        Returns
        -------
        ClientResponse
            An invite object.
        """
        path = f"/channels/{channel_id}/invites"
        payload = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique,
        }

        if target_type:
            payload["target_type"] = target_type

        if target_user_id:
            payload["target_user_id"] = target_user_id

        if target_application_id:
            payload["target_application_id"] = str(target_application_id)

        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_channel_permissions(
        self, channel_id: int, overwrite_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete a channel permission overwrite for a user or role in a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to delete permissions for.
        overwrite_id : int
            The ID of the user or role to delete permissions for.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/permissions/{overwrite_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def follow_news_channel(
        self, channel_id: int, webhook_channel_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Follow a News Channel to send messages to a target channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to follow.
        webhook_channel_id : int
            ID of target channel.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/followers"
        payload = {
            "webhook_channel_id": webhook_channel_id,
        }
        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def start_typing(self, channel_id: int) -> ClientResponse:
        """Post a typing indicator for the specified channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to start the typing indicator in.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/typing"
        return await self._client._request("POST", path)

    async def get_pinned_messages(self, channel_id: int) -> ClientResponse:
        """Get a list of pinned messages in a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get pinned messages for.

        Returns
        -------
        ClientResponse
            A list of message objects.
        """
        path = f"/channels/{channel_id}/pins"
        return await self._client._request("GET", path)

    async def pin_message(
        self, channel_id: int, message_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Pin a message in a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to pin the message in.
        message_id : int
            The ID of the message to pin.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/pins/{message_id}"
        return await self._client._request(
            "PUT", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def unpin_message(
        self, channel_id: int, message_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Unpin a message in a channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to unpin the message in.
        message_id : int
            The ID of the message to unpin.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/pins/{message_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def add_group_recipient(
        self,
        channel_id: int,
        user_id: int,
        access_token: str,
        nickname: Optional[str] = None,
    ) -> ClientResponse:
        """Adds a recipient to a Group DM using their access token.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to add the recipient to.
        user_id : int
            The ID of the user to add as a recipient.
        access_token : str
            Access token of a user.
        nickname : str, optional
            Nickname of the user being added, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/recipients/{user_id}"
        payload = {"access_token": access_token, "nick": nickname}
        return await self._client._request("PUT", path, json=payload)

    async def remove_group_recipient(
        self, channel_id: int, user_id: int
    ) -> ClientResponse:
        """Removes a recipient from a Group DM.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to remove the recipient from.
        user_id : int
            The ID of the user to remove as a recipient.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/recipients/{user_id}"
        return await self._client._request("DELETE", path)

    async def start_thread_from_message(
        self,
        channel_id: int,
        message_id: int,
        *,
        name: str,
        auto_archive_duration: int,
        rate_limit_per_user: int,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Creates a new thread from an existing message.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to start the thread in.
        message_id : int
            The ID of the message to start the thread from.
        name : str
            1-100 character channel name.
        auto_archive_duration : int
            Duration in minutes to automatically archive the thread after recent activity.
        rate_limit_per_user : int
            Amount of seconds a user has to wait before sending another message.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A channel object.
        """
        path = f"/channels/{channel_id}/messages/{message_id}/threads"
        payload = {
            "name": name,
            "auto_archive_duration": auto_archive_duration,
            "rate_limit_per_user": rate_limit_per_user,
        }

        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def start_thread_without_message(
        self,
        channel_id: int,
        name: str,
        auto_archive_duration: int,
        type: int,
        invitable: bool = True,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Creates a new thread.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to start the thread in.
        name : str
            1-100 character channel name.
        auto_archive_duration : int
            Duration in minutes to automatically archive the thread after recent activity.
        type : int
            The type of thread to create.
        invitable : bool, optional
            Whether non-moderators can add other non-moderators to a thread, by default True
        rate_limit_per_user : int, optional
            Amount of seconds a user has to wait before sending another message, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A channel object.
        """
        path = f"/channels/{channel_id}/threads"
        payload = {
            "name": name,
            "auto_archive_duration": auto_archive_duration,
            "type": type,
            "invitable": invitable,
            "rate_limit_per_user": rate_limit_per_user,
        }

        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def start_thread_in_forum(
        self,
        channel_id: int,
        name: str,
        auto_archive_duration: int,
        message: dict,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Creates a new thread in a forum channel.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to start the thread in.
        name : str
            1-100 character channel name.
        auto_archive_duration : int
            Duration in minutes to automatically archive the thread after recent activity. 60, 1440, 4320 or 10080.
        rate_limit_per_user : int, optional
            Amount of seconds a user has to wait before sending another message (0-21600), by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        message : Any
            Params for a message to send in the thread.

        Returns
        -------
        ClientResponse
            A channel object, with a nested message object.

        Raises
        ------
        InvalidParams
            Invalid params were given.
        """
        path = f"/channels/{channel_id}/threads"
        if (
            message.get("content") is None
            and message.get("embeds") is None
            and message.get("sticker_ids") is None
        ):
            raise InvalidParams(
                "content, embeds or sticker_ids must be provided for the message"
            )
        elif (
            auto_archive_duration != 60
            or auto_archive_duration != 1440
            or auto_archive_duration != 4320
            or auto_archive_duration != 10080
        ):
            raise InvalidParams(
                "auto_archive_duration must equal to 60, 1440, 4320 or 10080"
            )
        elif 0 > rate_limit_per_user or rate_limit_per_user > 21600:  # type: ignore
            raise InvalidParams("rate_limit_per_user must be between 0 and 21600")
        valid_message_keys = (
            "content",
            "embeds",
            "allowed_mentions",
            "components",
            "sticker_ids",
        )
        payload = {
            "name": name[:100],
            "auto_archive_duration": auto_archive_duration,
            "rate_limit_per_user": rate_limit_per_user,
        }
        payload["message"] = {
            k: v for k, v in message.items() if k in valid_message_keys
        }
        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def join_thread(self, channel_id: int) -> ClientResponse:
        """Adds the current user to a thread.

        Parameters
        ----------
        channel_id : int
            The ID of the thread to join.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/thread-members/@me"
        return await self._client._request("PUT", path)

    async def add_user_to_thread(self, channel_id: int, user_id: int) -> ClientResponse:
        """Adds another member to a thread.

        Parameters
        ----------
        channel_id : int
            The ID of the thread to add a user to.
        user_id : int
            The ID of the user to add to the thread.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/thread-members/{user_id}"
        return await self._client._request("PUT", path)

    async def leave_thread(self, channel_id: int) -> ClientResponse:
        """Removes the current user from a thread.

        Parameters
        ----------
        channel_id : int
            The ID of the thread to leave.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/thread-members/@me"
        return await self._client._request("DELETE", path)

    async def remove_user_from_thread(
        self, channel_id: int, user_id: int
    ) -> ClientResponse:
        """Removes a member from a thread.

        Parameters
        ----------
        channel_id : int
            The ID of the thread to remove a user from.
        user_id : int
            The ID of the user to remove from the thread.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/channels/{channel_id}/thread-members/{user_id}"
        return await self._client._request("DELETE", path)

    async def get_thread_member(self, channel_id: int, user_id: int) -> ClientResponse:
        """Gets a thread member.

        Parameters
        ----------
        channel_id : int
            The ID of the thread to get a member from.
        user_id : int
            The ID of the user to get from the thread.

        Returns
        -------
        ClientResponse
            A thread member object.
        """
        path = f"/channels/{channel_id}/thread-members/{user_id}"
        return await self._client._request("GET", path)

    async def get_thread_members(self, channel_id: int) -> ClientResponse:
        """Gets all thread members.

        Parameters
        ----------
        channel_id : int
            The ID of the thread to get members from.

        Returns
        -------
        ClientResponse
            A list of thread member objects.
        """
        path = f"/channels/{channel_id}/thread-members"
        return await self._client._request("GET", path)

    async def get_public_archived_threads(
        self,
        channel_id: int,
        before: Optional[ISO8601_timestamp] = None,
        limit: int = 50,
    ) -> ClientResponse:
        """Returns archived threads in the channel that are public.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get archived threads from.
        before : ISO8601_timestamp, optional
            Returns threads before this timestamp, by default None
        limit : int, optional
            Optional maximum number of threads to return, by default 50

        Returns
        -------
        ClientResponse
            A list of archived threads in the channel that are public.
        """
        path = f"/channels/{channel_id}/threads/archived/public"

        params = {}
        if before:
            params["before"] = before
        params["limit"] = limit
        return await self._client._request("GET", path, params=params)

    async def get_private_archived_threads(
        self, channel_id: int, before: Optional[ISO8601_timestamp] = None, limit=50
    ) -> ClientResponse:
        """Returns archived threads in the channel that are private.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get archived threads from.
        before : ISO8601_timestamp, optional
            Returns threads before this timestamp, by default None
        limit : int, optional
            Optional maximum number of threads to return, by default 50

        Returns
        -------
        ClientResponse
            A list of archived threads in the channel that are private.
        """
        path = f"/channels/{channel_id}/threads/archived/private"

        params = {}
        if before:
            params["before"] = before
        params["limit"] = limit
        return await self._client._request("GET", path, params=params)

    async def get_joined_private_archived_threads(
        self, channel_id: int, before: Optional[int] = None, limit: int = 50
    ) -> ClientResponse:
        """Returns archived joined threads in the channel that are private.

        Parameters
        ----------
        channel_id : int
            The ID of the channel to get joined archived threads from.
        before : int, optional
            Returns threads before this id, by default None
        limit : int, optional
            Optional maximum number of threads to return, by default 50

        Returns
        -------
        ClientResponse
            A list of archived joined threads in the channel that are private.
        """
        path = f"/channels/{channel_id}/users/@me/threads/archived/private"
        params = {}
        if before:
            params["before"] = before
        params["limit"] = limit
        return await self._client._request("GET", path, params=params)
