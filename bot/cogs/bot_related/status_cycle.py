import logging

from discord.ext.tasks import loop
from tools.cog import Cog
from tools.statuses import Statuses

logger = logging.getLogger("quasar")


class StatusCycle(Cog, name="Status Cycle"):
    """Automatically cycles through Quasar's statuses"""

    def __init__(self, bot):
        super().__init__(bot)
        self.statuses = Statuses()
        if len(self.statuses.activities):
            self.status_cycle.start()
        else:
            logger.warning("No random statuses available")

    # randomly change Quasar's status every 5 minutes
    @loop(minutes=5)
    async def status_cycle(self):

        thisStatus = self.statuses.next_status()

        try:
            await self.bot.change_presence(activity=thisStatus)
        except:
            logger.warning(
                f"Failed to update status to [{thisStatus.type} | '{thisStatus.name}']")

    @status_cycle.before_loop
    async def before_status_cycle(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(StatusCycle(bot))
