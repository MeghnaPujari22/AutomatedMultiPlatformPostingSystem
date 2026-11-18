from pydantic import BaseModel, field_validator
from urllib.parse import urlparse

class PostingRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty")

        if len(value) > 200:
            raise ValueError("Message must not exceed 200 characters")

        links = [
            token for token in value.split()
            if token.startswith("http://") or token.startswith("https://")
        ]

        if len(links) != 1:
            raise ValueError("Message must contain exactly one CTA link")

        parsed = urlparse(links[0])

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("Invalid URL")

        return value