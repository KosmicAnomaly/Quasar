from discord import ApplicationContext, Embed, Option, slash_command
from discord.ext.commands import BucketType, cooldown
from discord.utils import utcnow
from skyfield import almanac, api
from tools.cog import Cog
from tools.colors import Colors
from tools.tools import degree_to_cardinal


class Visible(Cog, name="Visible"):
    """Displays what objects are currently visible in the night sky"""

    def __init__(self, bot):
        super().__init__(bot)
        self.timescale = api.load.timescale()
        self.planets = api.load("de421.bsp")
        self.visible_planets = [
            {"name": "Mercury", "id": "Mercury Barycenter"},
            {"name": "Venus", "id": "Venus Barycenter"},
            {"name": "Mars", "id": "Mars Barycenter"},
            {"name": "Jupiter", "id": "Jupiter Barycenter"},
            {"name": "Saturn", "id": "Saturn Barycenter"}
        ]

    @slash_command(name="visible")
    @cooldown(1, 5, BucketType.user)
    async def visible(self, ctx: ApplicationContext, latitude: Option(float, "Your latitude (in degrees)", min_value=-90.0, max_value=90.0, required=True), longitude: Option(float, "Your longitude (in degrees)", min_value=-180.0, max_value=180.0, required=True), elevation: Option(float, "Your elevation (in meters)", min_value=-414.0, max_value=8848.0, required=False, default=0)):
        """Retrieves what planets are over 15° above the horizon and are visible with the naked eye"""

        await ctx.defer(ephemeral=bool(ctx.guild))

        latlon = api.wgs84.latlon(latitude, longitude, elevation_m=elevation)

        position = self.planets["earth"] + latlon

        sunState = almanac.sunrise_sunset(self.planets, latlon)

        now = self.timescale.from_datetime(utcnow())

        if sunState(now):
            await ctx.respond("It's daytime...\nYou can probably see the Sun but not much else", ephemeral=bool(ctx.guild))
            return

        embed = Embed(title="Visible Planets", color=Colors.violet())

        anythingVisible = False

        for p in self.visible_planets:

            astrometric = position.at(now).observe(self.planets[p["id"]])
            apparent = astrometric.apparent()
            alt, az, distance = apparent.altaz()

            alt = round(alt._degrees, 1)
            az = round(az._degrees, 1)

            direction = degree_to_cardinal(az)

            direction = degree_to_cardinal(az)
            if alt >= 15:
                data = f"Altitude: `{alt}°`\nAzimuth: `{az}° {direction}`"

                embed.add_field(name=p["name"], value=data, inline=True)
                anythingVisible = True

        if anythingVisible:
            await ctx.respond(embed=embed, ephemeral=bool(ctx.guild))
        else:
            await ctx.respond("No planets are visible right now, check again later!", ephemeral=bool(ctx.guild))


def setup(bot):
    bot.add_cog(Visible(bot))
