import os
from math import ceil as round_up

from discord import ApplicationContext, Embed
from discord.commands import slash_command
from discord.commands.core import SlashCommand
from discord.ext.commands import BucketType, cooldown
from discord.utils import snowflake_time, utcnow
from tools.cog import Cog
from tools.colors import Colors

# this thing that counts lines of code isnt mine, I found it on stack overflow but can't remember where
aDockstring = '"""'  # prevent a weird bug
'"""'


def count_code(rootdir, total_lines: int = 0, begin_start: bool = None):
    def _get_new_lines(source):
        total = len(source)
        i = 0
        while i < len(source):
            line = source[i]
            trimline = line.lstrip(" ")

            if trimline.startswith("#") or trimline == "":
                total -= 1
            elif aDockstring in trimline:  # docstring begin
                if trimline.count(aDockstring) == 2:  # docstring end on same line
                    total -= 1
                    i += 1
                    continue
                doc_start = i
                i += 1

                while aDockstring not in source[i]:  # docstring end
                    i += 1

                doc_end = i
                total -= (doc_end - doc_start + 1)
            i += 1
        return total

    for name in os.listdir(rootdir):
        file = os.path.join(rootdir, name)
        if os.path.isfile(file) and file.endswith(".py"):
            with open(file, "r", errors="ignore") as f:
                source = f.readlines()

            new_lines = _get_new_lines(source)
            total_lines += new_lines

    for file in os.listdir(rootdir):
        file = os.path.join(rootdir, file)
        if os.path.isdir(file):
            total_lines = count_code(file, total_lines,
                                     begin_start=rootdir)
    return total_lines


class Health(Cog, name="Health"):
    """Retrieve useful bot-related information"""

    @slash_command(name="ping")
    @cooldown(1, 3, BucketType.user)
    async def ping(self, ctx: ApplicationContext):
        """Display Quasar's current ping"""

        await ctx.respond("Calculating...", ephemeral=bool(ctx.guild))

        end = utcnow()
        start = snowflake_time(ctx.interaction.id)
        roundTripTime = round_up((end-start).microseconds/1000)

        latency = round_up(self.bot.latency*1000)

        embed = Embed(
            description=f"**\~\~\~\~\~\~\~\~\~\~**\nWebsocket: **{latency}ms**\nRound Trip: **{roundTripTime}ms**\n**\~\~\~\~\~\~\~\~\~\~**", color=Colors.sea_green())
        embed.set_author(
            name=self.bot.user, icon_url=self.bot.user.avatar.url)

        embed.set_thumbnail(
            url="https://res.cloudinary.com/kosmic-anomalies/image/upload/v1648787314/Bot%20Assets/Quasar/light_swirl.gif")

        distance1Way = 4101000
        speedOfLightms = 299792.458
        lightTravelTime = distance1Way / speedOfLightms
        percentLight = round(100*(lightTravelTime/latency), 2)

        embed.set_footer(
            text=f"Transmitting data at {percentLight}% the speed of light")

        await ctx.edit(content=None, embed=embed)

    @slash_command(name="statistics")
    @cooldown(1, 5, BucketType.user)
    async def statistics(self, ctx: ApplicationContext):
        """Display detailed statistics for Quasar"""

        await ctx.defer(ephemeral=bool(ctx.guild))

        # Display latencies
        embed = Embed(
            title="Statistics", color=Colors.royal_blue())
        embed.set_author(
            name=self.bot.user, icon_url=self.bot.user.avatar.url)

        commands = [c.name for c in self.bot.walk_application_commands()
                    if isinstance(c, SlashCommand)]

        embed.add_field(
            name="Commands", value=f"```{len(commands)} Slash Commands\n```", inline=True)

        # Display the total amount of servers that the bot is in, along with the average and max member counts
        servers = self.bot.guilds

        memberCounts = []
        for server in servers:
            memberCounts.append(server.member_count)

        embed.add_field(name="Usage Information",
                        value=f"```\nServer Count:\n {len(servers)} Servers\n\nLargest Server:\n {max(memberCounts)} Members\nAverage Server Size:\n {int(sum(memberCounts)/len(memberCounts))} Members\nTotal Member Count:\n {sum(memberCounts)} Members\n```", inline=False)
        # Count the lines of code that the bot is running
        linesOfCode = count_code(rootdir=os.getcwd())

        embed.add_field(name="Lines Of Code",
                        value=f"```\nRunning {linesOfCode} Lines Of Code```", inline=False)

        # Display the uptime
        startTime = int(self.bot.start_time.timestamp())
        embed.add_field(
            name="Uptime", value=f"**»** Booted up <t:{startTime}:R> (<t:{startTime}:d>)", inline=False)

        await ctx.respond(content=None, embed=embed, ephemeral=bool(ctx.guild))


def setup(bot):
    bot.add_cog(Health(bot))
