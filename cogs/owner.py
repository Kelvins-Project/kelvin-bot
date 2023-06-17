import discord
from discord.ext import commands
from views.create import CreateView
import traceback
import re
import asyncio

async def setup(bot):
    await bot.add_cog(Owner(bot))
      
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def reload(self, ctx):
        paginator = commands.Paginator(prefix='', suffix='')
        for extension in list(self.bot.extensions.keys()):
            try:
                await self.bot.reload_extension(extension)
                paginator.add_line(f"> Succesfully reloaded: ``{extension}``")
            except Exception as e:
                er = getattr(e, 'original', e)
                paginator.add_line(f'\U0001f6ab Failed to load extension: ``{extension}``')
                error = ''.join(traceback.format_exception(type(er), er, er.__traceback__))
                paginator.add_line('`'*3 + f'\n{error}' + '`'*3)

        for page in paginator.pages:
            await ctx.send(page, delete_after=5)

    @commands.command()
    async def load(self, ctx):
        embed = discord.Embed(description='◡̈ ‎ ‎__**open a ticket to**__:\n\n1. hire me free or paid\n2. mass with me\n\n__**to mass**:__\n1. type `-mass` in the ticket\n2. 2 ads pr ticket; 1 ticket per user\n\n__follow the instructions in the ticket after__', color=0x2F3136)
        await ctx.send(embed=embed, view=CreateView())

    @commands.command()
    async def invcheck(self, ctx):

        category_id = [1098196661148340284, 1105461295060353025, 1105462128107859978, 1105462240523600004, 1105462517586739240, 1105463989099565106, 1098198286772469840]
        valid = commands.Paginator(prefix='', suffix='')
        invalid = commands.Paginator(prefix='', suffix='')

        for id in category_id:
            category = self.bot.get_channel(id)
            for channel in category.channels:
                print(channel.name)
                async for message in channel.history(limit=1, oldest_first=True):
                    match = re.findall(r'(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?', message.content)
                    if match:
                        print(match)
                        try:
                            await asyncio.sleep(5)
                            await self.bot.fetch_invite(match[0])
                            valid.add_line(f'{channel.mention} is valid')
                        except discord.NotFound:
                            invalid.add_line(f'{channel.mention} is **invalid**')
                    else:
                        pass
        for page in valid.pages:
            await ctx.send(page)
        for page in invalid.pages:
            await ctx.send(page)

    @commands.command()
    async def open(self, ctx):
        total = 0
        channel = self.bot.get_channel(1119650620387897355)
        servers = [1098196661148340284, 1116684077236490290, 1105461295060353025, 1105462128107859978, 1105462240523600004, 1105462517586739240, 1105463989099565106]
        for x in servers: 
            category = self.bot.get_channel(x)
            total = total + len(category.channels)
        embed = discord.Embed(title='`` S `` `` T `` `` A `` `` T `` `` U `` `` S ``', description=f'\n**﹐mass** ``⟢`` **open**\n**﹢ hire** ``⟢`` **open**\n**﹐servercount** ``⟢`` **{total}**', color=0x2F3136)
        message = channel.get_partial_message(1119670765139271781)
        await message.edit(embed=embed)

    @commands.command()
    async def close(self, ctx):
        total = 0
        channel = self.bot.get_channel(1119650620387897355)
        servers = [1098196661148340284, 1116684077236490290, 1105461295060353025, 1105462128107859978, 1105462240523600004, 1105462517586739240, 1105463989099565106]
        for x in servers: 
            category = self.bot.get_channel(x)
            total = total + len(category.channels)
        embed = discord.Embed(title='`` S `` `` T `` `` A `` `` T `` `` U `` `` S ``', description=f'\n**﹐mass** ``⟢`` **closed**\n**﹢ hire** ``⟢`` **open**\n**﹐servercount** ``⟢`` **{total}**', color=0x2F3136)
        message = channel.get_partial_message(1119670765139271781)
        await message.edit(embed=embed)

