from discord import ApplicationContext, Embed
from discord.commands import slash_command
from discord.ext.commands import BucketType, cooldown
from discord.utils import utcnow
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from tools.cog import Cog
from tools.colors import Colors


class Phase(Cog, name="Moon Phase"):
    """Returns what phase the Moon is in"""

    def __init__(self, bot):
        super().__init__(bot)
        eph = load("de421.bsp")
        self.sun, self.moon, self.earth = eph["sun"], eph["moon"], eph["earth"]
        self.timescale = load.timescale()

    @slash_command(name="phase")
    @cooldown(1, 10, BucketType.user)
    async def phase(self, ctx: ApplicationContext):
        """Retrieves the current phase of the Moon"""
        now = utcnow()
        time = self.timescale.utc(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

        e = self.earth.at(time)
        _, slon, _ = e.observe(
            self.sun).apparent().frame_latlon(ecliptic_frame)
        _, mlon, _ = e.observe(
            self.moon).apparent().frame_latlon(ecliptic_frame)
        phaseDegrees = (mlon.degrees - slon.degrees) % 360.0

        embed = Embed(color=Colors.moon())

        if phaseDegrees <= 22.5:
            embed.title = "New Moon"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786241/Bot%20Assets/Quasar/moon_phases/new_moon.png")

        elif phaseDegrees <= 67.5:
            embed.title = "Waxing Crescent"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786242/Bot%20Assets/Quasar/moon_phases/waxing_crescent.png")

        elif phaseDegrees <= 112.5:
            embed.title = "First Quarter"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786242/Bot%20Assets/Quasar/moon_phases/first_quarter.png")

        elif phaseDegrees <= 157.5:
            embed.title = "Waxing Gibbous"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786242/Bot%20Assets/Quasar/moon_phases/waxing_gibbous.png")

        elif phaseDegrees <= 202.5:
            embed.title = "Full Moon"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786242/Bot%20Assets/Quasar/moon_phases/full_moon.png")

        elif phaseDegrees <= 247.5:
            embed.title = "Waning Gibbous"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786242/Bot%20Assets/Quasar/moon_phases/waning_gibbous.png")

        elif phaseDegrees <= 292.5:
            embed.title = "Third Quarter"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786242/Bot%20Assets/Quasar/moon_phases/third_quarter.png")

        elif phaseDegrees <= 337.5:
            embed.title = "Waning Crescent"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786241/Bot%20Assets/Quasar/moon_phases/waning_crescent.png")

        else:
            embed.title = "New Moon"
            embed.set_thumbnail(
                url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786241/Bot%20Assets/Quasar/moon_phases/new_moon.png")

        embed.set_footer(text=f"Angle: {round(phaseDegrees,1)}°")

        if ctx.guild:
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Phase(bot))
