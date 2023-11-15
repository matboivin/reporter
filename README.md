# Reporter

Store every message of Discord servers joined by a bot in a SQLite database.

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
BOT_TOKEN=  # Discord bot token
```

3. Build the project:

  ```console
  $ make up-build  # docker compose up --build --detach
  ```

4. Database will be mounted in `logs` directory.

## Usage

Run the project:

```console
$ make up  # docker compose up --detach
```

## Database

See the [database diagram](docs/discord_db.png).

To change the database filename, edit the command in `docker-compose.yml`. Example:

```yaml
services:
  bot:
    ...
    command: ["reporter", "--database-name", "myfile.db"]
```

The file will be available at `logs/myfile.db`.
