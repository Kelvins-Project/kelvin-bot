from discord.ext import commands
import discord

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='ping', description='Get the bot\'s latency')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
    
    @commands.hybrid_command(name='mc', description='Get the member count of the server')
    async def member_count(self, ctx):
        await ctx.send(f'There are {ctx.guild.member_count} members in this server')

    
        
async def setup(bot):
    await bot.add_cog(Misc(bot))