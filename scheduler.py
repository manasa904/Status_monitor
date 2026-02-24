import asyncio
from typing import List
from providers.base import StatusProvider
from models import StatusEvent
import logging

class Scheduler:
    def __init__(self, providers: List[StatusProvider], interval: int = 60):
        self.providers = providers
        self.interval = interval
        self._running = True

    async def _run_provider(self, provider: StatusProvider):
        while self._running:
            try:
                events = await provider.fetch_events()
                for event in events:
                    self._print_event(event)
            except Exception as e:
                print(f"[ERROR] {provider.name()} -> {e}")

            await asyncio.sleep(self.interval)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)

    def _extract_product(self, title: str) -> str:
        keywords = {
        "ChatGPT": "ChatGPT",
        "Codex": "Codex",
        "Sora": "Sora",
        "Image": "Image API",
        "Embedding": "Embeddings API",
        "Responses": "Responses API",
        "Finetuning": "Finetuning API",
        "Login": "Authentication",
        "Slack": "Slack Connector",
        "Github": "GitHub Integration",
        }

        for key, value in keywords.items():
            if key.lower() in title.lower():
                return value

        return "OpenAI Platform"

    def _print_event(self, event: StatusEvent):
        product = self._extract_product(event.title)

        print(
            f"[{event.published_at.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Product: {product}\n"
            f"Status: {event.title}\n"
        )

    async def start(self):
        tasks = [
            asyncio.create_task(self._run_provider(provider))
            for provider in self.providers
        ]

        await asyncio.gather(*tasks)

    def stop(self):
        self._running = False