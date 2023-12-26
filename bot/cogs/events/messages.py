import nextcord
from nextcord.ext import commands

from bot.misc.anprimbot import AnprimBot

class Messages(commands.Cog):
    bot: AnprimBot

    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        
        if message.channel.id == 1169329230195196014:
            await message.delete()


def setup(bot: AnprimBot):
    cog = Messages(bot)

    bot.add_cog(cog)