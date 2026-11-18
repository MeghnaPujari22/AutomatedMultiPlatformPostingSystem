import httpx
from app.config import settings
from app.platforms.base import PlatformPoster

class DiscordPoster(PlatformPoster):
    name = "Discord"

    async def post(self, message: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    settings.DISCORD_WEBHOOK_URL,
                    json={"content": message},
                )

            if response.status_code not in (200, 204):
                return self.failure(f"Discord API error: {response.status_code}")

            return self.success(None)

        except Exception as exc:
            return self.failure(str(exc))