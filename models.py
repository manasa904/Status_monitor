from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatusEvent:
    provider: str
    event_id: str
    title: str
    summary: str
    published_at: datetime