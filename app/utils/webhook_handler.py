"""Webhook handling utilities."""

from typing import Dict, Any, Callable
from datetime import datetime
import asyncio


class WebhookManager:
    """Manage webhooks."""

    def __init__(self):
        self.webhooks: Dict[str, list] = {}

    def register(self, event_type: str, callback: Callable):
        """Register webhook callback for event type."""
        if event_type not in self.webhooks:
            self.webhooks[event_type] = []
        self.webhooks[event_type].append(callback)

    async def trigger(self, event_type: str, data: Dict[str, Any]):
        """Trigger all webhooks for event type."""
        if event_type in self.webhooks:
            tasks = [
                callback({"event": event_type, "data": data, "timestamp": datetime.now().isoformat()})
                for callback in self.webhooks[event_type]
            ]
            await asyncio.gather(*tasks, return_exceptions=True)


webhook_manager = WebhookManager()
