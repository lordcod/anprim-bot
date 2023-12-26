import nextcord
from nextcord.ext import commands

from bot.misc.anprimbot import AnprimBot
from bot.views.view import IdeaBut

class Moderation(commands.Cog):
    bot: AnprimBot

    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot
    
    
    @commands.command()
    async def button_suggest(self, ctx:commands.Context):
        await ctx.message.delete()
        await ctx.send('Предложи свою идею для проекта!',view=IdeaBut(self.bot))

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx:commands.Context):
        await self.bot.close()
    
    @commands.command()
    async def infractions(self, ctx: commands.Context):
        pass
    
    



def setup(bot: AnprimBot):
    cog = Moderation(bot)

    bot.add_cog(cog)