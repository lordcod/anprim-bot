import nextcord
from nextcord.ext import commands

import asyncio
import logging

from typing import TypeVar, Callable, Coroutine, Any

_log = logging.getLogger(__name__)

Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])


class AnprimBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='a.', intents=nextcord.Intents.all())
    
    def add_event(self, coro: Coro) -> Coro:
        """
        It works according to the `event` principle
        
        Exemple
        -------
        ```
        def __init__(self, bot: AnprimBot):
            self.bot = bot
            bot.add_event(self.on_ready)
        
        async def on_ready(self):
            print(f"The bot is registered as {self.bot.user}")
        ```
        
        Parametrs
        ---------
        coro: Coro - corontine function
        
        Raises
        ------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("event registered must be a coroutine function")

        setattr(self, coro.__name__, coro)
        _log.debug("%s has successfully been registered as an event", coro.__name__)
        return coro
