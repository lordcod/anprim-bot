import nextcord
from nextcord.ext import commands,application_checks
from bot.views.view import (Confirm,IdeaBut,CreatePoll)
from bot.misc.env import token
from bot import db
import os

bot = commands.Bot(
    command_prefix='a.',
    intents=nextcord.Intents.all(),
    default_guild_ids=[1179069504186232852]
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

@bot.command()
async def button_suggest(ctx:commands.Context):
    await ctx.message.delete()
    await ctx.send('Предложи свою идею для проекта!',view=IdeaBut(bot))

@bot.slash_command()
async def poll(interaction: nextcord.Interaction):
    await interaction.response.send_modal(CreatePoll())

@bot.message_command("Finish Poll")
async def finish_poll(interaction: nextcord.Interaction, message: nextcord.Message):
    await interaction.response.pong()

    if not message.author == bot.user:
        return 
        
    user_id = db.get(message.id)
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


@bot.command()
@commands.is_owner()
async def shutdown(ctx:commands.Context):
    await bot.close()


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

if __name__ == "__main__":
    start_bot()