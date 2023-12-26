import nextcord
from nextcord.ext import commands

from bot.misc.anprimbot import AnprimBot

class Reactions(commands.Cog):
    bot: AnprimBot

    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: nextcord.Reaction, user: nextcord.User):
        if user.bot:
            return
        if not reaction.message.author.bot:
            return
        for react in reaction.message.reactions:
            if react == reaction:
                continue
            async for member in react.users():
                if member == user:
                    await react.remove(user)

def setup(bot: AnprimBot):
    cog = Reactions(bot)

    bot.add_cog(cog)