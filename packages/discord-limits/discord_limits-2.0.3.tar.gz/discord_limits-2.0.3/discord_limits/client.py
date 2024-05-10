import asyncio
import warnings
import datetime
from sys import version_info as python_version

from aiohttp import ClientResponse, ClientSession
from aiohttp import __version__ as aiohttp_version
from aiolimiter import AsyncLimiter

from . import __version__
from .errors import *
from .paths import Paths
from .rate_limits import BucketHandler, ClientRateLimits

from typing import Optional


class DiscordClient(Paths):
    """
    Parameters
    ----------
    token : str
        The token to use for the request.
    token_type : str, optional
        The type of token provided ('bot', 'bearer', 'user', None), by default 'bot'
    api_version : int, optional
        The Discord API version to use (6, 7, 8, 9, 10), by default 10

    Attributes
    ----------
    token : str
        The token to use for the request.
    token_type : str
        The type of token provided. Can be 'bot', 'bearer' or 'user'.
    api_version : int
        The Discord API version to use. Default is 10.
    suppress_warnings : bool
        Whether to suppress warnings or not. Default is False.
    max_attempts : int
        The maximum number of attempts to make a request. Default is 3.
    """

    def __init__(
        self,
        token: Optional[str],
        token_type: Optional[str] = "bot",
        api_version: int = 10,
        suppress_warnings: bool = False,
        max_attempts: int = 3,
    ):
        super().__init__(self)

        if api_version < 6:
            raise InvalidParams("API version must be 6 or higher.")
        elif api_version < 9 and not suppress_warnings:
            warnings.warn(
                f"API version {api_version} is now deprecated by Discord, some endpoints may not work as expected.",
                UserWarning,
            )

        if token_type == "bot":
            self.token = f"Bot {token}"
            self.token_type = token_type
        elif token_type == "bearer":
            self.token = f"Bearer {token}"
            self.token_type = token_type
        elif token_type == "user":
            if not suppress_warnings:
                warnings.warn(
                    "Use a user token at your own risk as (depending on your usage) it could be against Discord's ToS. If you are using this token for a bot, you should use the 'bot' token_type instead.",
                    UserWarning,
                )
            self.token = f"{token}"
            self.token_type = token_type
        else:
            self.token = None
            self.token_type = None

        self.rate_limits = ClientRateLimits()
        self._base_url = f"https://discord.com/api/v{api_version}"
        self._base_url_len = len(self._base_url)

        self._user_agent: str = (
            f"DiscordBot (https://github.com/ninjafella/discord-API-limits {__version__}) Python/{python_version[0]}.{python_version[1]}.{python_version[2]} aiohttp/{aiohttp_version}"
        )

        self.global_limiter = AsyncLimiter(50, 1)

        self.suppress_warnings = suppress_warnings
        self.max_attempts = max_attempts

    def _create_bucket_handler(self, r: ClientResponse, bucket_path: str):
        status = r.status

        if status == 400:
            raise BadRequest
        elif status == 401:
            raise Unauthorized
        elif status == 403:
            raise Forbidden
        elif status == 404:
            raise NotFound
        elif status == 500:
            raise InternalServerError

        if self.rate_limits.buckets.get(r.headers["X-RateLimit-Bucket"]) is not None:
            bucket_hash = r.headers["X-RateLimit-Bucket"]
            self.rate_limits.bucket_relations[bucket_path] = bucket_hash
            self._check_response(r, self.rate_limits.buckets[bucket_hash])
        else:
            bh = BucketHandler()
            self._check_response(r, bh)
            self.rate_limits.buckets[bh.bucket_hash] = bh
            self.rate_limits.bucket_relations[bucket_path] = bh.bucket_hash

    async def _request(
        self,
        method: str,
        path: str,
        headers: dict = {},
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        auth: bool = True,
        metadata: Optional[str] = None,
        _attempts: int = 0,
    ) -> ClientResponse:  # type: ignore

        if _attempts >= self.max_attempts:
            raise MaxAttemptsReached

        headers["User-Agent"] = self._user_agent
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        if auth:
            if self.token_type is None:
                raise InvalidParams(
                    "No token has been set. Please set a token with set_new_token()."
                )
            headers["Authorization"] = self.token
        cs = ClientSession()

        url = self._base_url + path

        request_manager = cs.request(
            method, url, json=json, params=params, headers=headers
        )

        if metadata is not None:
            bucket_path = f"{method}:{path}:{metadata}"
        bucket_path = f"{method}:{path}"

        bucket_hash = self.rate_limits.bucket_relations.get(bucket_path)
        if bucket_hash is not None:
            bucket_handler = self.rate_limits.buckets[bucket_hash]

            async with self.rate_limits.global_limiter:
                async with bucket_handler:
                    async with cs:
                        response = await request_manager
                        try:
                            self._check_response(response, bucket_handler)
                        except TooManyRequests:
                            await self._request(
                                method,
                                path,
                                headers=headers,
                                json=json,
                                params=params,
                                auth=auth,
                                metadata=metadata,
                                _attempts=_attempts + 1,
                            )
                        except Exception as e:
                            raise e

        else:
            async with self.rate_limits.global_limiter:
                async with cs:
                    response = await request_manager
                    try:
                        self._create_bucket_handler(response, bucket_path)
                    except TooManyRequests:
                        await self._request(
                            method,
                            path,
                            headers=headers,
                            json=json,
                            params=params,
                            auth=auth,
                            metadata=metadata,
                            _attempts=_attempts + 1,
                        )
                    except Exception as e:
                        raise e

    def _check_response(self, r: ClientResponse, bh: BucketHandler):
        headers = r.headers
        status = r.status

        if status == 400:
            raise BadRequest
        elif status == 401:
            raise Unauthorized
        elif status == 403:
            raise Forbidden
        elif status == 404:
            raise NotFound
        elif status == 500:
            raise InternalServerError

        for header in headers:
            if header == "X-RateLimit-Limit":
                bh.limit = int(headers["X-RateLimit-Limit"])
            elif header == "X-RateLimit-Remaining":
                bh.remaining = int(headers["X-RateLimit-Remaining"])
            elif header == "X-RateLimit-Reset":
                bh.reset = datetime.datetime.fromtimestamp(
                    float(headers["X-RateLimit-Reset"]),
                    datetime.timezone.utc,
                )
            elif header == "X-RateLimit-Bucket" and header != bh.bucket_hash:
                if bh.bucket_hash == "":
                    bh.bucket_hash = headers["X-RateLimit-Bucket"]
                old_hash = bh.bucket_hash
                bh.bucket_hash = headers["X-RateLimit-Bucket"]
                self.rate_limits.update_bucket_relations(old_hash, bh.bucket_hash)

        if status == 429:
            bh.retry_after = float(headers["X-RateLimit-Reset-After"])
            asyncio.ensure_future(bh.trigger_lock())
            raise TooManyRequests
        elif not (300 > status >= 200):
            raise UnknownError

    def set_new_token(
        self, token: Optional[str], token_type: Optional[str] = "bot"
    ) -> None:
        """Set a new token to use.

        Parameters
        ----------
        token : str
            The new token to use for the request.
        token_type : str, optional
            The type of token provided ('bot', 'bearer', 'user', None), by default 'bot'
        """
        if token_type == "bot":
            self.token = f"Bot {token}"
        elif token_type == "bearer":
            self.token = f"Bearer {token}"
        elif token_type == "user":
            if not self.suppress_warnings:
                warnings.warn(
                    "Use a user token at your own risk as (depending on your usage) it could be against Discord's ToS. If you are using this token for a bot, you should use the 'bot' token_type instead.",
                    UserWarning,
                )
            self.token = token
        else:
            self.token = None
