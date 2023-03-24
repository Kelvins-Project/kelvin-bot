import discord
from discord.ext import commands, tasks
from discord import app_commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.produce_meth.start()

    @app_commands.command(name='ping', description='Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    @app_commands.command(name='meth', description='Meth in stock.')
    async def meth(self, interaction: discord.Interaction):
        amount = f'{self.bot.produce} oz'
        await interaction.response.send_message(f'Meth in stock: {amount if not self.bot.produce == 0 else "SOLD OUT"}')
    
    @app_commands.command(name='buy', description='Meth in stock.')
    async def buy(self, interaction: discord.Interaction, oz: int):
        if self.bot.produce == 0:
            return await interaction.response.send_message(f'We outtie cuh.')
        if self.bot.produce < oz:
            return await interaction.response.send_message(f'You tryna cop more than we got cuh hop off my dick.')
        amount = self.bot.produce - oz
        await interaction.response.send_message(f'Aii, you got ur shit, now get outta here. Meth in stock: {amount if not amount == 0 else "SOLD OUT"}')

    @tasks.loop(seconds=10)
    async def produce_meth(self):
        self.bot.produce += 2
    
async def setup(bot):
    await bot.add_cog(Commands(bot))
    