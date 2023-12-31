"""Data models."""
from dataclasses import dataclass

from discord import Guild
from discord import Message as DiscordMessage
from discord import User as DiscordUser


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
    owner_id : str, optional
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
    owner_id: str | None = None

    @classmethod
    def from_guild(cls, discord_guild: Guild):  # type: ignore
        """Create instance from discord.Guild."""
        return cls(
            discord_id=str(discord_guild.id),
            name=discord_guild.name,
            created_at=discord_guild.created_at.isoformat()
            if discord_guild.created_at
            else None,
            member_count=discord_guild.member_count,
            owner_id=str(discord_guild.owner_id),
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
    server_id : int
        Discord server ID in database.

    Class methods
    -------------
    from_message(discord_message)
        Create instance from discord.Message.

    """

    discord_id: str
    name: str
    server_id: int

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
    from_user(discord_user)
        Create instance from discord.User.
    from_message(discord_message)
        Create instance from discord.Message.

    """

    discord_id: str
    username: str
    discriminator: str = ""

    @classmethod
    def from_user(cls, discord_user: DiscordUser):  # type: ignore
        """Create instance from discord.User."""
        return cls(
            discord_id=str(discord_user.id),
            username=discord_user.name,
            discriminator=discord_user.discriminator,
        )

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
    author_id : str, optional
        Discord user ID in database.
    channel_id : int, optional
        Discord channel ID in database.
    server_id : int, optional
        Discord server ID in database.
    is_edited : int, default=0
        1 if the message was edited (default: 0).
    attachments_url : str, optional
        Attachments CDN links.

    """

    discord_id: str
    created_at: str
    content: str
    author_id: int | None = None
    channel_id: int | None = None
    server_id: int | None = None
    is_edited: int = 0
    attachments_url: str | None = None
