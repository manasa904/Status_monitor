# OpenAI Status Monitor (Event-Driven Incident Tracker)

## Overview

This project implements a lightweight, asynchronous monitoring system that tracks service incidents from the OpenAI Status Page.

The system:

1. Monitors the official OpenAI RSS status feed  
2. Detects new incidents, outages, and degradations  
3. Logs the affected product/service and latest status message  
4. Avoids reprocessing previously seen incidents  

The implementation is designed to be scalable, event-driven, and extensible to support monitoring 100+ similar status pages.

No UI or database is used — console output is sufficient by design.


## Methodology

### Incident Ingestion

The system consumes the official RSS feed:

```
https://status.openai.com/feed.rss
```

RSS is used instead of HTML scraping because:

- It provides structured data
- It reduces bandwidth overhead
- It avoids brittle parsing logic
- It is designed for event-based consumption


### Asynchronous Architecture

The system is built using:

- `asyncio`
- `httpx.AsyncClient`

This ensures:

- Non-blocking I/O
- Efficient periodic checks
- Scalability across multiple providers
- Clean separation of responsibilities

Each provider runs as an independent async task managed by a scheduler.


### Provider Abstraction

A base `StatusProvider` interface is defined to support extensibility.

New providers can be added by implementing the same interface and registering them in the scheduler.

This allows the system to scale horizontally to monitor multiple services.


### Efficient Update Detection

To prevent redundant processing:

- RSS feeds are processed from newest → oldest
- Once a previously seen incident is encountered, parsing stops
- Only unseen incidents are logged

This ensures:

- Minimal overhead
- Idempotent execution
- Clean event detection

State is stored in-memory for simplicity.

### Product Identification

The affected product/service is inferred using lightweight keyword matching from incident titles.

Examples:

- "ChatGPT" → ChatGPT
- "Codex" → Codex
- "Sora" → Sora
- "image" → Image API
- "finetuning" → Finetuning API
- otherwise → OpenAI Platform

This heuristic approach satisfies the requirement to extract affected services without relying on undocumented APIs.


## Project Structure

```
status_monitor/
│
├── main.py
├── scheduler.py
├── state.py
├── models.py
├── providers/
│   ├── __init__.py
│   ├── base.py
│   └── openai_rss.py
└── requirements.txt
```


## Usage

### Install Dependencies

```
pip install -r requirements.txt
```

### Run the Monitor

```
python main.py --interval 60
```

Optional parameter:

```
--interval <seconds>
```

Defines how often the RSS feed is checked.


## Example Output

```
[2026-02-23 16:09:30]
Product: ChatGPT
Status: Elevated Error Rate for ChatGPT Conversations for Business and Enterprise Customers
```

The system remains silent if no new incidents are detected.


## Limitations

- State resets on application restart
- Product detection uses keyword heuristics
- Uses periodic RSS polling (webhooks would be more efficient if available)

## Future Improvements

- Persistent state storage (Redis / SQLite)
- Structured product extraction from API (if available)
- Webhook-based real-time ingestion
- Alert integrations (Slack / Email)
- Centralized logging


## Summary

This solution emphasizes:

- Clean modular architecture
- Asynchronous execution
- Efficient update detection
- Extensibility to multiple providers
- Avoidance of inefficient polling or HTML scraping

The focus was to build a maintainable and scalable monitoring framework rather than a simple script.
