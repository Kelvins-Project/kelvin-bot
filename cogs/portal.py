from discord.ext import commands
from views.done import DoneView
class Portal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='mass', description='Starts the massing process.')
    async def mass(self, ctx):
        await ctx.send('1. send ad in cb & non cb\n2. 2 ads per ticket; 1 ticket per user\n3. post from b2t\n4. send ss of post last category\n\ntype `-start` once you have read this and are ready to begin massing.')
    
    @commands.hybrid_command(name='start', description='Executes the start checkpoint.')
    async def start(self, ctx):
        await ctx.send('1. make sure you have read the embed properly or your ticket will be __**closed**__!\n2. plz list any servers you may have skipped and be sure to read the reqs of each channel\n3. if there are no reqs listed in one of the channels it means the server has no reqs.\n\nyou can start now. type `-done` once done')

    @commands.hybrid_command(name='done', description='Executes the done checkpoint.')
    async def done(self, ctx):
        await ctx.send(f'{ctx.author.mention} select a post method', view=DoneView())

async def setup(bot):
    await bot.add_cog(Portal(bot))
    