import nextcord


class ChoiseServerView(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Юниум', emoji='<a:purpletick:1113650352449929217>', style=nextcord.ButtonStyle.green, custom_id='server:union')
    async def on_server_union(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = interaction.guild.get_role(1251087876037283901)

        if role in interaction.user.roles:
            await interaction.response.send_message(f'Снята роль {role.mention}!', ephemeral=True)
            await interaction.user.remove_roles(role)
        else:
            await interaction.response.send_message(f'Выдана роль {role.mention}!', ephemeral=True)
            await interaction.user.add_roles(role)

    @nextcord.ui.button(label='Полфорт', emoji='<a:purpletick:1113650352449929217>', style=nextcord.ButtonStyle.blurple, custom_id='server:poltfort')
    async def on_server_poltfort(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = interaction.guild.get_role(1251087948292816916)

        if role in interaction.user.roles:
            await interaction.response.send_message(f'Снята роль {role.mention}!', ephemeral=True)
            await interaction.user.remove_roles(role)
        else:
            await interaction.response.send_message(f'Выдана роль {role.mention}!', ephemeral=True)
            await interaction.user.add_roles(role)
