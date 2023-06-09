import discord
from views.urgent import UrgentView

class Done(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='batch', description='batching ads'),
            discord.SelectOption(label='sep-1h', description='seps ads for 1h'),
            discord.SelectOption(label='sep-2h', description='seps ads for 2h'),
            discord.SelectOption(label='sep-3h', description='seps ads for 3h'),
            discord.SelectOption(label='ovn', description='seps ads for overnight (only for byp)'),
        ]

        super().__init__(placeholder='choose a option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        dir = {'stox': 1105116553122435112, 'icon/decor': 1105116582730006578, 'social': 1105116620445192204, 'mnml': 1105463864012845166, 'other': 1105150560795111446}
        embed = discord.Embed(description='pick a urguency ! (u better do this part or ticket closeed `2/2`)', color=0x2F3136)
        await interaction.response.defer()
        if self.values[0] == 'ovn':
            if interaction.guild.get_role(1101821406838263848) in interaction.user.roles:
                await interaction.followup.send(f'{interaction.user.mention}', embed=embed, view=UrgentView(self.values[0]))
                for ids in dir.values():
                    role = interaction.guild.get_role(ids)
                    await interaction.user.remove_roles(role)
            else:
                await interaction.followup.send(f'{interaction.user.mention}', embed=discord.Embed(description='you dont have byp !!', color=0x2F3136))
        else:
            await interaction.followup.send(f'{interaction.user.mention}', embed=embed, view=UrgentView(self.values[0]))
            for ids in dir.values():
                role = interaction.guild.get_role(ids)
                await interaction.user.remove_roles(role)
        

class DoneView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Done())
