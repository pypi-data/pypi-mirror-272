from typing import TYPE_CHECKING

from aiohttp import ClientResponse

from discord_limits.errors import *

if TYPE_CHECKING:
    from discord_limits import DiscordClient


class ApplicationPaths:
    """
    Parameters
    ----------
    client : discord_limits.DiscordClient
        The DiscordClient instance to use.
    """

    def __init__(self, client: "DiscordClient"):
        self._client = client

    # Application commands (global)

    async def get_global_application_commands(
        self, application_id: int
    ) -> ClientResponse:
        """Fetch all of the global commands for an application.

        Parameters
        ----------
        application_id : int
            The application ID.

        Returns
        -------
        ClientResponse
            A list of application command objects.
        """
        path = f"/applications/{application_id}/commands"
        return await self._client._request("GET", path)

    async def create_global_application_command(
        self, application_id: int, payload: dict
    ) -> ClientResponse:
        """Create a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        payload : dict
            The params to create the command with.

        Returns
        -------
        ClientResponse
            An application command object.
        """
        path = f"/applications/{application_id}/commands"
        return await self._client._request("POST", path, json=payload)

    async def get_global_application_command(
        self, application_id: int, command_id: int
    ) -> ClientResponse:
        """Get a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        command_id : int
            The command ID.

        Returns
        -------
        ClientResponse
            An application command object.
        """
        path = f"/applications/{application_id}/commands/{command_id}"
        return await self._client._request("GET", path)

    async def edit_global_application_command(
        self, application_id: int, command_id: int, payload: dict
    ) -> ClientResponse:
        """Edit a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        command_id : int
            The command ID.
        payload : dict
            The params to edit the command with.

        Returns
        -------
        ClientResponse
            An application command object.
        """
        path = f"/applications/{application_id}/commands/{command_id}"
        valid_keys = (
            "name",
            "description",
            "options",
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}
        return await self._client._request("PATCH", path, json=payload)

    async def delete_global_application_command(
        self, application_id: int, command_id: int
    ) -> ClientResponse:
        """Delete a global command.

        Parameters
        ----------
        application_id : int
            The application ID.
        command_id : int
            The command ID.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/applications/{application_id}/commands/{command_id}"
        return await self._client._request("DELETE", path)

    async def bulk_overwrite_global_application_commands(
        self, application_id: int, payload: dict
    ) -> ClientResponse:
        """Bulk edit global commands.

        Parameters
        ----------
        application_id : int
            The application ID.
        payload : dict
            The params to edit the commands with.

        Returns
        -------
        ClientResponse
            A list of application command objects.
        """
        path = f"/applications/{application_id}/commands"
        return await self._client._request("PUT", path, json=payload)

    # Application commands (guild)

    async def get_guild_application_commands(
        self, application_id: int, guild_id: int, with_localisations: bool = False
    ) -> ClientResponse:
        """Fetch all of the guild commands for an application.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        with_localisations : bool, optional
            Whether to include full localisations dictionaries, by default False

        Returns
        -------
        ClientResponse
            A list of application command objects.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands"
        return await self._client._request("GET", path)

    async def create_guild_application_command(
        self, application_id: int, guild_id: int, payload: dict
    ) -> ClientResponse:
        """Create a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        payload : dict
            The params to create the command with.

        Returns
        -------
        ClientResponse
            An application command object.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands"
        return await self._client._request("POST", path, json=payload)

    async def get_guild_application_command(
        self, application_id: int, guild_id: int, command_id: int
    ) -> ClientResponse:
        """Get a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.

        Returns
        -------
        ClientResponse
            An application command object.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"
        return await self._client._request("GET", path)

    async def edit_guild_application_command(
        self, application_id: int, guild_id: int, command_id: int, payload: dict
    ) -> ClientResponse:
        """Edit a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.
        payload : dict
            The params to edit the command with.

        Returns
        -------
        ClientResponse
            An application command object.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"
        valid_keys = (
            "name",
            "description",
            "options",
        )
        payload = {k: v for k, v in payload.items() if k in valid_keys}
        return await self._client._request("PATCH", path, json=payload)

    async def delete_guild_application_command(
        self, application_id: int, guild_id: int, command_id: int
    ) -> ClientResponse:
        """Delete a guild command.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"
        return await self._client._request("DELETE", path)

    async def bulk_overwrite_guild_application_commands(
        self, application_id: int, guild_id: int, payload: dict
    ) -> ClientResponse:
        """Bulk overwrite guild commands.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        payload : dict
            The params to overwrite the commands with.

        Returns
        -------
        ClientResponse
            A list of application command objects.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands"
        return await self._client._request("PUT", path, json=payload)

    async def get_guild_application_command_permissions(
        self, application_id: int, guild_id: int
    ) -> ClientResponse:
        """Fetch all of the guild application command permissions for an application.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.

        Returns
        -------
        ClientResponse
            A list of guild application command permissions objects.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands/permissions"
        return await self._client._request("GET", path)

    async def get_application_command_permissions(
        self, application_id: int, guild_id: int, command_id: int
    ) -> ClientResponse:
        """Get permissions for a specific command for your application in a guild.

        Parameters
        ----------
        application_id : int
            _description_
        guild_id : int
            _description_
        command_id : int
            _description_

        Returns
        -------
        ClientResponse
            A guild application command permissions object.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions"
        return await self._client._request("GET", path)

    async def edit_application_command_permissions(
        self, application_id: int, guild_id: int, command_id: int, payload: dict
    ) -> ClientResponse:
        """Edit a guild application command permissions.

        Parameters
        ----------
        application_id : int
            The application ID.
        guild_id : int
            The guild ID.
        command_id : int
            The command ID.
        payload : dict
            The params to edit the command permissions with.

        Returns
        -------
        ClientResponse
            A guild application command permissions object.
        """
        path = f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions"
        return await self._client._request("PUT", path, json=payload)
