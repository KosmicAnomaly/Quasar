import logging
from datetime import timedelta
from math import ceil as round_up

from discord import (ApplicationCommandError, ApplicationContext,
                     DiscordServerError, Embed, Forbidden, HTTPException,
                     NotFound)
from discord.commands import CheckFailure
from discord.ext.commands import (BotMissingPermissions, CommandOnCooldown,
                                  MissingPermissions, NoPrivateMessage,
                                  PrivateMessageOnly)
from discord.utils import utcnow
from tools.cog import Cog
from tools.colors import Colors

logger = logging.getLogger("quasar")


class ErrorHandler(Cog, name="Error Handler"):
    """Handles command errors"""

    @Cog.listener()
    async def on_application_command_error(self, ctx: ApplicationContext, error: ApplicationCommandError):
        """Handles slash command errors"""

        commandName = ctx.command.qualified_name

        error = getattr(error, "original", error)

        embed = Embed(color=Colors.black())
        embed.set_author(name=f"/{commandName}")

        if isinstance(error, CheckFailure):
            embed.description = "You are not allowed to use this command!"

        elif isinstance(error, Forbidden):
            embed.description = "Discord unexpectedly prevented me from running that command!"

        elif isinstance(error, NotFound):
            embed.description = "Something I need has been lost to the infinite depths of space"

        elif isinstance(error, DiscordServerError):
            embed.description = "An error on Discord's end prevented me from running that command!"

        elif isinstance(error, HTTPException):
            logger.warning(
                f"HTTPException {error.status} - Code: {error.code} | Message: {error.text} | Response: {error.response} | Command: /{commandName}")
            return

        elif isinstance(error, NoPrivateMessage):
            embed.description = f"You can only use this command in Discord servers, not DMs"

        elif isinstance(error, PrivateMessageOnly):
            embed.description = f"You can only use this command in DMs, not Discord servers"

        elif isinstance(error, BotMissingPermissions):
            missingPerms = [perm.replace("_", " ").replace(
                "guild", "server").replace("moderate", "timeout").title() for perm in error.missing_permissions]

            missing = "**" + "**, **".join(missingPerms) + "**"

            embed.add_field(name="I'm Missing These Permissions:",
                            value=missing, inline=False)

        elif isinstance(error, MissingPermissions):
            missingPerms = [perm.replace("_", " ").replace("guild", "server").replace("moderate", "timeout").title()
                            for perm in error.missing_permissions]

            missing = "**" + "**, **".join(missingPerms) + "**"

            embed.add_field(name="You're Missing These Permissions:",
                            value=missing, inline=False)

        elif isinstance(error, CommandOnCooldown):
            cooldown = round_up(error.retry_after)
            laterDT = utcnow()+timedelta(seconds=cooldown)
            if error.retry_after < 60:
                timeFormat = f"in {round_up(cooldown)} seconds"
            elif error.retry_after < 86400:
                timeFormat = f"at <t:{int(laterDT.timestamp())}:t>"
            else:
                timeFormat = f"<t:{int(laterDT.timestamp())}:F>"

            embed.description = f"This command is on cooldown! You can use it again {timeFormat}"

        else:
            # if unhandled, log the error and apologize
            embed.description = "Something unexpected happened while trying to run this command, sorry!"

            logger.error(
                f"Uncaught {type(error)} exception running /{commandName}:\n  {error}")

        if ctx.interaction.response.is_done():
            await ctx.edit(content=None, embed=embed, view=None)
        else:
            await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
