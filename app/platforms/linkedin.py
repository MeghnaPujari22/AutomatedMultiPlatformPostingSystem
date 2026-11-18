
import httpx
from app.config import settings
from app.platforms.base import PlatformPoster


class LinkedInPoster(PlatformPoster):
    name = "LinkedIn"

    async def post(self, message: str) -> dict:
        try:
            headers = {
                "Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
                "LinkedIn-Version": "202601",
            }

            payload = {
                "author": settings.LINKEDIN_AUTHOR_URN,
                "commentary": message,
                "visibility": "PUBLIC",
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": [],
                },
                "lifecycleState": "PUBLISHED",
                "isReshareDisabledByAuthor": False,
            }

            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(
                    "https://api.linkedin.com/rest/posts",
                    headers=headers,
                    json=payload,
                )

            if response.status_code not in (200, 201):
                return self.failure(
                    f"LinkedIn API error: {response.status_code} "
                    f"- {response.text}"
                )

            post_id = (
                response.headers.get("x-restli-id")
                or response.json().get("id")
            )

            posted_url = (
                f"https://www.linkedin.com/feed/update/{post_id}"
                if post_id else None
            )

            return self.success(posted_url)

        except httpx.HTTPError as exc:
            return self.failure(f"LinkedIn HTTP error: {str(exc)}")

        except Exception as exc:
            return self.failure(str(exc))
