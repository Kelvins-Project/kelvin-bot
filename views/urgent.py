import discord
from discord.ext import commands

class Urgent(discord.ui.Select):
    def __init__(self):
        self.timeout = 6000

    
        options = [
            discord.SelectOption(label='nurg', description='not urgent'),
            discord.SelectOption(label='surg', description='kind of urgent'),
            discord.SelectOption(label='urg', description='very urgent'),
        ]

        super().__init__(placeholder='choose a option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction):
        await interaction.message.delete()
        channel_name = interaction.channel.name
        pin = await interaction.channel.send(f'you have selected **{self.values[0]}**')
        await pin.pin()
        await interaction.channel.edit(name=f'{channel_name}-{self.values[0]}')


class UrgentView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Urgent())