import httpx
import feedparser
from datetime import datetime
from typing import List

from models import StatusEvent
from providers.base import StatusProvider
from state import StateStore


class OpenAIStatusProvider(StatusProvider):
    RSS_URL = "https://status.openai.com/feed.rss"

    def __init__(self, state: StateStore):
        self._state = state
        self._provider_name = "OpenAI"

    def name(self) -> str:
        return self._provider_name

    async def fetch_events(self) -> List[StatusEvent]:
        headers = {}

        etag = self._state.get_etag(self.name())
        last_modified = self._state.get_last_modified(self.name())

        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(self.RSS_URL, headers=headers)

        if response.status_code == 304:
            return []

        if response.status_code != 200:
            return []

        self._state.set_etag(self.name(), response.headers.get("ETag"))
        self._state.set_last_modified(
            self.name(), response.headers.get("Last-Modified")
        )

        feed = feedparser.parse(response.text)
        events: List[StatusEvent] = []

        events: List[StatusEvent] = []

        for entry in feed.entries:
            event_id = entry.get("guid") or entry.get("id") or entry.get("title")
            if not event_id:
             continue

            # Stop processing once we reach an already seen event
            if not self._state.is_new_event(self.name(), event_id):
                break

            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            else:
                published = datetime.utcnow()

            event = StatusEvent(
            provider=self.name(),
            event_id=event_id,
            title=entry.get("title", "No title"),
            summary=entry.get("summary", ""),
            published_at=published,
            )

            events.append(event)

        return events