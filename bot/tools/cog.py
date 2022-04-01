from discord import Cog
from discord.utils import utcnow


class Cog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_at = utcnow()
