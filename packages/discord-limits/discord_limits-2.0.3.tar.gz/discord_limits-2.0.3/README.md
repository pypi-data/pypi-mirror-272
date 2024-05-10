[![Documentation Status]](https://discord-limits.readthedocs.io/en/latest/?badge=latest)
[![Version](https://img.shields.io/badge/Version-v2.0.3-blue)](https://img.shields.io/badge/Version-v2.0.3-blue)

# discord_limits

### A simple library to asynchronously make API requests to Discord without having to worry about ratelimits.

<br>

---

# Basic usage

```py
import discord_limits
import asyncio

limits_client = discord_limits.DiscordClient("YOUR_TOKEN", "bot")

async def main():
    await limits_client.channel.create_message("CHANNEL_ID", "Hello World!")

asyncio.run(main())

```

---
### Requires:
- [aiolimiter](https://pypi.org/project/aiolimiter/)
- [aiohttp](https://pypi.org/project/aiohttp/)


[def]: https://readthedocs.org/projects/discord-limits/badge/?version=latest