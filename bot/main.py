import nextcord
from nextcord.ext import commands
from bot.views.view import (Confirm,IdeaBut)
from bot.misc.anprimbot import AnprimBot
from bot.misc.env import token
import os



bot = AnprimBot(
    command_prefix='a.',
    intents=nextcord.Intents.all()
)


@bot.event
async def on_ready():
    bot.add_view(Confirm(bot))
    bot.add_view(IdeaBut(bot))
    print(f"The bot is registered as {bot.user}")

@bot.event
async def on_message(message: nextcord.Message):
    if message.author.bot:
        return
    
    if message.channel.id == 1169329230195196014:
        await message.delete()
    
    await bot.process_commands(message)



def load_dir(dirpath: str) -> None:
    for filename in os.listdir(dirpath):
        if os.path.isfile(f'{dirpath}/{filename}') and filename.endswith(".py") and not filename.startswith("__"):
            fmp = filename[:-3]
            supdirpath = dirpath[2:].split("/")
            findirpatch = '.'.join(supdirpath)
            
            bot.load_extension(f"{findirpatch}.{fmp}")
        elif os.path.isdir(f'{dirpath}/{filename}'):
            load_dir(f'{dirpath}/{filename}')

def start_bot():
    load_dir("./bot/cogs")
    
    bot.run(token)
