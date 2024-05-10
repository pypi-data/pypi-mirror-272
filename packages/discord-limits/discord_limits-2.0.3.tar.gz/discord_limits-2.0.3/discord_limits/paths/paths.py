from aiohttp import ClientResponse
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from discord_limits.client import DiscordClient

from discord_limits.errors import *

from .applicationPaths import ApplicationPaths
from .auditPaths import AuditPaths
from .autoModerationPaths import AutoModerationPaths
from .channelPaths import ChannelPaths
from .emojiPaths import EmojiPaths
from .guildPaths import GuildPaths
from .interationsPaths import InteractionsPaths
from .invitePaths import InvitePaths
from .stagePaths import StagePaths
from .stickerPaths import StickerPaths
from .userPaths import UserPaths
from .webhookPaths import WebhookPaths


class Paths:
    """A class representing various paths related to different entities.

    Parameters
    ----------
    client : DiscordClient
        The client to use for the paths.

    Attributes
    ----------
    application : ApplicationPaths
        The application paths.
    audit_logs : AuditPaths
        The audit log paths.
    auto_moderation : AutoModerationPaths
        The auto moderation paths.
    channel : ChannelPaths
        The channel paths.
    emoji : EmojiPaths
        The emoji paths.
    guild : GuildPaths
        The guild paths.
    interactions : InteractionsPaths
        The interactions paths.
    invite : InvitePaths
        The invite paths.
    stage : StagePaths
        The stage paths.
    sticker : StickerPaths
        The sticker paths.
    user : UserPaths
        The users paths.
    webhook : WebhookPaths
        The webhook paths.
    """

    def __init__(self, client):
        self._client: "DiscordClient" = client
        self.application: ApplicationPaths = ApplicationPaths(
            self._client
        )  #: ApplicationPaths: The application paths.
        self.audit_logs: AuditPaths = AuditPaths(
            self._client
        )  #: AuditPaths: The audit log paths.
        self.auto_moderation: AutoModerationPaths = AutoModerationPaths(
            self._client
        )  #: AutoModerationPaths: The auto moderation paths
        self.channel: ChannelPaths = ChannelPaths(
            self._client
        )  #: ChannelPaths: The channel paths.
        self.emoji: EmojiPaths = EmojiPaths(
            self._client
        )  #: EmojiPaths: The emoji paths.
        self.guild: GuildPaths = GuildPaths(
            self._client
        )  #: GuildPaths: The guild paths.
        self.interactions: InteractionsPaths = InteractionsPaths(
            self._client
        )  #: InteractionsPaths: The interactions paths
        self.invite: InvitePaths = InvitePaths(
            self._client
        )  #: InvitePaths: The invite paths.
        self.stage: StagePaths = StagePaths(
            self._client
        )  #: StagePaths: The stage paths.
        self.sticker: StickerPaths = StickerPaths(
            self._client
        )  #: StickerPaths: The sticker paths.
        self.user: UserPaths = UserPaths(self._client)  #: UserPaths: The users paths.
        self.webhook: WebhookPaths = WebhookPaths(
            self._client
        )  #: WebhookPaths: The webhook paths.

    async def list_voice_regions(self) -> ClientResponse:
        """Get a list of voice regions.

        Returns
        -------
        ClientResponse
            A list of voice region objects.
        """
        path = "/voice/regions"
        return await self._client._request("GET", path)

    async def get_gateway(self) -> ClientResponse:
        """Get the gateway URL.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = "/gateway"
        return await self._client._request("GET", path, auth=False)

    async def get_bot_gateway(self) -> ClientResponse:
        """Get the gateway URL for a bot.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = "/gateway/bot"
        return await self._client._request("GET", path)

    async def application_info(self) -> ClientResponse:
        """Get the application info.

        Returns
        -------
        ClientResponse
            An application object.
        """
        path = "/oauth2/applications/@me"
        return await self._client._request("GET", path)

    async def authorisation_info(self, bearer_token: str) -> ClientResponse:
        """Get the authorisation info.

        Parameters
        ----------
        bearer_token : str
            The bearer token to get the authorisation info for.

        Returns
        -------
        ClientResponse
            The response from Discord.
        """
        path = "/oauth2/@me"
        return await self._client._request(
            "GET",
            path,
            headers={"Authorization": f"Bearer {bearer_token}"},
            auth=False,
        )  # auth is False as a bearer_token is used
