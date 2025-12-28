"""Slack integration."""

import httpx
from typing import Dict, Any

from app.config import get_settings

settings = get_settings()


async def send_slack_alert(message: str, severity: str = "info") -> bool:
    """Send alert to Slack."""
    if not settings.SLACK_WEBHOOK_URL:
        return False

    colors = {
        "critical": "#c01547",
        "high": "#a84b2f",
        "medium": "#f59e0b",
        "low": "#208091",
        "info": "#627c71",
    }

    payload = {
        "attachments": [
            {
                "color": colors.get(severity, colors["info"]),
                "title": f"🚨 {severity.upper()} Alert",
                "text": message,
                "footer": "SecureGuard Security Monitoring",
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            await client.post(settings.SLACK_WEBHOOK_URL, json=payload)
        return True
    except Exception:
        return False
