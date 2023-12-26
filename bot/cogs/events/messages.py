import nextcord
from nextcord.ext import commands

class Messages(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        
        if message.channel.id == 1169329230195196014:
            await message.delete()


def setup(bot: commands.Bot):
    cog = Messages(bot)

    bot.add_cog(cog)