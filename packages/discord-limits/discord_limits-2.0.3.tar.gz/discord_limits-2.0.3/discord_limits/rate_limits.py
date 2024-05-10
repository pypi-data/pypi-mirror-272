import asyncio
import datetime
import stat
from typing import Dict, Optional

from aiohttp import ClientResponse
from aiolimiter import AsyncLimiter
from .errors import *


class BucketHandler:
    limit: Optional[int] = None  # The rate limit
    remaining: Optional[int] = None  # Remaining requests
    reset: Optional[datetime.datetime] = None  # When the rate limit resets
    retry_after: Optional[float] = None  # How long to wait before retrying the request
    bucket_hash: str = ""  # The bucket hash from Discord
    lock: asyncio.Event = (
        asyncio.Event()
    )  # Used to lock the bucket if a rate limit is hit

    def __init__(self):
        self.lock.set()

    async def trigger_lock(self):
        self.lock.clear()
        await asyncio.sleep(self.retry_after)  # type: ignore
        self.lock.set()

    async def __aenter__(self):
        await self.lock.wait()
        if self.remaining is not None and self.remaining == 0:
            now = datetime.datetime.now(datetime.timezone.utc)
            to_wait = (self.reset - now).total_seconds() + 1  # type: ignore
            await asyncio.sleep(to_wait)
        return self

    async def __aexit__(self, *args):
        pass


class ClientRateLimits:
    buckets: Dict[str, BucketHandler] = dict()  # {bucket_hash: BucketHandler}
    bucket_relations: Dict[str, str] = dict()  # {path: bucket_hash}

    def __init__(self):
        self.global_limiter = AsyncLimiter(50, 1)  # 50 requests per second

    def update_bucket_relations(self, old_hash: str, new_hash: str):
        for path, bucket_hash in self.bucket_relations.items():
            if bucket_hash == old_hash:
                self.bucket_relations[path] = new_hash

        self.buckets[new_hash] = self.buckets.pop(old_hash)
