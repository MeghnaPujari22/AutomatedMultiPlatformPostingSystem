import httpx

from app.config import settings
from app.platforms.base import PlatformPoster


class SlackPoster(PlatformPoster):
    name = "Slack"

    async def post(self, message: str) -> dict:
        try:
            if not settings.SLACK_WEBHOOK_URL:
                return self.failure("Slack webhook URL is not configured")

            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    settings.SLACK_WEBHOOK_URL,
                    json={"text": message},
                )

            if response.status_code != 200:
                return self.failure(
                    f"Slack API error {response.status_code}: {response.text}"
                )

            return self.success(None)

        except httpx.TimeoutException:
            return self.failure("Slack API request timed out")

        except httpx.RequestError as exc:
            return self.failure(f"Slack API request failed: {str(exc)}")

        except Exception as exc:
            return self.failure(f"Unexpected Slack error: {str(exc)}")