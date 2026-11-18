import asyncio

from app.platforms.telegram import TelegramPoster
from app.platforms.discord import DiscordPoster
from app.platforms.linkedin import LinkedInPoster
from app.platforms.slack import SlackPoster
from app.platforms.devto import DevToPoster

PLATFORMS = [
    TelegramPoster(),
    DiscordPoster(),
    LinkedInPoster(),
    SlackPoster(),
    DevToPoster(),
]


async def post_to_all_platforms(message: str) -> list[dict]:
    tasks = [platform.post(message) for platform in PLATFORMS]
    return await asyncio.gather(*tasks, return_exceptions=False)