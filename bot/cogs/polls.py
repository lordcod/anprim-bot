import nextcord
from nextcord.ext import commands

from bot.views.view import CreatePoll
from bot import db

import os


class Polls(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
        
    @nextcord.slash_command(name="test-poll", guild_ids=[1179069504186232852])
    async def poll(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(CreatePoll())

    @nextcord.message_command("Test Finish Poll", guild_ids=[1179069504186232852])
    async def finish_poll(self, interaction: nextcord.Interaction, message: nextcord.Message):
        await interaction.response.send_message("Pong!", ephemeral=True, delete_after=0.05)
        
        if not message.author == self.bot.user:
            return 
        
        user_id = db.get('polls', message.id)
        
        if user_id and not interaction.user.id == user_id:
            await interaction.response.send_message('Это не ваш опрос',ephemeral=True)
            return
        general_count = sum([react.count for react in message.reactions])-len(message.reactions)
        
        choices = []
        for desc in message.embeds[0].description.split("\n"):
            choices.append(desc)
        text = ''
        for num, react in enumerate(message.reactions):
            count = react.count - 1
            percent = count//general_count * 100
            text = f'{text}{choices[num]} - **{percent}%**\n'
        await message.reply(text)



def setup(bot: commands.Bot):
    cog = Polls(bot)

    bot.add_cog(cog)