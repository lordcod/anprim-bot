import nextcord
from nextcord.ext import commands,application_checks
from bot.views.view import (Confirm,IdeaBut,CreatePoll)
from bot.misc.env import token
from bot import db

loc = False

bot = commands.Bot(command_prefix='a.',intents=nextcord.Intents.all())



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

@bot.command()
async def button_suggest(ctx:commands.Context):
    await ctx.message.delete()
    await ctx.send('Предложи свою идею для проекта!',view=IdeaBut(bot))

@bot.slash_command()
async def poll(interaction: nextcord.Interaction):
    await interaction.response.send_modal(CreatePoll())

@bot.message_command("Finish Poll")
async def finish_poll(interaction: nextcord.Interaction, message: nextcord.Message):
    if not message.author == bot.user:
        return 
        
    user_id = db.get(message.id)
    if not interaction.user.id == user_id:
        await interaction.response.send_message('Это не ваш опрос',ephemeral=True)
        return
    general_count = sum([react.count for react in message.reactions])-len(message.reactions)
    
    choices = []
    for desc in message.embeds[0].description.split("\n"):
        choices.append(desc)
    integer = 0
    text = ''
    for react in message.reactions:
        count = react.count - 1
        percent = int((count/general_count)*100)
        text = f'{text}{choices[integer]} - **{percent}%**\n'
        integer += 1
    await message.reply(text)
    await interaction.response.defer(ephemeral=True)

@bot.event
async def on_reaction_add(reaction: nextcord.Reaction, user: nextcord.User):
    if user.bot:
        return
    if not reaction.message.author.bot:
        return
    for react in reaction.message.reactions:
        if react == reaction:
            continue
        async for umem in react.users():
            if umem == user:
                await react.remove(user)


@bot.command()
@commands.is_owner()
async def shutdown(ctx:commands.Context):
    await bot.close()


def start_bot():
    bot.run(token)

if __name__ == "__main__":
    start_bot()