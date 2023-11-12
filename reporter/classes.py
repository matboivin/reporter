"""Data models."""
from dataclasses import dataclass

from discord import Message as DiscordMessage


@dataclass
class Server:
    """Class defining a Discord server.

    Attributes
    ----------
    discord_id : str
        Discord guild ID.
    name : str
        The server's name.
    created_at : str, optional
        The chat's creation date in ISO 8601 format.
    member_count : int, optional
        The number of users in the server.
    owner_id : int, optional
        Owner Discord user ID.

    Class methods
    -------------
    from_message(discord_guild)
        Create instance from discord.Guild.

    """

    discord_id: str
    name: str
    created_at: str | None = None
    member_count: int | None = None
    owner_id: int | None = None

    @classmethod
    def from_guild(cls, discord_guild: Guild):  # type: ignore
        """Create instance from discord.Guild."""
        return cls(
            discord_id=str(discord_guild.id),
            name=discord_guild.name,
            created_at=discord_guild.created_at.isoformat(),
            member_count=discord_guild.member_count,
            owner_id=discord_guild.owner_id,
        )


@dataclass
class Channel:
    """Class defining a Discord channel.

    Attributes
    ----------
    discord_id : str
        Discord channel ID.
    name : str
        The channel's name.
    server_id : str
        Discord guild ID.

    Class methods
    -------------
    from_message(discord_message)
        Create instance from discord.Message.

    """

    discord_id: str
    name: str
    server_id: str

    @classmethod
    def from_message(cls, discord_message: DiscordMessage):  # type: ignore
        """Create instance from discord.Message."""
        return cls(
            discord_id=str(discord_message.channel.id),
            name=discord_message.channel.name,
            server_id=discord_message.guild.owner_id,
        )


@dataclass
class User:
    """Class defining a Discord User.

    Attributes
    ----------
    discord_id : str
        Discord user ID.
    username : str
        User's name.
    discriminator : str, optional
        Four digits sequence that used to be put after username.

    Class methods
    -------------
    from_message(discord_message)
        Create instance from discord.Message.

    """

    discord_id: str
    username: str
    discriminator: str = ""

    @classmethod
    def from_message(cls, discord_message: DiscordMessage):  # type: ignore
        """Create instance from discord.Message."""
        return cls(
            discord_id=str(discord_message.author.id),
            username=discord_message.author.name,
            discriminator=discord_message.author.discriminator,
        )


@dataclass
class Message:
    """Class defining a message.

    Attributes
    ----------
    discord_id : str
        Discord message ID.
    created_at : str
        Date and time the message was sent in ISO 8601 format.
    content : str
        The content in text format.
    author_id : str
        The author Discord ID.
    channel_id : str
        The channel Discord ID.
    server_id : str
        The server Discord ID.
    edited : bool, default=False
        True if the message is an edited one (default: False).
    attachments_url : str, optional
        Attachments CDN links.

    """

    discord_id: str
    created_at: str
    content: str
    author_id: str
    channel_id: str
    server_id: str
    edited: bool = False
    attachments_url: str | None = None
