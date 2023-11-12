"""Main."""
from argparse import ArgumentParser, Namespace
from os import getenv
from sqlite3 import Connection, Cursor
from sqlite3 import Error as SqliteError
from sqlite3 import connect

from aiohttp.client_exceptions import ClientConnectorError
from discord import Client

from .bot_client import init_bot
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
        "-p",
        "--database-path",
        type=str,
        default="discord.db",
        help="path to SQLite database (default: 'discord.db')",
    )

    return parser.parse_args()


def entrypoint() -> None:
    """Program's entrypoint."""
    args: Namespace = parse_args()
    bot_token: str | None = getenv("BOT_TOKEN")

    set_logger(args.debug)

    if not bot_token:
        programLogger.error("Missing environment variables BOT_TOKEN.")
        return

    try:
        connection: Connection = connect(args.database_path)
        cursor: Cursor = connection.cursor()
        # create_tables(cursor)

        bot: Client = init_bot()

        bot.run(bot_token)  # Run until disconnect

    except (ClientConnectorError, SqliteError) as err:
        log_to_file(str(err))

    except KeyboardInterrupt:
        programLogger.notice("Program interrupted.")

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    entrypoint()
