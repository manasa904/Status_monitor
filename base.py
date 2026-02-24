from abc import ABC, abstractmethod
from typing import List
from models import StatusEvent


class StatusProvider(ABC):
    @abstractmethod
    async def fetch_events(self) -> List[StatusEvent]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass