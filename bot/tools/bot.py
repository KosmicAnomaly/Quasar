import logging
from contextlib import suppress

from discord import AllowedMentions, Bot, Guild, HTTPException, Intents
from discord.utils import utcnow

logger = logging.getLogger("quasar")


class Quasar(Bot):
    def __init__(self):

        super().__init__(
            chunk_guilds_at_startup=False,
            help_command=None,
            heartbeat_timeout=120.0,
            allowed_mentions=AllowedMentions.none(),
            intents=Intents(guilds=True)
        )

        self.last_disconnect = None
        self.connected = False

    def process_reconnect(self):
        self.connected = True
        if self.last_disconnect:
            seconds = (utcnow() - self.last_disconnect).total_seconds()
            if seconds >= 60:
                logger.warning(
                    f"Reconnected to Discord after {seconds} seconds of downtime")

    async def on_ready(self):
        if not hasattr(self, "start_time"):
            self.start_time = utcnow()
            logger.info(
                f"{self.user} has logged into Discord (Running on {len(self.guilds)} servers)")

        if not self.connected:
            self.process_reconnect()

    async def on_connect(self):
        if not self.connected:
            self.process_reconnect()

        await self.sync_commands(force=True)

    async def on_resumed(self):
        if not self.connected:
            self.process_reconnect()

    async def on_disconnect(self):
        if self.connected:
            self.connected = False
            self.last_disconnect = utcnow()

    async def on_guild_join(self, guild: Guild):
        """Log when Quasar joins a server"""
        logger.info(
            f"{self.user} joined a server (Name: {guild.name}, ID: {guild.id}, Member Count: {guild.member_count})")

    async def on_guild_remove(self, guild: Guild):
        """Log when Quasar leaves a server"""
        logger.info(
            f"{self.user} was removed from a server (Name: {guild.name}, ID: {guild.id})")

    async def get_or_fetch_channel(self, id: int):
        channel = self.get_channel(id)
        if not channel:
            with suppress(HTTPException):
                channel = await self.fetch_channel(id)
        return channel
