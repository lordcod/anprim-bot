import nextcord
from nextcord.ext import commands

from bot.misc.anprim_bot import AnprimBot


class Reactions(commands.Cog):
    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: nextcord.Reaction, user: nextcord.User):
        if user.bot or not reaction.message.author.bot:
            return

        for react in reaction.message.reactions:
            if react == reaction:
                continue

            react_users = await react.users().flatten()
            if user in react_users:
                await reaction.remove(user)


def setup(bot):
    cog = Reactions(bot)

    bot.add_cog(cog)
