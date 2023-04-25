from discord.ext import commands
import discord

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class Greedy(commands.Converter):
        async def convert(self, ctx, *links):
            return list(links)
        
    @commands.hybrid_command(name='info', description='Get the bot\'s info')
    async def info(self, ctx):
        embed = discord.Embed(description=f'bot sees {ctx.guild.member_count} users', color=0x2F3136)
        embed.set_footer(text=f'ping {round(self.bot.latency * 1000)}ms')
        await ctx.send(embed=embed)


            

        
async def setup(bot):
    await bot.add_cog(Misc(bot))