from discord import ApplicationContext, Embed, Option, slash_command
from discord.ext.commands import BucketType, cooldown
from discord.ext.tasks import loop
from discord.utils import utcnow
from skyfield.api import load, wgs84
from tools.cog import Cog
from tools.colors import Colors
from tools.tools import degree_to_cardinal


class ISS(Cog, name="ISS"):
    """Displays where the ISS is in the night sky"""

    def __init__(self, bot):
        super().__init__(bot)
        self.timescale = load.timescale()
        self.update_tle.start()

    # update the ISS tle file every hour
    @loop(hours=1)
    async def update_tle(self):

        url = "https://celestrak.com/satcat/tle.php?CATNR=25544"
        filename = "tle-CATNR-25544.txt"
        self.ISS_TLE = load.tle_file(url, filename=filename, reload=True)[0]

    @slash_command(name="iss")
    @cooldown(1, 5, BucketType.user)
    async def iss(self, ctx: ApplicationContext, latitude: Option(float, "Your latitude (in degrees)", min_value=-90.0, max_value=90.0, required=True), longitude: Option(float, "Your longitude (in degrees)", min_value=-180.0, max_value=180.0, required=True), elevation: Option(float, "Your elevation (in meters)", min_value=-414.0, max_value=8848.0, required=False, default=0)):
        """Retrieves where the ISS is relative to your location"""

        await ctx.defer(ephemeral=bool(ctx.guild))

        position = wgs84.latlon(latitude, longitude, elevation_m=elevation)

        now = self.timescale.from_datetime(utcnow())

        embed = Embed(title="ISS Location", color=Colors.iss())

        difference = self.ISS_TLE - position

        alt, az, distance = difference.at(now).altaz()
        alt = round(alt._degrees, 1)
        az = round(az._degrees, 1)

        direction = degree_to_cardinal(az)

        embed.description = f"Altitude: `{alt}°`{' (Below the horizon)' if alt <= 0 else ''}\nAzimuth: `{az}° {direction}`"

        await ctx.respond(embed=embed, ephemeral=bool(ctx.guild))


def setup(bot):
    bot.add_cog(ISS(bot))
