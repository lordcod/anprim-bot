import nextcord
from nextcord.ext import commands
import nextcord.state

from bot.misc.anprim_bot import AnprimBot


class Threads(commands.Cog):
    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot
        bot.add_event(self.on_thread_create)

    async def on_thread_create(self, thread: nextcord.Thread):
        if thread.parent_id != 1249393310456348695:
            pass

        role = thread.guild.get_role(1251081478700404846)
        await thread.owner.add_roles(role)


def setup(bot):
    cog = Threads(bot)
    bot.add_cog(cog)
