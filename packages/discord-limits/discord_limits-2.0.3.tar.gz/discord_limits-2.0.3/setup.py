from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="discord_limits",
    packages=find_packages(
        include=["discord_limits", "discord_limits.paths", "discord_limits.objects"]
    ),
    version="2.0.3",
    description="Make Discord API calls without having to worry about ratelimits.",
    author="ninjafella",
    license="MIT",
    install_requires=["aiolimiter==1.1.0", "aiohttp==3.9.5"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ninjafella/discord-API-limits",
    python_requires=">=3.10",
)
