import nextcord
from nextcord.ext import commands

from bot.misc.anprim_bot import AnprimBot
from bot.views.view import Confirm, IdeaBut


class Errors(commands.Cog):
    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot

        bot.add_event(self.on_error)

    async def on_error(self):
        self.bot.add_view(Confirm(self.bot))
        self.bot.add_view(IdeaBut(self.bot))
        print(f"The bot is registered as {self.bot.user}")


def setup(bot):
    cog = Errors(bot)

    bot.add_cog(cog)
