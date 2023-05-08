import discord
from discord.ext import commands
from views.done import DoneView

def cog_check(ctx):
    guild = ctx.bot.get_guild(1098191144686473216)
    if ctx.guild.id != guild.id:
        return False

class Portal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name='mass', description='Starts the massing process.')
    async def mass(self, ctx):
        await ctx.send('1. send ad in cb & non cb\n2. 2 ads per ticket; 1 ticket per user\n3. post from b2t\n4. send ss of post last category\n5. servers are filtered by themes, u can use `-access <stox|icon/decor|social|other|all>`\n\ntype `-start` once you have read this and is ready to begin massing.')
    
    @commands.hybrid_command(name='start', description='Executes the start checkpoint.')
    async def start(self, ctx):
        await ctx.send('1. make sure you have read the embed properly or your ticket will be __**closed**__!\n2. plz list any servers you may have skipped in a __**single**__ message as the bot will auto detect the skips and be sure to read the reqs of each channel.\n3. if there are no reqs listed in one of the channels it means the server has no reqs.\n\nyou can start now, type `-done` once done')

    @commands.hybrid_command(name='done', description='Executes the done checkpoint.')
    async def done(self, ctx):
        await ctx.send(f'{ctx.author.mention} select a post method', view=DoneView())
    
    @commands.Cog.listener('on_message')
    async def skip_listner(self, message):
        listings = ['skip', 'skips', 'skipped', 'skip', 'skippin', 'skipping', 'skippings', 'skippins']
        if message.author.id == self.bot.user.id:
            return
        if any([word in message.content.lower() for word in listings]):
            if len(message.content) < 10:
                return
            else:
                await message.pin()

    @commands.hybrid_command(name='access', description='Gives access to a servers.')
    async def access(self, ctx, access: str):
        stox = ctx.guild.get_role(1105116553122435112)
        icon = ctx.guild.get_role(1105116582730006578)
        social = ctx.guild.get_role(1105116620445192204)
        other = ctx.guild.get_role(1105150560795111446)
        if access.lower() == 'stox':
            await ctx.send('you have been given access to stox servers')
            await ctx.author.add_roles(stox)
        elif access.lower() == 'icon/decor':
            await ctx.send('you have been given access to icon/decor servers')
            await ctx.author.add_roles(icon)
        elif access.lower() == 'social':
            await ctx.send('you have been given access to social servers')
            await ctx.author.add_roles(social)
        elif access.lower() == 'other':
            await ctx.send('you have been given access to other servers')
            await ctx.author.add_roles(other)
        elif access.lower() == 'all':
            await ctx.send('you have been given access to all servers')
            await ctx.author.add_roles(stox, icon, social, other)
        else:
            await ctx.send('invalid access type')

async def setup(bot):
    await bot.add_cog(Portal(bot))
    