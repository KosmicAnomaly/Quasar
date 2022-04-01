from discord import ApplicationContext, Embed, SlashCommandGroup
from discord.ext.commands import BucketType, cooldown
from discord.utils import utcnow
from skyfield import eclipselib
from skyfield.api import load
from tools.cog import Cog
from tools.colors import Colors


class Eclipse(Cog, name="Eclipse"):
    """Returns dates of upcoming eclipses"""

    def __init__(self, bot):
        super().__init__(bot)
        self.eph = load("de421.bsp")
        self.timescale = load.timescale()

    RootGroup = SlashCommandGroup(
        "eclipse", "Commands related to eclipses")

    @RootGroup.command(name="lunar")
    @cooldown(1, 10, BucketType.user)
    async def lunar(self, ctx: ApplicationContext):
        """Retrieves the lunar eclipses over the next two years"""

        await ctx.defer(ephemeral=bool(ctx.guild))

        now = utcnow()
        timeNow = self.timescale.utc(now.year, now.month, now.day)
        timeLater = self.timescale.utc(now.year+2, now.month, now.day)

        times, y, details = eclipselib.lunar_eclipses(
            timeNow, timeLater, self.eph)

        embed = Embed(title="Upcoming Lunar Eclipses", color=Colors.moon())

        description = ""
        for ti, yi in zip(times, y):
            ts = int(ti.utc_datetime().timestamp())
            type = eclipselib.LUNAR_ECLIPSES[yi]
            description += f"{type} Eclipse on <t:{ts}:f>\n"

        embed.description = description

        await ctx.respond(embed=embed, ephemeral=bool(ctx.guild))


def setup(bot):
    bot.add_cog(Eclipse(bot))
