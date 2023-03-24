import discord
from discord.ext import commands, tasks
from discord import app_commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.produce_drugs.start()

    async def meth_dealer(self):
        return await self.bot.db.fetchval('SELECT meth_amount FROM drug_stock')

    @app_commands.command(name='ping', description='Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    @app_commands.command(name='meth', description='Meth in stock.')
    async def meth(self, interaction: discord.Interaction):
        amount = f'{await self.meth_dealer()} oz'
        await interaction.response.send_message(f'Meth in stock: {amount if not await self.meth_dealer() == None or 0 else "SOLD OUT"}')

    @tasks.loop(seconds=60)
    async def produce_drugs(self):
        current_amount = await self.bot.db.fetchval('SELECT meth_amount FROM drug_stock')
        await self.bot.db.execute('INSERT INTO drug_stock (meth_amount) VALUES ($1)', current_amount + 2)
    
async def setup(bot):
    await bot.add_cog(Commands(bot))
    