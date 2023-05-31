from discord.ext import commands
import discord

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

    @commands.hybrid_command(name='ban', description='Ban a user')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(description=f'{member.mention} has been banned', color=0x2F3136)
        await member.ban(reason=reason)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='kick', description='Kick a user')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(description=f'{member.mention} has been kicked', color=0x2F3136)
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

