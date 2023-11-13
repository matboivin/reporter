"""Discord bot client."""
from sqlite3 import Connection

from discord import Client, DMChannel, GroupChannel, Intents
from discord import Message as DiscordMessage
from discord import MessageType

from .classes import Channel, Message, Server, User
from .database import create_channel, create_message, create_server, create_user
from .logger import log_to_file, programLogger


def ignore_message(client: Client, discord_message: DiscordMessage) -> bool:
    """Check whether to ignore incoming message.

    Parameters
    ----------
    client : discord.Client
        The Discord client.
    discord_message : discord.Message
        A Discord Message.

    Returns
    -------
    bool

    """
    # Ignore own messages.
    if discord_message.author == client.user:
        return True

    # Ignore DMs
    if isinstance(discord_message.channel, GroupChannel) or isinstance(
        discord_message.channel, DMChannel
    ):
        return True

    # Ignore informational messages
    if discord_message.type not in (MessageType.default, MessageType.reply):
        return True

    return False


async def process_message(
    connection: Connection,
    discord_message: DiscordMessage,
    is_edited: bool = False,
) -> None:
    """Parse message.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.
    discord_message : discord.Message
        An incoming Discord Message.
    is_edited : bool, default=False
        Whether the message was edited.

    """
    try:
        message: Message = Message(
            discord_id=str(discord_message.id),
            created_at=discord_message.edited_at.isoformat()
            if is_edited
            else discord_message.created_at.isoformat(),
            content=discord_message.content,
            author_id=create_user(
                connection, User.from_message(discord_message)
            ),
            channel_id=create_channel(
                connection, Channel.from_message(discord_message)
            ),
            server_id=create_server(
                connection, Server.from_guild(discord_message.guild)
            ),
            is_edited=int(is_edited),
        )

        if discord_message.attachments:
            attachment_links: list[str] = [
                attachment.url for attachment in discord_message.attachments
            ]
            message.attachments_url = ", ".join(attachment_links)

    except AttributeError as err:
        log_to_file(f"Couldn't process message: {err}")

    else:
        create_message(connection, message)


def init_bot(connection: Connection) -> Client:
    """Initialize the Discord bot client.

    Parameters
    ----------
    connection : sqlite3.Connection
        Database connection interface.

    Returns
    -------
    discord.Client
        The Discord client.

    """
    intents: Intents = Intents.default()
    intents.message_content = True
    client: Client = Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        """Log when bot is ready."""
        programLogger.notice(f"Bot '{client.user}' connected.")

    @client.event
    async def on_message(discord_message: DiscordMessage) -> None:
        """Handle new message event.

        Parameters
        ----------
        discord_message : discord.Message
            An incoming Discord Message

        """
        if ignore_message(client, discord_message):
            return

        await process_message(connection, discord_message)

    @client.event
    async def on_message_edit(
        before: DiscordMessage, after: DiscordMessage
    ) -> None:
        """Handle edited message event.

        Parameters
        ----------
        before : discord.Message
            The Discord Message before editing.
        after : discord.Message
            The Discord Message after editing.

        """
        if ignore_message(client, after):
            return

        await process_message(connection, after, is_edited=True)

    return client
