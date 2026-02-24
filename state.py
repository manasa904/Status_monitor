from typing import Dict, Set, Optional


class StateStore:
    def __init__(self):
        self.seen_events: Dict[str, Set[str]] = {}
        self.etags: Dict[str, Optional[str]] = {}
        self.last_modified: Dict[str, Optional[str]] = {}

    def is_new_event(self, provider: str, event_id: str) -> bool:
        if provider not in self.seen_events:
            self.seen_events[provider] = set()

        if event_id in self.seen_events[provider]:
            return False

        self.seen_events[provider].add(event_id)
        return True

    def get_etag(self, provider: str) -> Optional[str]:
        return self.etags.get(provider)

    def set_etag(self, provider: str, etag: Optional[str]):
        self.etags[provider] = etag

    def get_last_modified(self, provider: str) -> Optional[str]:
        return self.last_modified.get(provider)

    def set_last_modified(self, provider: str, value: Optional[str]):
        self.last_modified[provider] = value