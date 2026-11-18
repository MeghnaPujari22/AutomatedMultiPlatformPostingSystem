import httpx

from app.config import settings
from app.platforms.base import PlatformPoster


class DevToPoster(PlatformPoster):
    name = "DEV Community"

    async def post(self, message: str) -> dict:
        try:
            if not settings.DEVTO_API_KEY:
                return self.failure("DEV Community API key is not configured")

            title = message.split("https://")[0].strip()

            if not title:
                title = "Automated Post"

            if len(title) > 120:
                title = title[:117] + "..."

            headers = {
                "api-key": settings.DEVTO_API_KEY,
                "Content-Type": "application/json",
            }

            payload = {
                "article": {
                    "title": title,
                    "body_markdown": message,
                    "published": True,
                    "tags": ["python", "api", "automation"],
                }
            }

            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(
                    "https://dev.to/api/articles",
                    headers=headers,
                    json=payload,
                )

            if response.status_code not in (200, 201):
                return self.failure(
                    f"DEV Community API error {response.status_code}: {response.text}"
                )

            article = response.json()
            posted_url = article.get("url")

            return self.success(posted_url)

        except httpx.TimeoutException:
            return self.failure("DEV Community API request timed out")

        except httpx.RequestError as exc:
            return self.failure(f"DEV Community API request failed: {str(exc)}")

        except Exception as exc:
            return self.failure(f"Unexpected DEV Community error: {str(exc)}")