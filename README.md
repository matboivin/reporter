# Reporter

Store every message of servers joined by a bot.

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
BOT_TOKEN=  # Token of the Discord bot
```

3. Build the project:

  ```console
  $ make up-build
  ```

4. Database will be mounted in `logs` directory.

## Usage

Run the project:

```console
$ make up
```
