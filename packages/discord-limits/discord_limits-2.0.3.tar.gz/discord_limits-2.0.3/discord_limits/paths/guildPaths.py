from typing import TYPE_CHECKING, Any, List, TypeVar, Optional

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient

ISO8601_timestamp = TypeVar("ISO8601_timestamp", str, bytes)


class GuildPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    async def create_guild(
        self,
        name: str,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        roles: Optional[List[Any]] = None,
        channels: Optional[List[Any]] = None,
        afk_channel_id: Optional[int] = None,
        afk_timeout: Optional[int] = None,
        system_channel_id: Optional[int] = None,
        system_channel_flags: Optional[int] = None,
    ) -> ClientResponse:
        """Create a new guild.

        Parameters
        ----------
        name : str
            Name of the guild (2-100 characters).
        verification_level : int, optional
            The verification level for the guild, by default None
        default_message_notifications : int, optional
            The default message notification level, by default None
        explicit_content_filter : int, optional
            The explicit content filter level, by default None
        roles : List[Any], optional
            The roles for the guild, by default None
        channels : List[Any], optional
            The channels for the guild, by default None
        afk_channel_id : int, optional
            The ID for afk channel, by default None
        afk_timeout : int, optional
            The AFK timeout in seconds, by default None
        system_channel_id : int, optional
            The id of the channel where guild notices are sent, by default None
        system_channel_flags : int, optional
            System channel flags, by default None

        Returns
        -------
        ClientResponse
            A guild object.
        """
        path = "/guilds"
        payload = {
            "name": name,
        }
        if verification_level is not None:
            payload["verification_level"] = verification_level  # type: ignore
        if default_message_notifications is not None:
            payload["default_message_notifications"] = default_message_notifications  # type: ignore
        if explicit_content_filter is not None:
            payload["explicit_content_filter"] = explicit_content_filter  # type: ignore
        if roles is not None:
            payload["roles"] = roles  # type: ignore
        if channels is not None:
            payload["channels"] = channels  # type: ignore
        if afk_channel_id is not None:
            payload["afk_channel_id"] = afk_channel_id  # type: ignore
        if afk_timeout is not None:
            payload["afk_timeout"] = afk_timeout  # type: ignore
        if system_channel_id is not None:
            payload["system_channel_id"] = system_channel_id  # type: ignore
        if system_channel_flags is not None:
            payload["system_channel_flags"] = system_channel_flags  # type: ignore

        return await self._client._request("POST", path, json=payload)

    async def get_guild(
        self, guild_id: int, with_counts: bool = True
    ) -> ClientResponse:
        """Get a guild by ID.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get.
        with_counts : bool, optional
            When true, will return approximate member and presence counts for the guild, by default True

        Returns
        -------
        ClientResponse
            A guild object.
        """
        path = f"/guilds/{guild_id}"
        params = {"with_counts": with_counts}
        return await self._client._request("GET", path, params=params)

    async def get_guild_preview(self, guild_id: int) -> ClientResponse:
        """Get a guild preview by ID.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get.

        Returns
        -------
        ClientResponse
            A guild preview object.
        """
        path = f"/guilds/{guild_id}/preview"
        return await self._client._request("GET", path)

    async def edit_guild(
        self, guild_id: int, reason: Optional[str] = None, **options: Any
    ) -> ClientResponse:
        """Edit a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        options : Any
            The params required to update the required aspects of the guild.

        Returns
        -------
        ClientResponse
            A guild object.
        """
        path = f"/guilds/{guild_id}"

        payload = {}

        valid_keys = (
            "name",
            "region",
            "verification_level",
            "default_message_notifications",
            "explicit_content_filter",
            "afk_channel_id",
            "afk_timeout",
            "owner_id",
            "system_channel_id",
            "system_channel_flags",
            "rules_channel_id",
            "public_updates_channel_id",
            "preferred_locale",
            "features",
            "description",
            "premium_progress_bar_enabled",
        )
        payload.update(
            {k: v for k, v in options.items() if k in valid_keys and v is not None}
        )

        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_guild(self, guild_id: int) -> ClientResponse:
        """Delete a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}"
        return await self._client._request("DELETE", path)

    async def get_guild_channels(self, guild_id: int) -> ClientResponse:
        """Get a guild's channels.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get channels for.

        Returns
        -------
        ClientResponse
            A list of guild channel objects.
        """
        path = f"/guilds/{guild_id}/channels"
        return await self._client._request("GET", path)

    async def create_channel(
        self, guild_id: int, name: str, *, reason: Optional[str] = None, **options: Any
    ) -> ClientResponse:
        """Create a channel in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to create a channel in.
        name : str
            The channel name (1-100 characters).
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        options : Any
            The params required to create a channel of the required settings.

        Returns
        -------
        ClientResponse
            A channel object.
        """
        path = f"/guilds/{guild_id}/channels"

        payload = {
            "name": name,
        }

        valid_keys = (
            "type",
            "topic",
            "bitrate",
            "user_limit",
            "rate_limit_per_user",
            "position",
            "permission_overwrites",
            "parent_id",
            "nsfw",
            "default_auto_archive_duration",
        )
        payload.update(
            {k: v for k, v in options.items() if k in valid_keys and v is not None}
        )

        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def edit_channel_position(
        self,
        guild_id: int,
        channel_id: int,
        position: int,
        sync_permissions: bool,
        parent_id: int,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Edit a channel's position in the channel list.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit the channel position in.
        channel_id : int
            The ID of the channel to edit.
        position : int
            The new position of the channel.
        sync_permissions : bool
            Whether to sync permissions with the channel's new position.
        parent_id : int
            The ID of the new parent category for the channel.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/channels"

        payload = {
            "id": channel_id,
            "position": position,
            "lock_permissions": sync_permissions,
            "parent_id": parent_id,
        }

        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_active_threads(self, guild_id: int) -> ClientResponse:
        """Get a guild's active threads.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get active threads for.

        Returns
        -------
        ClientResponse
            A list of threads and members.
        """
        path = f"/guilds/{guild_id}/threads/active"
        return await self._client._request("GET", path)

    async def get_member(self, guild_id: int, member_id: int) -> ClientResponse:
        """Get a member in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get a member from.
        member_id : int
            The ID of the member to get.

        Returns
        -------
        ClientResponse
            A guild member object.
        """
        path = f"/guilds/{guild_id}/members/{member_id}"
        return await self._client._request("GET", path)

    async def get_members(
        self, guild_id: int, limit: int = 1, after: Optional[int] = None
    ) -> ClientResponse:
        """Get a list of members in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get members from.
        limit : int, optional
            Max number of members to return (1-1000), by default 1
        after : int, optional
            The highest user id in the previous page, by default None

        Returns
        -------
        ClientResponse
            A list of guild member objects.

        Raises
        ------
        InvalidParams
            If the limit is not between 1 and 1000.
        """
        if 1 > limit or limit > 1000:
            raise InvalidParams("limit must be between 1 and 1000")

        path = f"/guilds/{guild_id}/members"

        params = {
            "limit": limit,
        }
        if after is not None:
            params["after"] = after

        return await self._client._request("GET", path, params=params)

    async def search_guild_members(
        self, guild_id: int, query: str, limit: int = 1
    ) -> ClientResponse:
        """Search for members in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to search for members in.
        query : str
            The query to search for.
        limit : int, optional
            Max number of members to return (1-1000), by default 1

        Returns
        -------
        ClientResponse
            A list of guild member objects.

        Raises
        ------
        InvalidParams
            If the limit is not between 1 and 1000.
        """
        if 1 > limit or limit > 1000:
            raise InvalidParams("limit must be between 1 and 1000")

        path = f"/guilds/{guild_id}/members/search"

        params = {
            "limit": limit,
            "query": query,
        }
        return await self._client._request("GET", path, params=params)

    async def add_guild_member(
        self,
        guild_id: int,
        user_id: int,
        access_token: str,
        nick: Optional[str] = None,
        roles: Optional[List[int]] = None,
        mute: bool = False,
        deaf: bool = False,
    ) -> ClientResponse:
        """Add a member to a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to add a member to.
        user_id : int
            The ID of the user to add.
        access_token : str
            The access token of the user to add.
        nick : str, optional
            Value to set user's nickname to, by default None
        roles : List[int], optional
            Array of role ids the member is assigned, by default None
        mute : bool, optional
            Whether the user is muted in voice channels, by default False
        deaf : bool, optional
            Whether the user is deafened in voice channels, by default False

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/members/{user_id}"

        payload = {"access_token": access_token, "mute": mute, "deaf": deaf}

        if nick is not None:
            payload["nick"] = nick
        if roles is not None:
            payload["roles"] = roles

        return await self._client._request("PUT", path, json=payload)

    async def modify_guild_member(
        self,
        user_id: int,
        guild_id: int,
        nick: Optional[str] = None,
        roles: Optional[List[int]] = None,
        mute: Optional[bool] = None,
        deafen: Optional[bool] = None,
        channel_id: Optional[int] = None,
        timeout: Optional[ISO8601_timestamp] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Modify a member in a guild.

        Parameters
        ----------
        user_id : int
            The ID of the user to modify.
        guild_id : int
            The ID of the guild to modify the member in.
        nick : str, optional
            Value to set user's nickname to, by default None
        roles : List[int], optional
            Array of role ids the member is assigned, by default None
        mute : bool, optional
            Whether the user is muted in voice channels, by default None
        deafen : bool, optional
            Whether the user is deafened in voice channels, by default None
        channel_id : int, optional
            ID of channel to move user to, by default None
        timeout : ISO8601_timestamp, optional
            When the user's timeout will expire and the user will be able to communicate in the guild again, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/members/{user_id}"
        payload = {}
        if nick is not None:
            payload["nick"] = nick
        if roles is not None:
            payload["roles"] = roles
        if mute is not None:
            payload["mute"] = mute
        if deafen is not None:
            payload["deaf"] = deafen
        if channel_id is not None:
            payload["channel_id"] = channel_id
        if timeout is not None:
            payload["timeout"] = timeout

        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def modify_current_member(
        self, guild_id: int, nick: str, reason: Optional[str] = None
    ) -> ClientResponse:
        """Modify the current user in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to modify the member in.
        nick : str
            Value to set user's nickname to.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/members/@me"
        payload = {"nick": nick}
        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def add_role(
        self, guild_id: int, user_id: int, role_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Add a role to a member in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild that the users is in.
        user_id : int
            The ID of the user to add a role to.
        role_id : int
            The ID of the role to add.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
        return await self._client._request(
            "PUT", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def remove_role(
        self, guild_id: int, user_id: int, role_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Remove a role from a member in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild that the users is in.
        user_id : int
            The ID of the user to remove a role from.
        role_id : int
            The ID of the role to remove.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def kick(
        self, user_id: int, guild_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Kick a member from a guild.

        Parameters
        ----------
        user_id : int
            The ID of the user to kick.
        guild_id : int
            The ID of the guild to kick the member from.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/members/{user_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_bans(
        self,
        guild_id: int,
        limit: int = 1000,
        before: Optional[int] = None,
        after: Optional[int] = None,
    ) -> ClientResponse:
        """Get a list of all bans in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get bans from.
        limit : int, optional
            The number of users to return (up to maximum 1000), by default 1000
        before : int, optional
            Consider only users before given user id, by default None
        after : int, optional
            Consider only users after given user id, by default None

        Returns
        -------
        ClientResponse
            A list of ban objects.
        """
        path = f"/guilds/{guild_id}/bans"
        params = {
            "limit": limit,
        }
        if before is not None:
            params["before"] = before
        if after is not None:
            params["after"] = after

        return await self._client._request("GET", path, params=params)

    async def get_ban(self, user_id: int, guild_id: int) -> ClientResponse:
        """Get a ban from a guild.

        Parameters
        ----------
        user_id : int
            The ID of the user to get a ban from.
        guild_id : int
            The ID of the guild to get a ban from.

        Returns
        -------
        ClientResponse
            A ban object.
        """
        path = f"/guilds/{guild_id}/bans/{user_id}"
        return await self._client._request("GET", path)

    async def ban(
        self,
        user_id: int,
        guild_id: int,
        delete_message_days: int = 0,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Ban a user from a guild.

        Parameters
        ----------
        user_id : int
            The ID of the user to ban.
        guild_id : int
            The ID of the guild to ban the user from.
        delete_message_days : int, optional
            Number of days to delete messages for (0-7), by default 0
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A ban object.

        Raises
        ------
        InvalidParams
            If the delete_message_days is not an integer between 0 and 7.
        """
        if 0 > delete_message_days or delete_message_days > 7:
            raise InvalidParams("limit must be between 0 and 7")

        path = f"/guilds/{guild_id}/bans/{user_id}"

        params = {
            "delete_message_days": delete_message_days,
        }

        return await self._client._request(
            "PUT", path, params=params, headers={"X-Audit-Log-Reason": reason}
        )

    async def unban(
        self, user_id: int, guild_id: int, *, reason: Optional[str] = None
    ) -> ClientResponse:
        """Unban a user from a guild.

        Parameters
        ----------
        user_id : int
            The ID of the user to unban.
        guild_id : int
            The ID of the guild to unban the user from.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/bans/{user_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_roles(self, guild_id: int) -> ClientResponse:
        """Get a list of all roles in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get roles from.

        Returns
        -------
        ClientResponse
            A list of role objects.
        """
        path = f"/guilds/{guild_id}/roles"
        return await self._client._request("GET", path)

    async def create_role(
        self,
        guild_id: int,
        name: Optional[str] = None,
        permissions: Optional[str] = None,
        colour: Optional[int] = None,
        hoist: Optional[bool] = None,
        unicode_emoji: Optional[str] = None,
        mentionable: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Create a role in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to create a role in.
        name : str, optional
            Name of the role, by default None
        permissions : str, optional
            Bitwise value of the enabled permissions, by default None
        colour : int, optional
            RGB colour value, by default None
        hoist : bool, optional
            Whether the role should be displayed separately in the sidebar, by default None
        unicode_emoji : str, optional
            The role's unicode emoji as a standard emoji, by default None
        mentionable : bool, optional
            Whether the role should be mentionable, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A role object.
        """
        path = f"/guilds/{guild_id}/roles"
        payload = {}
        if name is not None:
            payload["name"] = name
        if permissions is not None:
            payload["permissions"] = permissions
        if colour is not None:
            payload["color"] = colour
        if hoist is not None:
            payload["hoist"] = hoist
        if unicode_emoji is not None:
            payload["unicode_emoji"] = unicode_emoji
        if mentionable is not None:
            payload["mentionable"] = mentionable
        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def move_role_position(
        self, guild_id: int, role_id: int, position: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Move a role's position in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to move a role in.
        role_id : int
            The ID of the role to move.
        position : int
            The new position of the role.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A list of role objects.
        """
        path = f"/guilds/{guild_id}/roles"
        payload = {"id": role_id, "position": position}
        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def edit_role(
        self, guild_id: int, role_id: int, reason: Optional[str] = None, **fields: Any
    ) -> ClientResponse:
        """Edit a role in a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit a role in.
        role_id : int
            The ID of the role to edit.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        **fields : Any
            The params required to update the required aspects of the role.

        Returns
        -------
        ClientResponse
            A role object.
        """
        path = f"/guilds/{guild_id}/roles/{role_id}"
        valid_keys = (
            "name",
            "permissions",
            "color",
            "hoist",
            "unicode_emoji",
            "mentionable",
        )
        payload = {k: v for k, v in fields.items() if k in valid_keys}
        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_role(
        self, guild_id: int, role_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete a role from a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete a role from.
        role_id : int
            The ID of the role to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/roles/{role_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def estimate_pruned_members(
        self, guild_id: int, days: int = 7, roles: Optional[str] = None
    ) -> ClientResponse:
        """Get the number of members that would be removed from a guild if prune was run.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get prune estimates for.
        days : int, optional
            Number of days to count prune for (1-30), by default 7
        roles : str, optional
            Role(s) to include, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.

        Raises
        ------
        InvalidParams
            If the days parameter is not between 1 and 30.
        """
        if 1 > days or days > 30:
            raise InvalidParams("days must be between 1 and 30")

        path = f"/guilds/{guild_id}/prune"

        params = {
            "days": days,
        }
        if roles is not None:
            params["include_roles"] = ", ".join(roles)  # type: ignore

        return await self._client._request("GET", path, params=params)

    async def prune_members(
        self,
        guild_id: int,
        days: int = 7,
        compute_prune_count: bool = False,
        roles: Optional[List[int]] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Prune members from a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to prune members from.
        days : int, optional
            Number of days to prune (1-30), by default 7
        compute_prune_count : bool, optional
            Whether pruned is returned, by default False
        roles : List[int], optional
            Role(s) to include, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.

        Raises
        ------
        InvalidParams
            If the days parameter is not between 1 and 30.
        """
        if 1 > days or days > 30:
            raise InvalidParams("days must be between 1 and 30")

        path = f"/guilds/{guild_id}/prune"

        payload = {
            "days": days,
            "compute_prune_count": compute_prune_count,
        }
        if roles:
            payload["include_roles"] = ", ".join(roles)  # type: ignore

        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_voice_regions(self, guild_id: int) -> ClientResponse:
        """Get the voice regions for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get voice regions for.

        Returns
        -------
        ClientResponse
            A list of voice region objects.
        """
        path = f"/guilds/{guild_id}/regions"
        return await self._client._request("GET", path)

    async def get_guild_invites(self, guild_id: int) -> ClientResponse:
        """Get the invites for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get invites for.

        Returns
        -------
        ClientResponse
            A list of invite objects.
        """
        path = f"/guilds/{guild_id}/invites"
        return await self._client._request("GET", path)

    async def get_guild_integrations(self, guild_id: int) -> ClientResponse:
        """Get the integrations for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get integrations for.

        Returns
        -------
        ClientResponse
            A list of integration objects.
        """
        path = f"/guilds/{guild_id}/integrations"
        return await self._client._request("GET", path)

    async def create_integration(
        self, guild_id: int, type: Any, id: Any
    ) -> ClientResponse:
        """Create an integration for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to create an integration for.
        type : Any
            The type of integration to create.
        id : Any
            The ID of the integration to create.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/integrations"

        payload = {
            "type": type,
            "id": id,
        }

        return await self._client._request("POST", path, json=payload)

    async def edit_integration(
        self, guild_id: int, integration_id: int, **payload: Any
    ) -> ClientResponse:
        """Edit an integration for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit an integration for.
        integration_id : int
            The ID of the integration to edit.
        payload : Any
            The params for the JSON payload.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/integrations/{integration_id}"

        return await self._client._request("PATCH", path, json=payload)

    async def sync_integration(
        self, guild_id: int, integration_id: int
    ) -> ClientResponse:
        """Sync an integration for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to sync an integration for.
        integration_id : int
            The ID of the integration to sync.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/integrations/{integration_id}/sync"

        return await self._client._request("POST", path)

    async def delete_guild_integration(
        self, guild_id: int, integration_id: int, *, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete an integration for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete an integration for.
        integration_id : int
            The ID of the integration to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/integrations/{integration_id}"

        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_guild_widget_settings(self, guild_id: int) -> ClientResponse:
        """Get the widget settings for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get widget settings for.

        Returns
        -------
        ClientResponse
            A guild widget settings object.
        """
        path = f"/guilds/{guild_id}/widget"
        return await self._client._request("GET", path)

    async def edit_widget(
        self, guild_id: int, enabled, channel_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Edit the widget settings for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit widget settings for.
        enabled : _type_
            Whether the widget is enabled.
        channel_id : int
            The ID of the channel to send the widget to.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A guild widget settings object.
        """
        path = f"/guilds/{guild_id}/widget"
        payload = {
            "enabled": enabled,
            "channel_id": channel_id,
        }
        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_guild_widget(self, guild_id: int) -> ClientResponse:
        """Get the widget for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get widget for.

        Returns
        -------
        ClientResponse
            A guild widget object.
        """
        path = f"/guilds/{guild_id}/widget.json"
        return await self._client._request("GET", path)

    async def get_vanity_code(self, guild_id: int) -> ClientResponse:
        """Get the vanity URL for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the vanity URL for.

        Returns
        -------
        ClientResponse
            A partial invite object.
        """
        path = f"/guilds/{guild_id}/vanity-url"
        return await self._client._request("GET", path)

    async def change_vanity_code(
        self, guild_id: int, code, reason: Optional[str] = None
    ) -> ClientResponse:
        """Change the vanity URL for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to change the vanity URL for.
        code : _type_
            The vanity URL code.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/vanity-url"
        payload = {"code": code}
        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_guild_welcome_screen(self, guild_id: int) -> ClientResponse:
        """Get the welcome screen for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the welcome screen for.

        Returns
        -------
        ClientResponse
            A welcome screen object.
        """
        path = f"/guilds/{guild_id}/welcome-screen"
        return await self._client._request("GET", path)

    async def edit_guild_welcome_screen(
        self,
        guild_id: int,
        enabled: Optional[bool] = None,
        welcome_channels: Optional[List[Any]] = None,
        description: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> ClientResponse:
        """Edit the welcome screen for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit the welcome screen for.
        enabled : bool, optional
            Whether the welcome screen is enabled, by default None
        welcome_channels : List[Any], optional
            Channels linked in the welcome screen and their display options, by default None
        description : str, optional
            The server description to show in the welcome screen, by default None
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            A welcome screen object.
        """
        path = f"/guilds/{guild_id}/welcome-screen"

        payload = {
            "enabled": enabled,
            "welcome_channels": welcome_channels,
            "description": description,
        }

        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def edit_voice_state(
        self,
        guild_id: int,
        channel_id: int,
        suppress: Optional[bool] = None,
        request_to_speak_timestamp: Optional[ISO8601_timestamp] = None,
    ) -> ClientResponse:
        """Edit the voice state for a user.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit the voice state for.
        channel_id : int
            The id of the channel the user is currently in.
        suppress : bool, optional
            Toggles the user's suppress state, by default None
        request_to_speak_timestamp : ISO8601_timestamp, optional
            Sets the user's request to speak, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/voice-states/@me"
        payload = {
            "channel_id": channel_id,
        }
        if suppress is not None:
            payload["suppress"] = suppress
        if request_to_speak_timestamp is not None:
            payload["request_to_speak_timestamp"] = request_to_speak_timestamp  # type: ignore
        return await self._client._request("PATCH", path, json=payload)

    async def edit_users_voice_state(
        self,
        guild_id: int,
        user_id: int,
        channel_id: int,
        suppress: Optional[bool] = None,
    ) -> ClientResponse:
        """Edit the voice state for a user.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit the voice state for.
        user_id : int
            The ID of the user to edit the voice state for.
        channel_id : int
            The id of the channel the user is currently in
        suppress : bool, optional
            Toggles the user's suppress state, by default None

        Returns
        -------
        ClientResponse
            _description_
        """
        path = f"/guilds/{guild_id}/voice-states/{user_id}"
        payload = {
            "channel_id": channel_id,
        }
        if suppress is not None:
            payload["suppress"] = suppress
        return await self._client._request("PATCH", path, json=payload)

    """
    Guild Scheduled Event
    """

    async def get_scheduled_events(
        self, guild_id: int, with_user_count: bool
    ) -> ClientResponse:
        """Get the scheduled events for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the scheduled events for.
        with_user_count : bool
            Include number of users subscribed to each event.

        Returns
        -------
        ClientResponse
            A list of guild scheduled event objects.
        """
        path = f"/guilds/{guild_id}/scheduled-events"
        params = {"with_user_count": with_user_count}
        return await self._client._request("GET", path, params=params)

    async def create_guild_scheduled_event(
        self, guild_id: int, reason: Optional[str] = None, **payload: Any
    ) -> ClientResponse:
        """Create a scheduled event for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to create the scheduled event for.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        payload : Any
            The params for the JSON payload.

        Returns
        -------
        ClientResponse
            A guild scheduled event object.
        """
        path = f"/guilds/{guild_id}/scheduled-events"
        valid_keys = (
            "channel_id",
            "entity_metadata",
            "name",
            "privacy_level",
            "scheduled_start_time",
            "scheduled_end_time",
            "description",
            "entity_type",
            "image",
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._client._request(
            "POST", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_scheduled_event(
        self, guild_id: int, guild_scheduled_event_id: int, with_user_count: bool
    ) -> ClientResponse:
        """Get a scheduled event for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the scheduled event for.
        guild_scheduled_event_id : int
            The ID of the scheduled event to get.
        with_user_count : bool
            Include number of users subscribed to this event.

        Returns
        -------
        ClientResponse
            A guild scheduled event object.
        """
        path = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
        params = {"with_user_count": with_user_count}
        return await self._client._request("GET", path, params=params)

    async def edit_scheduled_event(
        self,
        guild_id: int,
        guild_scheduled_event_id: int,
        *,
        reason: Optional[str] = None,
        **payload: Any,
    ) -> ClientResponse:
        """Edit a scheduled event for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit the scheduled event for.
        guild_scheduled_event_id : int
            The ID of the scheduled event to edit.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None
        payload : Any
            The params required to update the required aspects of the scheduled event.

        Returns
        -------
        ClientResponse
            A guild scheduled event object.
        """
        path = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
        valid_keys = (
            "channel_id",
            "entity_metadata",
            "name",
            "privacy_level",
            "scheduled_start_time",
            "scheduled_end_time",
            "status",
            "description",
            "entity_type",
            "image",
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}

        return await self._client._request(
            "PATCH", path, json=payload, headers={"X-Audit-Log-Reason": reason}
        )

    async def delete_scheduled_event(
        self, guild_id: int, guild_scheduled_event_id: int, reason: Optional[str] = None
    ) -> ClientResponse:
        """Delete a scheduled event for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete the scheduled event for.
        guild_scheduled_event_id : int
            The ID of the scheduled event to delete.
        reason : str, optional
            A reason for this action that will be displayed in the audit log, by default None

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
        return await self._client._request(
            "DELETE", path, headers={"X-Audit-Log-Reason": reason}
        )

    async def get_scheduled_event_users(
        self,
        guild_id: int,
        guild_scheduled_event_id: int,
        limit: int,
        with_member: bool,
        before: Optional[int] = None,
        after: Optional[int] = None,
    ) -> ClientResponse:
        """Get the users subscribed to a scheduled event.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the scheduled event users for.
        guild_scheduled_event_id : int
            The ID of the scheduled event to get the users for.
        limit : int
            Number of users to return (up to maximum 100)
        with_member : bool
            Include guild member data if it exists
        before : int, optional
            Consider only users before given user id, by default None
        after : int, optional
            Consider only users after given user id, by default None

        Returns
        -------
        ClientResponse
            A list of guild scheduled event user objects.
        """
        path = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users"

        params = {
            "limit": limit,
            "with_member": int(with_member),
        }

        if before is not None:
            params["before"] = before
        if after is not None:
            params["after"] = after

        return await self._client._request("GET", path, params=params)

    """
    Guild Template
    """

    async def get_template(self, code: str) -> ClientResponse:
        """Get a guild template.

        Parameters
        ----------
        code : str
            The code of the template to get.

        Returns
        -------
        ClientResponse
            A guild template object.
        """
        path = f"/guilds/templates/{code}"
        return await self._client._request("GET", path)

    async def create_from_template(self, code: str, name: str) -> ClientResponse:
        """Create a guild from a template.

        Parameters
        ----------
        code : str
            The code of the template to create the guild from.
        name : str
            Name of the guild (2-100 characters).

        Returns
        -------
        ClientResponse
            A guild object.
        """
        path = f"/guilds/templates/{code}"
        payload = {
            "name": name,
        }
        return await self._client._request("POST", path, json=payload)

    async def get_guild_templates(self, guild_id: int) -> ClientResponse:
        """Get a guild's templates.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to get the templates for.

        Returns
        -------
        ClientResponse
            A list of guild template objects.
        """
        path = f"/guilds/{guild_id}/templates"
        return await self._client._request("GET", path)

    async def create_template(
        self, guild_id: int, name: str, description: Optional[str] = None
    ) -> ClientResponse:
        """Create a template for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to create the template for.
        name : str
            Name of the template (1-100 characters).
        description : str, optional
            Description for the template (0-120 characters), by default None

        Returns
        -------
        ClientResponse
            A guild template object.
        """
        path = f"/guilds/{guild_id}/templates"
        payload = {
            "name": name[:100],
        }
        if description is not None:
            payload["description"] = description[:120]
        return await self._client._request("POST", path, json=payload)

    async def sync_template(self, guild_id: int, code: str) -> ClientResponse:
        """Sync a template for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to sync the template for.
        code : str
            The code of the template to sync.

        Returns
        -------
        ClientResponse
            A guild template object.
        """
        path = f"/guilds/{guild_id}/templates/{code}"
        return await self._client._request("PUT", path)

    async def edit_template(
        self, guild_id: int, code: str, name: str, description: Optional[str] = None
    ) -> ClientResponse:
        """Edit a template for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to edit the template for.
        code : str
            The code of the template to edit.
        name : str
            Name of the template (1-100 characters)
        description : str, optional
            Description for the template (0-120 characters), by default None

        Returns
        -------
        ClientResponse
            A guild template object.
        """
        path = f"/guilds/{guild_id}/templates/{code}"
        payload = {
            "name": name[:100],
        }
        if description is not None:
            payload["description"] = description[:120]
        return await self._client._request("PATCH", path, json=payload)

    async def delete_template(self, guild_id: int, code: str) -> ClientResponse:
        """Delete a template for a guild.

        Parameters
        ----------
        guild_id : int
            The ID of the guild to delete the template for.
        code : str
            The code of the template to delete.

        Returns
        -------
        ClientResponse
            A guild template object.
        """
        path = f"/guilds/{guild_id}/templates/{code}"
        return await self._client._request("DELETE", path)
