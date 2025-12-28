"""Rate limiting utilities."""

from datetime import datetime, timedelta
from typing import Dict


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, requests: int = 100, period: int = 60):
        self.requests = requests
        self.period = period
        self.requests_map: Dict[str, list] = {}

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for client."""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.period)

        if client_id not in self.requests_map:
            self.requests_map[client_id] = []

        # Remove old requests
        self.requests_map[client_id] = [
            req_time
            for req_time in self.requests_map[client_id]
            if req_time > cutoff
        ]

        if len(self.requests_map[client_id]) < self.requests:
            self.requests_map[client_id].append(now)
            return True

        return False
