import datetime
import json
from os import getenv

import requests
from discord import ApplicationContext, Embed
from discord.commands import Option, slash_command
from discord.ext.commands import BucketType, cooldown
from tools.cog import Cog
from tools.colors import Colors


class APOD(Cog, name="APOD"):
    """Retrieves an Astronomy Picture Of the Day"""

    def __init__(self, bot):
        self.Bot = bot
        self.name = "APOD"
        self.api_key = getenv("NASA_API_KEY", "")

    @slash_command(name="apod")
    @cooldown(2, 6, BucketType.user)
    async def apod(self, ctx: ApplicationContext, date: Option(str, "Date in MM/DD/YYYY format (Or type \"random\" for a random date)", required=False, default=None)):
        """Astronomy Picture Of the Day"""

        await ctx.defer(ephemeral=bool(ctx.guild))

        endpoint = "https://api.nasa.gov/planetary/apod"

        if not date:
            url = f"{endpoint}?api_key={self.api_key}&thumbs=true"
        elif date == "random":
            url = f"{endpoint}?api_key={self.api_key}&thumbs=true&count=1"
        else:
            try:
                d = datetime.datetime.strptime(date, "%m/%d/%Y")

            except ValueError:
                await ctx.respond("That is not a valid date format! (I need `MM/DD/YYYY`)", ephemeral=bool(ctx.guild))
                return
            else:
                apiDate = d.strftime("%Y-%m-%d")
                url = f"{endpoint}?api_key={self.api_key}&thumbs=true&date={apiDate}"

        response = requests.get(url=url)
        if response.status_code == 404:
            await ctx.respond("I was unable to reach the APOD API!", ephemeral=True)
            return

        if response.status_code == 400:
            data = json.loads(response.text)
            await ctx.respond(data.get("msg"), ephemeral=True)
            return

        data = json.loads(response.text)
        if isinstance(data, list):
            data = data[0]

        title = data.get("title") or Embed.Empty
        description = data.get("explanation") or Embed.Empty
        d = datetime.date.fromisoformat(data.get("date"))

        websiteDate = d.strftime("%y%m%d")
        url = f"https://apod.nasa.gov/apod/ap{websiteDate}.html"

        embed = Embed(title=title, url=url,
                      description=description, color=Colors.orange())

        footerDate = d.strftime("%m/%d/%Y")
        copyright = data.get("copyright")

        if copyright:
            embed.set_footer(text=f"{footerDate}\nCopyright {copyright}")
        else:
            embed.set_footer(text=footerDate)

        image = data.get("thumbnail_url") or data.get(
            "hdurl") or data.get("url")
        if image:
            embed.set_image(url=image)

        embed.set_author(name="NASA", url="https://www.nasa.gov/",
                         icon_url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648786130/Bot%20Assets/Quasar/nasa_logo.png")

        await ctx.respond(embed=embed, ephemeral=bool(ctx.guild))


def setup(bot):
    bot.add_cog(APOD(bot))
