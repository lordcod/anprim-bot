import nextcord
from nextcord.ext import commands
import time

from bot.misc.utils import TableDict,alphabet
from bot.misc.env import (channel_suggest,channel_suggest_accept,accept_roles)
from bot import db

from bot.misc.anprim_bot import AnprimBot

timeout = TableDict(0)


class ConfirmModal(nextcord.ui.Modal):
    bot: AnprimBot
    
    def __init__(self, bot, interaction: nextcord.Interaction):
        super().__init__(
            "Предложить идею",
            timeout=5 * 60,  # 5 minutes
        )
        self.bot = bot
        self.interaction = interaction

        self.idea = nextcord.ui.TextInput(
            label="Аргумент:",
            required=False,
            style=nextcord.TextInputStyle.paragraph,
            min_length=0,
            max_length=1500,
        )
        self.add_item(self.idea)

    async def callback(self, inter: nextcord.Interaction) -> None:
        interaction = self.interaction
        name = interaction.user.nick or interaction.user.global_name or interaction.user.name
        val = self.idea.value
        
        embed = interaction.message.embeds[0]
        embed.color = nextcord.Color.green()
        embed.set_footer(text=f'Одобрено | {name}',icon_url=interaction.user.display_avatar)
        ping = interaction.message.content
        content = f'{ping} твоя идея одобрена!'
        
        views = Confirm(self.bot)
        views.confirm.disabled = True
        views.cancel.disabled = True
        
        await interaction.message.edit(content=content,embed=embed,view=views)
        
        
        channel = self.bot.get_channel(channel_suggest_accept)
        embed_accept = nextcord.Embed(
            title="Идея одобрена!",
            color=nextcord.Color.green()
        )
        embed_accept.add_field(name='Суть идеи:',value=embed.fields[0].value,inline=False)
        if val:
            embed_accept.add_field(name='Аргумент подтверждения:',value=val,inline=False)
        embed_accept.set_footer(text=name,icon_url=interaction.user.display_avatar)
        await channel.send(content=content,embed=embed_accept)

class Confirm(nextcord.ui.View):
    bot: AnprimBot
    
    def __init__(self, bot: AnprimBot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @nextcord.ui.button(label="Одобрить", style=nextcord.ButtonStyle.green,custom_id='persistent_view:confirm')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role_ids = [role.id for role in interaction.user.roles] 
        for ar in accept_roles:
            if ar in role_ids:
                break
        else:  
            return
        await interaction.response.send_modal(ConfirmModal(self.bot,interaction))
    
    @nextcord.ui.button(label="Отказать", style=nextcord.ButtonStyle.red,custom_id='persistent_view:cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role_ids = [role.id for role in interaction.user.roles] 
        for ar in accept_roles:
            if ar in role_ids:
                break
        else:  
            return
        name = interaction.user.nick or interaction.user.global_name or interaction.user.name
        embed = interaction.message.embeds[0]
        embed.color = nextcord.Color.red()
        embed.set_footer(text=f'Отказано | {name}',icon_url=interaction.user.display_avatar)
        
        ping = interaction.message.content
        content = f'{ping} твоей идеи отказано!'
        
        self.confirm.disabled = True
        self.cancel.disabled = True
        
        await interaction.message.edit(content=content,embed=embed,view=self)


class IdeaModal(nextcord.ui.Modal):
    bot: AnprimBot
    
    def __init__(self,bot: AnprimBot):
        super().__init__(
            "Предложить идею",
            timeout=5 * 60,  # 5 minutes
        )
        self.bot = bot

        self.idea = nextcord.ui.TextInput(
            label="Расскажи нам о своей идее",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Опиши свою идею как можно более подробно с примерами использования.",
            min_length=10,
            max_length=1800,
        )
        self.add_item(self.idea)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        channel = self.bot.get_channel(channel_suggest)
        name = interaction.user.nick or interaction.user.global_name or interaction.user.name
        idea = self.idea.value
        
        embed = nextcord.Embed(
            title='Новая идея!',
            description='Будет идея или нет, зависит от вас!',
            color=0xffba08
        )
        embed.set_author(
            name=name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name='Идея:',value=idea)
        
        mes = await channel.send(content=interaction.user.mention,embed=embed,view=Confirm(self.bot))
        await mes.add_reaction("<a:tickmark:1170029771040759969>")
        await mes.add_reaction("<a:cross:1170029921314279544>")
        await mes.create_thread(name=f"Обсуждение идеи от {name}")
        
        timeout[interaction.user.id] = time.time()+1800

class IdeaBut(nextcord.ui.View):
    bot: AnprimBot
    
    def __init__(self,bot: AnprimBot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Предложить идею",
        style=nextcord.ButtonStyle.green,
        custom_id="persistent_view:sug"
    )
    async def suggest(
        self,
        button: nextcord.ui.Button,
        interaction: nextcord.Interaction
    ) -> None:
        if timeout[interaction.user.id] > time.time():
            await interaction.response.send_message(content=(
                    "Предложить идею можно только раз в 30 минут\n"
                    f"Следующия возможность подать идею будет через: <t:{timeout[interaction.user.id]:.0f}:R>"
                ),
                ephemeral=True
            )
            return
        await interaction.response.send_modal(modal=IdeaModal(self.bot))


class CreatePoll(nextcord.ui.Modal):
    def __init__(self) -> None:
        super().__init__("Create pool", timeout=300)
        
        self.question = nextcord.ui.TextInput(
            label='Question',
            placeholder='Write a question',
            max_length=100
        )
        self.choices = nextcord.ui.TextInput(
            label='Choices',
            placeholder='Write the options of choice through the line each',
            style=nextcord.TextInputStyle.paragraph
        )
        self.description = nextcord.ui.TextInput(
            label='Description',
            style=nextcord.TextInputStyle.paragraph,
            required=False
        )
        
        self.add_item(self.question)
        self.add_item(self.choices)
        self.add_item(self.description)
    
    
    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True, with_message=False)
        
        question = self.question.value
        choices = self.choices.value
        sketch = self.description.value
        
        description = ""
        
        if 1 >= len(choices.split('\n')):
            await interaction.followup.send(content="Должно быть больше 1 варианта выбора\nЧтобы указать еще варианты перенесите строку", ephemeral=True, delete_after=5.0)
            return
        
        for num, choice in enumerate(choices.split('\n')[:len(alphabet)]):
            description = (
                f'{description}'
                f'{num+1}.`{choice}`({alphabet[num]})\n'
            )
        
        
        embed = nextcord.Embed(
            title=question,
            description=description,
            color=0xffba08
        )
        if sketch:
            embed.add_field(name='Описание',value=sketch)
        
        message = await interaction.channel.send(embed=embed)
        
        for serial, _ in enumerate(choices.split('\n')[:len(alphabet)]):
            await message.add_reaction(alphabet[serial])
        
        nurtured_data = {
            'title':question,
            'sketch':sketch,
            'user_id':interaction.user.id,
            'options':choices.split('\n')[:len(alphabet)],
        } 
        db.set('polls', message.id, nurtured_data)


