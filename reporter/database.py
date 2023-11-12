"""SQLite helpers."""
from sqlite3 import Cursor

sql_create_servers_table: str = """
CREATE TABLE IF NOT EXISTS servers (
    id integer PRIMARY KEY,
    discord_id text UNIQUE,
    name text NOT NULL,
    created_at text,
    members_count integer,
    owner_id
);
"""

sql_create_channels_table: str = """
CREATE TABLE IF NOT EXISTS channels (
    id integer PRIMARY KEY,
    discord_id text UNIQUE,
    name text NOT NULL
);
"""

sql_create_users_table: str = """
CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    discord_id text UNIQUE,
    username text NOT NULL,
    display_name text NOT NULL,
    discriminator text
);
"""

sql_create_messages_table: str = """
CREATE TABLE IF NOT EXISTS messages (
    id integer PRIMARY KEY,
    discord_id text,
    created_at text,
    content text NOT NULL,
    author_id,
    channel_id,
    server_id,
    edited boolean NOT NULL,
);
"""


def create_tables(cursor: Cursor) -> None:
    """Create all tables.

    Parameters
    ----------
    cursor : sqlite3.Cursor
        Database cursor.

    Raises
    ------
    sqlite3.Error

    """
    cursor.execute(sql_create_servers_table)
    cursor.execute(sql_create_channels_table)
    cursor.execute(sql_create_users_table)
    cursor.execute(sql_create_messages_table)
