import nextcord
from nextcord.ext import commands
import asyncio
from bot.misc.anprim_bot import AnprimBot
from bot.views.view import Confirm, IdeaBut
from bot.views.choiser import ChoiseServerView


class Ready(commands.Cog):
    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot

        bot.add_event(self.on_ready)

    async def on_ready(self):
        self.bot.add_view(Confirm(self.bot))
        self.bot.add_view(ChoiseServerView())
        self.bot.add_view(IdeaBut(self.bot))
        print(f"The bot is registered as {self.bot.user}")


def setup(bot):
    cog = Ready(bot)

    bot.add_cog(cog)
