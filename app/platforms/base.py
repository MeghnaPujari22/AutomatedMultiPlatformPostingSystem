from abc import ABC, abstractmethod
from typing import Optional
import httpx

class PlatformPoster(ABC):
    name: str

    @abstractmethod
    async def post(self, message: str) -> dict:
        pass

    def success(self, posted_url: Optional[str]) -> dict:
        from datetime import datetime

        now = datetime.now()

        return {
            "platform": self.name,
            "status": "success",
            "posted_url": posted_url,
            "public_access": True,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "error": None,
        }

    def failure(self, error: str) -> dict:
        return {
            "platform": self.name,
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": error,
        }