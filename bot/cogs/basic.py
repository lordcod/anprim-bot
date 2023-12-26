import nextcord
from nextcord.ext import commands

from bot.misc.anprimbot import AnprimBot

class Basic(commands.Cog):
    bot: AnprimBot

    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot
    


def setup(bot: AnprimBot):
    cog = Basic(bot)

    bot.add_cog(cog)