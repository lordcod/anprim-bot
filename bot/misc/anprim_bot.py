import nextcord
from nextcord.ext import commands

class AnprimBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='a.', intents=nextcord.Intents.all())
    
    def add_event(self, coro):
        self.event(coro)
