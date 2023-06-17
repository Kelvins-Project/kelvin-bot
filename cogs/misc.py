from discord.ext import commands
import discord
from discord import app_commands

async def setup(bot):
    await bot.add_cog(Misc(bot))
    
class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name='info', description='Get the bot\'s info')
    async def info(self, ctx):
        embed = discord.Embed(description=f'bot sees {ctx.guild.member_count} users', color=0x2F3136)
        embed.set_footer(text=f'ping {round(self.bot.latency * 1000)}ms')
        await ctx.send(embed=embed)

