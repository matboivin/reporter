"""Discord bot client."""

from discord import Client, DMChannel, GroupChannel, Intents
from discord import Message as DiscordMessage
from discord import MessageType
from rich.pretty import pprint

from .classes import Channel, Message, Server, User
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
    discord_message: DiscordMessage, is_edited: bool = False
) -> None:
    """Parse message.

    Parameters
    ----------
    discord_message : discord.Message
        An incoming Discord Message.
    is_edited : bool, default=False
        Whether the message was edited.

    """
    try:
        author: User = User.from_message(discord_message)
        channel: Channel = Channel.from_message(discord_message)
        message: Message = Message(
            discord_id=str(discord_message.id),
            created_at=discord_message.edited_at.isoformat()
            if is_edited
            else discord_message.created_at.isoformat(),
            content=discord_message.content,  # TODO
            author_id=str(discord_message.author.id),  # TODO
            channel_id=str(discord_message.channel.id),  # TODO
            server_id=discord_message.guild.owner_id,
            edited=is_edited,
        )

        if discord_message.attachments:
            attachment_links: list[str] = [
                attachment.url for attachment in discord_message.attachments
            ]
            message.attachments_url = ", ".join(attachment_links)

    except AttributeError as err:
        log_to_file(f"Couldn't process message: {err}")

    else:
        pprint(author)
        pprint(channel)
        pprint(message)


def init_bot() -> Client:
    """Initialize the Discord bot client.

    Returns
    -------
    discord.Client
        The Discord client.

    """
    intents: Intents = Intents.default()
    intents.message_content = True  # Defaut perm
    client: Client = Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        """Log when bot is ready."""
        programLogger.notice(f"Bot '{client.user}' connected.")

        # Display all joined servers
        joined_servers: list[Server] = []

        for guild in client.guilds:
            joined_servers.append(Server.from_guild(guild))

        pprint(joined_servers)
        # TODO: Store in DB

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

        await process_message(discord_message)

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

        await process_message(after, is_edited=True)

    return client
