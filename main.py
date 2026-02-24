import asyncio
import argparse
from scheduler import Scheduler
from state import StateStore
from providers.openai_rss import OpenAIStatusProvider


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=60)
    args = parser.parse_args()

    state = StateStore()
    provider = OpenAIStatusProvider(state)

    scheduler = Scheduler([provider], interval=args.interval)

    try:
        await scheduler.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        scheduler.stop()

if __name__ == "__main__":
    asyncio.run(main())