import discord
from views.urgent import UrgentView

class Done(discord.ui.Select):
    def __init__(self):

    
        options = [
            discord.SelectOption(label='batch', description='batching ads'),
            discord.SelectOption(label='sep-1h', description='seps ads for 1h'),
            discord.SelectOption(label='sep-2h', description='seps ads for 2h'),
            discord.SelectOption(label='sep-3h', description='seps ads for 3h'),
        ]

        super().__init__(placeholder='choose a option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(f'you have selected **{self.values[0]}**')
        await interaction.channel.send(f'{interaction.user.mention} select a urgentness', view=UrgentView(self.values[0]))

class DoneView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Done())