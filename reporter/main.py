"""Program's entrypoint."""
from argparse import ArgumentParser, Namespace
from os import getenv
from sqlite3 import Connection, connect

from aiohttp.client_exceptions import ClientConnectorError
from discord import Client

from .bot_client import init_bot
from .database import create_tables
from .logger import log_to_file, programLogger, set_logger


def parse_args() -> Namespace:
    """Parse the arguments of the program.

    Returns
    -------
    argparse.Namespace
        Command line arguments of the program.

    """
    parser: ArgumentParser = ArgumentParser(
        description="Discord bot to listen to server's messages."
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="display debug logs"
    )
    parser.add_argument(
        "-f",
        "--database-file",
        type=str,
        metavar="filename.db",
        default="discord.db",
        help="SQLite database filename (default: 'discord.db')",
    )

    return parser.parse_args()


def entrypoint() -> None:
    """Program's entrypoint."""
    args: Namespace = parse_args()
    bot_token: str | None = getenv("BOT_TOKEN")

    set_logger(args.debug)

    if not bot_token:
        programLogger.error("Missing environment variable: BOT_TOKEN.")
        return

    try:
        connection: Connection = connect(f"logs/{args.database_file}")
        programLogger.debug(f"Connected to database '{args.database_file}'")
        create_tables(connection)

        bot: Client = init_bot(connection)

        bot.run(bot_token)

    except ClientConnectorError as err:
        log_to_file(str(err))

    except KeyboardInterrupt:
        programLogger.notice("Program interrupted.")

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    entrypoint()
