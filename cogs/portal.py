import discord
from discord.ext import commands
from views.done import DoneView
import re

async def setup(bot):
    await bot.add_cog(Portal(bot))

class Portal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild.id == 1098191144686473216:
            return True

    @commands.hybrid_command(name='mass', description='Starts the massing process.')
    async def mass(self, ctx):
        embed = discord.Embed(description='1. make sure you have read the embed properly or your ticket will be __**closed**__!\n\n2. send ad in cb and non cb\n\n3. plz list any servers you may have skipped in a __**single**__ message as the bot will auto detect the skips and be sure to read the reqs of each channel.\n\n4. if there are no reqs listed in one of the channels it means the server has no reqs\n\n5. servers are filtered by themes, you can use `-access <stox|icon/decor|social|mnml|other|all>`\n\nyou can start now, type `-done` once done', color=0x2F3136)
        embed.set_image(url='https://cdn.korino.dev/r/HsvKWy.png?compress=false')
        await ctx.send(embed=embed)
    
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
        if message.author.bot:
            return
        if message.channel.topic != str(message.author.id):
            return
        if message.guild.id != 1098191144686473216:
            return
        if any([word in message.content.lower() for word in listings]):
            if len(message.content) < 10:
                return
            else:
                await message.pin()

    @commands.Cog.listener('on_message_edit')
    async def skip_listner_edit(self, before, after):
        listings = ['skip', 'skips', 'skipped', 'skip', 'skippin', 'skipping', 'skippings', 'skippins']
        if before.author.id == self.bot.user.id:
            return
        if before.author.bot:
            return
        if before.channel.topic != str(before.author.id):
            return
        if before.guild.id != 1098191144686473216:
            return
        if any([word in after.content.lower() for word in listings]):
            if len(after.content) < 10:
                return
            else:
                await after.pin()

    @commands.Cog.listener('on_message')
    async def ad_listener(self, message):
        if message.author.id == self.bot.user.id:
            return
        if message.author.bot:
            return
        if message.channel.topic != str(message.author.id):
            return
        if message.guild.id != 1098191144686473216:
            return
        if not message.content.startswith('```') and not message.content.endswith('```'):
            return
        match = re.findall(r'(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?', message.content)
        if match:
            await message.pin()

    @commands.Cog.listener('on_message_edit')
    async def ad_listener_edit(self, before, after):
        if before.author.id == self.bot.user.id:
            return
        if before.author.bot:
            return
        if before.channel.topic != str(before.author.id):
            return
        if before.guild.id != 1098191144686473216:
            return
        if not after.content.startswith('```') and not after.content.endswith('```'):
            return
        match = re.findall(r'(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?', after.content)
        if match:
            await after.pin()

        
    @commands.hybrid_command(name='access', description='Gives access to a servers.')
    async def access(self, ctx, access: str):

        dir = {'stox': 1105116553122435112, 'icon/decor': 1105116582730006578, 'social': 1105116620445192204, 'mnml': 1105463864012845166, 'other': 1105150560795111446}
        if access.lower() == 'all':
            for ids in dir.values():
                role = ctx.guild.get_role(ids)
                await ctx.author.add_roles(role)
            await ctx.send('you have been given access to all servers')
        elif access not in dir:
            await ctx.send('invalid access type')
        else:
            role = ctx.guild.get_role(dir[access.lower()])
            await ctx.author.add_roles(role)
            await ctx.send(f'you have been given access to {access.lower()} servers')
        
    @commands.Cog.listener('on_message')
    async def ad_divider(self, message):
        embed = discord.Embed()
        embed.set_image(url='https://64.media.tumblr.com/3eeb3876b5e82cde2e742d917965cda9/aeec771f2613a911-b6/s2048x3072/35d14bb1b40d524d14d64d8b81da47597952fb64.pnj')
        if message.author.id == self.bot.user.id:
            return
        if message.author.bot:
            return
        if message.channel.id != 1098228193456038008:
            return
        match = re.findall(r'(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?', message.content)
        if match:
            await message.channel.send(embed=embed, color=0x2F3136)