import nextcord
from nextcord.ext import commands

class AnprimBot(commands.Bot):
    message_history: list = []