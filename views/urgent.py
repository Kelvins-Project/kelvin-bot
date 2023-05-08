import discord
from discord.ext import commands

class Urgent(discord.ui.Select):
    def __init__(self):

    
        options = [
            discord.SelectOption(label='non-urgent', description='not urgent'),
            discord.SelectOption(label='semi-urgent', description='kind of urgent'),
            discord.SelectOption(label='urgent', description='very urgent'),
        ]

        super().__init__(placeholder='choose a option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        pin = await interaction.channel.send(f'you have selected **{self.values[0]}**')
        await pin.pin()


class UrgentView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Urgent())