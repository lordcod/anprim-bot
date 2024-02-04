import nextcord
from nextcord.ext import commands

from bot.misc.anprim_bot import AnprimBot

class Basic(commands.Cog):
    bot: AnprimBot

    def __init__(self, bot) -> None:
        self.bot = bot
    


def setup(bot):
    cog = Basic(bot)

    bot.add_cog(cog)