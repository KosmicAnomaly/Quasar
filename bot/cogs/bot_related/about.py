import logging
from contextlib import suppress
from os import getenv

from discord import (ApplicationContext, ButtonStyle, Embed, HTTPException,
                     Permissions)
from discord.commands import slash_command
from discord.ext.commands import BucketType, cooldown
from discord.ui import Button, View
from discord.utils import oauth_url
from tools.cog import Cog
from tools.colors import Colors

logger = logging.getLogger("quasar")


class About(Cog, name="About"):
    """A command about the bot"""

    @slash_command(name="about")
    @cooldown(1, 10, BucketType.user)
    async def about(self, ctx: ApplicationContext):
        """What's a Quasar?"""

        await ctx.defer(ephemeral=bool(ctx.guild))

        embed = Embed(color=Colors.neon_blue())

        embed.set_author(
            name=self.bot.user, icon_url=self.bot.user.avatar.url)

        appInfo = await self.bot.application_info()

        if appInfo.team:
            owner = appInfo.team.owner
        else:
            owner = appInfo.owner
        fetchedOwner = await self.bot.get_or_fetch_user(owner.id)
        if fetchedOwner:
            embed.set_footer(
                text=f"Developed with ♥ by {fetchedOwner}", icon_url=fetchedOwner.avatar.url)
        else:
            embed.set_footer(
                text=f"Developed with ♥ by {owner}")

        view = View()

        botInvite = oauth_url(client_id=self.bot.user.id, permissions=Permissions(
            permissions=3072), scopes=("bot", "applications.commands"))

        emoji = self.bot.get_emoji(939800328147181639)
        view.add_item(Button(style=ButtonStyle.link,
                      label="Invite Quasar", url=botInvite, emoji=emoji, row=0))

        channelID = getenv("SUPPORT_CHANNEL_ID") or None
        if channelID and channelID.isnumeric():
            channel = await self.bot.get_or_fetch_channel(int(channelID))
            if channel:
                invite = None
                with suppress(HTTPException):
                    invite = await channel.create_invite(unique=False, reason="Support server invite")
                if invite:
                    emoji = self.bot.get_emoji(939802043000971294)
                    view.add_item(Button(style=ButtonStyle.link,
                                         label="Support Server", url=invite.url, emoji=emoji, row=0))

        if appInfo.terms_of_service_url:
            view.add_item(Button(style=ButtonStyle.link,
                                 label="Terms of Service", url=appInfo.terms_of_service_url, emoji="📜", row=1))

        if appInfo.privacy_policy_url:
            view.add_item(Button(style=ButtonStyle.link,
                                 label="Privacy Policy", url=appInfo.privacy_policy_url, emoji="🕵️", row=1))

        await ctx.respond(embed=embed, view=view, ephemeral=bool(ctx.guild))


def setup(bot):
    bot.add_cog(About(bot))
