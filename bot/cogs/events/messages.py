import nextcord
from nextcord.ext import commands

from bot.misc.anprim_bot import AnprimBot


class Messages(commands.Cog):
    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot
        self.bot.add_event(self.on_message)

    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return

        if message.channel.id == 1169329230195196014:
            await message.delete()

        await self.bot.process_commands(message)


def setup(bot):
    cog = Messages(bot)

    bot.add_cog(cog)
