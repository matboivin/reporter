# Discord bot

Discord bot to listen to messages.

## Prerequisites

- A Discord bot
- GNU make
- Docker
- Docker Compose v2

## Installation

1. Get the bot token.

2. Set `.env` file.

```sh
COMPOSE_PROJECT_NAME=reporter
COMPOSE_FILE=docker-compose.yml
BOT_TOKEN=  # Token of the Telegram bot
```

3. Build the project:

  ```console
  $ make up-build
  ```
