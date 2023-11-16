# Reporter

Store every message of Discord servers joined by a bot in a SQLite database.

## Prerequisites

- A Discord bot
- Docker
- Docker Compose v2
- GNU make (optional)

## Installation

1. Get the bot token.

2. Set `.env` file.

```sh
COMPOSE_PROJECT_NAME=reporter
COMPOSE_FILE=docker-compose.yml
BOT_TOKEN=  # Discord bot token
```

3. Build the project using either the Makefile alias or docker CLI:

  ```console
  $ make up-build  # docker compose up --build --detach
  ```

## Usage

Available options:

```console
reporter [-h] [-d] [-f filename.db]

Discord bot to listen to server's messages.

options:
  -h, --help            show this help message and exit
  -d, --debug           display debug logs
  -f filename.db, --database-file filename.db
                        SQLite database filename (default: 'discord.db')
```

Run the project:

```console
$ make up  # docker compose up --detach
```

Stop the project:

```console
$ make stop  # docker compose stop
```

Other common tasks can be found in the Makefile.

## Database

See the [database diagram](docs/discord_db.png).

Database will be created in the `logs` directory. Default database name is `discord.db`. To change it, edit the command in `docker-compose.yml`

Example:

```yaml
services:
  bot:
    ...
    command: ["reporter", "--database-file", "myfile.db"]
```

The file will be available at `logs/myfile.db`.
