import httpx
from app.config import settings
from app.platforms.base import PlatformPoster

class TelegramPoster(PlatformPoster):
    name = "Telegram"

    async def post(self, message: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": settings.TELEGRAM_CHAT_ID,
                        "text": message,
                        "disable_web_page_preview": False,
                    },
                )

            data = response.json()

            if response.status_code != 200:
                return self.failure(data.get("description", "Telegram API error"))

            message_id = data["result"]["message_id"]
            posted_url = (
                f"https://t.me/{settings.TELEGRAM_CHAT_ID}/{message_id}"
                if str(settings.TELEGRAM_CHAT_ID).startswith("@")
                else None
            )

            return self.success(posted_url)

        except Exception as exc:
            return self.failure(str(exc))