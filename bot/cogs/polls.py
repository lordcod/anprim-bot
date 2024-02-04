import nextcord
from nextcord.ext import commands

from bot.misc.anprim_bot import AnprimBot
from bot.views.view import CreatePoll
from bot.misc.utils import alphabet
from bot import db


def is_valid_poll_data(data: dict|None) -> bool:
    if not data:
        return False
    
    user_id = data.get('user_id')
    title = data.get('title')
    options = data.get('options')
    
    return user_id and title and options


class Polls(commands.Cog):
    bot: AnprimBot

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @nextcord.slash_command(name="test-poll", guild_ids=[1179069504186232852])
    async def poll(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(CreatePoll())

    @nextcord.message_command("Test Finish Poll", guild_ids=[1179069504186232852])
    async def finish_poll(self, interaction: nextcord.Interaction, message: nextcord.Message):
        await interaction.response.defer(ephemeral=True, with_message=False)

        poll_data: dict = db.get('polls', message.id)
        if not is_valid_poll_data(poll_data):
            return
        
        user_id = poll_data.get('user_id')
        title = poll_data.get('title')
        options = poll_data.get('options')
        
        if not interaction.user.id == user_id:
            await interaction.edit_original_message(content="Это не ваш опрос.\nУ вас нет прав завершить данное голование!")
            return
        
        general_count = sum([react.count for react in message.reactions])-len(message.reactions)
        
        text = ''
        for num, react in enumerate(message.reactions):
            count = react.count - 1
            percent = (0 if general_count==0 else count//general_count) * 100
            text = (
                f'{text}'
                f'{num+1}.`{options[num]}`({alphabet[num]}) - **{percent}%**\n'
            )
        
        embed = nextcord.Embed(
            title=title,
            description=text,
            color=0xffba08,
            timestamp=interaction.created_at
        )
        embed.set_footer(text="Голосование было завершено!")
        
        await message.edit(embed=embed)
        
        await interaction.edit_original_message(content="Голосование успешно завершено!")



def setup(bot):
    cog = Polls(bot)

    bot.add_cog(cog)