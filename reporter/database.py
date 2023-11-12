"""SQLite helpers."""
from dataclasses import astuple
from sqlite3 import Connection, Cursor
from sqlite3 import Error as SqliteError
from sqlite3 import IntegrityError
from typing import Any, Literal

from rich.pretty import pretty_repr

from .classes import Channel, Message, Server, User
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
    server_id int NOT NULL,
    FOREIGN KEY (server_id) REFERENCES servers (id)
);
"""

sql_create_users_table: str = """
CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    discord_id text UNIQUE,
    username text NOT NULL,
    discriminator text
);
"""

sql_create_messages_table: str = """
CREATE TABLE IF NOT EXISTS messages (
    id integer PRIMARY KEY,
    discord_id text NOT NULL,
    created_at text NOT NULL,
    content text NOT NULL,
    author_id int,
    channel_id int,
    server_id int,
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


def fetch_by_discord_id(
    connection: Connection, table: Literal["servers", "users"], discord_id: str
) -> int | None:
    """Fetch object ID by Discord unique ID.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.
    table : str
        The table name.
    discord_id : str
        The object Discord unique ID.

    Returns
    -------
    int or None
        The ID if object was found. Otherwise, None.

    """
    query: str = f"SELECT id FROM {table} WHERE discord_id=?"  # nosec
    cursor: Cursor = connection.cursor()

    try:
        result: Cursor = cursor.execute(query, (discord_id,))
        first_result: Any | None = result.fetchone()

        if first_result:
            return int(first_result[0])

    except SqliteError as err:
        programLogger.error(f"Failed fetching: {err}")

    return None


def fetch_server_channel(
    connection: Connection, channel: Channel
) -> int | None:
    """Fetch channel server.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.
    channel : Channel
        The channel data.

    Returns
    -------
    int or None
        The ID if object was found. Otherwise, None.

    """
    query: str = (
        "SELECT id FROM channels WHERE discord_id=? AND name=? AND server_id=?"
    )
    cursor: Cursor = connection.cursor()

    try:
        result: Cursor = cursor.execute(
            query, (channel.discord_id, channel.name, channel.server_id)
        )
        first_result: Any | None = result.fetchone()

        if first_result:
            return int(first_result[0])

    except SqliteError as err:
        programLogger.error(f"Failed fetching channel: {err}")

    return None


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
    server_id: int | None = None

    try:
        cursor.execute(query, astuple(server))
        connection.commit()
        server_id = cursor.lastrowid
        programLogger.debug(
            f"Created server ID: {server_id}, data: {pretty_repr(server)}"
        )

    except IntegrityError as err:
        programLogger.warning(f"Failed creating server: {err}")
        return fetch_by_discord_id(connection, "servers", server.discord_id)

    except SqliteError as err:
        programLogger.error(f"Failed creating server: {err}")

    return server_id


def create_channel(connection: Connection, channel: Channel) -> int | None:
    """Insert a new channel row.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.
    channel : Channel
        The channel data.

    Returns
    -------
    int or None
        The generated ID if object was created. Otherwise, None.

    """
    query: str = "INSERT INTO channels(discord_id,name,server_id) VALUES(?,?,?)"
    cursor: Cursor = connection.cursor()
    channel_id: int | None = fetch_server_channel(connection, channel)

    if channel_id:  # Channel already exist
        return channel_id

    try:
        cursor.execute(query, astuple(channel))
        connection.commit()
        channel_id = cursor.lastrowid
        programLogger.debug(
            f"Created channel ID: {channel_id}, data: {pretty_repr(channel)}"
        )

    except SqliteError as err:
        programLogger.error(f"Failed creating channel: {err}")

    return channel_id


def create_user(connection: Connection, user: User) -> int | None:
    """Insert a new user row.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.
    user : User
        The user data.

    Returns
    -------
    int or None
        The generated ID if object was created. Otherwise, None.

    """
    query: str = (
        "INSERT INTO users(discord_id,username,discriminator) VALUES(?,?,?)"
    )
    cursor: Cursor = connection.cursor()
    user_id: int | None = None

    try:
        cursor.execute(query, astuple(user))
        connection.commit()
        user_id = cursor.lastrowid
        programLogger.debug(
            f"Created user ID: {user_id}, data: {pretty_repr(user)}"
        )

    except IntegrityError as err:
        programLogger.warning(f"Failed creating user: {err}")
        return fetch_by_discord_id(connection, "users", user.discord_id)

    except SqliteError as err:
        programLogger.error(f"Failed creating user: {err}")

    return user_id


def create_message(connection: Connection, message: Message) -> int | None:
    """Insert a new message row.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.
    message : Message
        The message data.

    Returns
    -------
    int or None
        The generated ID if object was created. Otherwise, None.

    """
    query: str = (
        "INSERT INTO messages(discord_id,created_at,content,author_id,"
        "channel_id,server_id,is_edited,attachments_url) "
        "VALUES(?,?,?,?,?,?,?,?)"
    )
    cursor: Cursor = connection.cursor()
    message_id: int | None = None

    try:
        cursor.execute(query, astuple(message))
        connection.commit()
        message_id = cursor.lastrowid
        programLogger.debug(
            f"Created message ID: {message_id}, data: {pretty_repr(message)}"
        )

    except IntegrityError as err:
        programLogger.warning(f"Failed creating message: {err}")

    except SqliteError as err:
        programLogger.error(f"Failed creating message: {err}")

    return message_id
