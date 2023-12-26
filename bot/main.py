import nextcord
from nextcord.ext import commands
from bot.views.view import (Confirm,IdeaBut)
from bot.misc.env import token

import os
from time import time as tick
from datetime import datetime

week = 60 * 60 * 24 * 7

bot = commands.Bot(
    command_prefix='a.',
    intents=nextcord.Intents.all()
)



@bot.event
async def on_ready():
    bot.add_view(Confirm(bot))
    bot.add_view(IdeaBut(bot))
    print(f"The bot is registered as {bot.user}")
@bot.command()
async def infractions(ctx: commands.Context):
    users_data = {}
    
    current_time = int(tick())
    week_ago = current_time-week
    
    dt_current_time = datetime.fromtimestamp(current_time)
    dt_week_ago = datetime.fromtimestamp(week_ago)
    
    async for message in ctx.channel.history(limit=250, after=dt_week_ago, before=dt_current_time):
        if message.author.id not in users_data:
            users_data[message.author.id] = []
        
        users_data[message.author.id].append(message)
    
    sorted(users_data.items(), key=lambda item: len(item[1]), reverse=True)
    
    total_results = 0
    description = ""
    for user_id, messages in users_data.items():
        total_results += len(messages)
        
        user = ctx.guild.get_member(user_id)
        description = (
            f"{description}"
            f"**{user.display_name}** - {len(messages)}\n"
        )
    
    embed = nextcord.Embed(
        title="Reports for week",
        description=description,
        color=0xffba08,
    )
    embed.set_footer(text=f"Total results: {total_results}")
    await ctx.send(embed=embed)

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
