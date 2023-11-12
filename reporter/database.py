"""SQLite helpers."""
from dataclasses import astuple
from sqlite3 import Connection, Cursor
from sqlite3 import Error as SqliteError

from rich.pretty import pretty_repr

from .classes import Server
from .logger import programLogger

sql_create_servers_table: str = """
CREATE TABLE IF NOT EXISTS servers (
    id integer PRIMARY KEY,
    discord_id text UNIQUE,
    name text NOT NULL,
    created_at text,
    member_count integer,
    owner_id text
);
"""

sql_create_channels_table: str = """
CREATE TABLE IF NOT EXISTS channels (
    id integer PRIMARY KEY,
    discord_id text NOT NULL,
    name text NOT NULL,
    server_id text NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers (id)
);
"""

sql_create_users_table: str = """
CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    discord_id text UNIQUE,
    username text NOT NULL,
    discriminator text,
);
"""

sql_create_messages_table: str = """
CREATE TABLE IF NOT EXISTS messages (
    id integer PRIMARY KEY,
    discord_id text NOT NULL,
    created_at text NOT NULL,
    content text NOT NULL,
    author_id text NOT NULL,
    channel_id text NOT NULL,
    server_id text NOT NULL,
    is_edited integer NOT NULL,
    attachments_url text,
    FOREIGN KEY (author_id) REFERENCES users (id),
    FOREIGN KEY (channel_id) REFERENCES channels (id),
    FOREIGN KEY (server_id) REFERENCES servers (id)
);
"""


def create_tables(connection: Connection) -> None:
    """Create all tables.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.

    Raises
    ------
    sqlite3.Error

    """
    cursor: Cursor = connection.cursor()
    programLogger.debug("Creating tables ...")

    cursor.execute(sql_create_servers_table)
    programLogger.debug("Created servers table.")
    cursor.execute(sql_create_channels_table)
    programLogger.debug("Created channels table.")
    cursor.execute(sql_create_users_table)
    programLogger.debug("Created users table.")
    cursor.execute(sql_create_messages_table)
    programLogger.debug("Created messages table.")


def create_server(connection: Connection, server: Server) -> int | None:
    """Insert a new server row.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.
    server : Server
        The server data.

    Returns
    -------
    int or None
        The generated ID if object was created. Otherwise, None.

    """
    query: str = (
        "INSERT INTO servers(discord_id,name,created_at,member_count, owner_id)"
        "VALUES(?,?,?,?,?)"
    )
    cursor: Cursor = connection.cursor()

    try:
        cursor.execute(query, astuple(server))
        connection.commit()
        server_id: int | None = cursor.lastrowid
        programLogger.debug(
            f"Created server ID: {server_id}, data: {pretty_repr(server)}"
        )

    except SqliteError as err:
        programLogger.error(f"Failed creating server: {err}")
        return None

    return server_id
