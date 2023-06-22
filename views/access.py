import discord

class AccessView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.dir = {'stox': 1105116553122435112, 'icon/decor': 1105116582730006578, 'social': 1105116620445192204, 'mnml': 1105463864012845166, 'other': 1105150560795111446}

    @discord.ui.button(label='stox', style=discord.ButtonStyle.green, custom_id='persistent_view:stox')
    async def stox(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.dir['stox'])
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'you have been given access to stox servers')
    
    @discord.ui.button(label='icon/decor', style=discord.ButtonStyle.green, custom_id='persistent_view:icon_decor')
    async def icon_decor(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.dir['icon/decor'])
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'you have been given access to icon/decor servers')

    @discord.ui.button(label='social', style=discord.ButtonStyle.green, custom_id='persistent_view:social')
    async def social(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.dir['social'])
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'you have been given access to social servers')

    @discord.ui.button(label='other', style=discord.ButtonStyle.green, custom_id='persistent_view:other')
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.dir['other'])
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'you have been given access to other servers')

    @discord.ui.button(label='mnml', style=discord.ButtonStyle.green, custom_id='persistent_view:mnml')
    async def mnml(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.dir['mnml'])
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'you have been given access to mnml servers')

    @discord.ui.button(label='all', style=discord.ButtonStyle.green, custom_id='persistent_view:all')
    async def all(self, interaction: discord.Interaction, button: discord.ui.Button):
        for ids in self.dir.values():
                role = interaction.guild.get_role(ids)
                await interaction.user.add_roles(role)
        await interaction.response.send_message(f'you have been given access to all servers')
