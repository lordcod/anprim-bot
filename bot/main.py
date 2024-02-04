import nextcord
from nextcord.ext import commands
from bot.misc.env import token
from bot.misc.anprim_bot import AnprimBot

import os
import time
from datetime import datetime

week = 60 * 60 * 24 * 7

bot = AnprimBot()

def load_dir(dirpath: str) -> None:
    for filename in os.listdir(dirpath):
        if os.path.isfile(f'{dirpath}/{filename}') and filename.endswith(".py"):
            fmp = filename[:-3]
            supdirpath = dirpath[2:].split("/")
            findirpatch = '.'.join(supdirpath)
            
            bot.load_extension(f"{findirpatch}.{fmp}")
        elif os.path.isdir(f'{dirpath}/{filename}'):
            load_dir(f'{dirpath}/{filename}')

def start_bot():
    # load_dir("./bot/cogs")
    
    bot.run(token)
