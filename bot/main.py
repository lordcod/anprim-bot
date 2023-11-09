import nextcord
from nextcord.ext import commands
from bot.views.view import (Confirm,IdeaBut)
from bot.misc.env import token


bot = commands.Bot(command_prefix='a.',intents=nextcord.Intents.all(),default_guild_ids=[1160838343421075476])



@bot.event
async def on_ready():
    bot.add_view(Confirm(bot))
    bot.add_view(IdeaBut(bot))
    print(f"The bot is registered as {bot.user}")


@bot.command()
# @commands.has_any_role(1169257391058079814,1163742629289271316)
async def button_suggest(ctx:commands.Context):
    await ctx.message.delete()
    await ctx.send('Предложи свою идею для проекта!',view=IdeaBut(bot))

@bot.command()
@commands.is_owner()
async def shutdown(ctx:commands.Context):
    await bot.close()


def start_bot():
    bot.run(token)

if __name__ == "__main__":
    start_bot()