import nextcord
from nextcord.ext import commands


class Basic(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


def setup(bot: commands.Bot):
    cog = Basic(bot)

    bot.add_cog(cog)