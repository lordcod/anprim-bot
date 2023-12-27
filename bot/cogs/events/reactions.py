import nextcord
from nextcord.ext import commands


class Reactions(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
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

def setup(bot: commands.Bot):
    cog = Reactions(bot)

    bot.add_cog(cog)