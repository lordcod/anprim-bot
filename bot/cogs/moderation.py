import nextcord
from nextcord.ext import commands

import time
from typing import Optional
import re
from bot.misc.datas import rules, category_title
from bot.misc.anprim_bot import AnprimBot
from bot.views.view import IdeaBut

class Moderation(commands.Cog):
    def __init__(self, bot: AnprimBot) -> None:
        self.bot = bot
    
    
    @commands.command()
    async def button_suggest(self, ctx:commands.Context):
        await ctx.message.delete()
        await ctx.send('Предложи свою идею для проекта!',view=IdeaBut(self.bot))

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx:commands.Context):
        await self.bot.close()
    
    @commands.command("rules")
    async def command_rules(self, ctx: commands.Context, _rule: Optional[str] = None):
        if _rule is not None and (rule := re.fullmatch(r"([1-6]).(1?[0-9])", _rule)):
            title = category_title.get(rule.group(1))
            description = rules.get(rule.group(1)).get(rule.group(2))
            
            embed = nextcord.Embed(
                title=title,
                description=description,
                color=0xffba08
            )
            await ctx.send(embed=embed)
        elif _rule is not None and (category := re.fullmatch(r"([1-6])", _rule)):
            description = ""
            for num, rule in rules[category.group(1)].items():
                description += f"**{num}**. {rule}\n"
            
            embed = nextcord.Embed(
                title=category_title.get(category.group(1)),
                description=description,
                color=0xffba08
            )
            await ctx.send(embed=embed)
        else:
            embeds = []
            
            for category_id, _rules in rules.items():
                description = ""
                for num, rule in _rules.items():
                    description += f"**{num}**. {rule}\n"
                
                embeds.append(nextcord.Embed(title=category_title[category_id], description=description, color=0xffba08))
            
            await ctx.send(embeds=embeds)
    
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx: commands.Context, limit: int):
        if limit > 200:
            raise commands.CommandError("The maximum number of messages to delete is `100`")
        
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f'Deleted {len(deleted)} message(s)',delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self,ctx: commands.Context,member: nextcord.Member,limit: int):
        if limit > 100:
            raise commands.CommandError("The maximum number of messages to delete is `100`")
        
        messages = []
        
        minimum_time = int((time.time() - 14 * 24 * 60 * 60) * 1000.0 - 1420070400000) << 22
        
        async for message in ctx.channel.history(limit=250):
            if len(messages) >= limit:
                break
            if message.author == member:
                messages.append(message)
            
            if message.id < minimum_time:
                break
        
        await ctx.channel.delete_messages(messages)
        
        await ctx.send(f'Deleted {len(messages)} message(s)',delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def between(self,ctx: commands.Context, message_start:nextcord.Message, messsage_finish:nextcord.Message=None):
        if messsage_finish and message_start.channel != messsage_finish.channel:
            raise commands.CommandError("Channel error")
        
        messages = []
        finder = False
        minimum_time = int((time.time() - 14 * 24 * 60 * 60) * 1000.0 - 1420070400000) << 22
        
        async for message in message_start.channel.history(limit=100):
            if not messsage_finish:
                messsage_finish = message
            
            if message == messsage_finish:
                finder = True
            
            if finder:
                messages.append(message)
            
            if message == message_start or len(messages) >= 50 or message.id < minimum_time:
                break
        
        await ctx.channel.delete_messages(messages)
        
        await ctx.send(f'Deleted {len(messages)} message(s)', delete_after=5.0)


def setup(bot):
    cog = Moderation(bot)

    bot.add_cog(cog)