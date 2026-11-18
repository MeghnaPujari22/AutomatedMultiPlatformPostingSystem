import os

import requests
from dotenv import load_dotenv

load_dotenv()

PLATFORM = os.getenv("PLATFORM", "").lower().strip()
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"


def post_message(message: str) -> str:
    """Post a message to the platform selected in .env."""
    if not message or not message.strip():
        raise ValueError("Message cannot be empty")

    if not PLATFORM:
        raise ValueError("PLATFORM is not set in .env")

    if DRY_RUN:
        return f"DRY RUN: Would post to {PLATFORM}: {message}"

    posters = {
        "telegram": post_to_telegram,
        "discord": post_to_discord,
        "linkedin": post_to_linkedin,
        "devto": post_to_devto,
        "slack": post_to_slack,
    }

    poster = posters.get(PLATFORM)
    if poster is None:
        raise ValueError(
            f"Unsupported PLATFORM '{PLATFORM}'. "
            "Use telegram, discord, linkedin, devto, or slack."
        )

    return poster(message)


def post_to_telegram(message: str) -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")

    return f"Posted to Telegram: message ID {data['result']['message_id']}"


def post_to_discord(message: str) -> str:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL must be set")

    response = requests.post(
        webhook_url,
        json={"content": message},
        timeout=30,
    )
    response.raise_for_status()

    return "Posted to Discord"


def post_to_linkedin(message: str) -> str:
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.getenv("LINKEDIN_AUTHOR_URN")

    if not access_token or not author_urn:
        raise ValueError(
            "LINKEDIN_ACCESS_TOKEN and LINKEDIN_AUTHOR_URN must be set"
        )

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    post_id = response.headers.get("x-restli-id", "unknown")
    return f"Posted to LinkedIn: {post_id}"


def post_to_devto(message: str) -> str:
    api_key = os.getenv("DEVTO_API_KEY")

    if not api_key:
        raise ValueError("DEVTO_API_KEY must be set")

    url = "https://dev.to/api/articles"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }

    first_line = message.strip().splitlines()[0]
    body = message.strip()

    payload = {
        "article": {
            "title": first_line[:120],
            "body_markdown": body,
            "published": False,
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    article = response.json()
    return (
        f"Created Dev.to draft: {article.get('url', 'unknown URL')} "
        f"(published=False)"
    )


def post_to_slack(message: str) -> str:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL must be set")

    response = requests.post(
        webhook_url,
        json={"text": message},
        timeout=30,
    )
    response.raise_for_status()

    return "Posted to Slack"


if __name__ == "__main__":
    test_message = "Hello from my automated multi-platform posting test!"
    print(post_message(test_message))