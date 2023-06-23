import discord
from discord.ext import menus
from discord.ext import commands
from discord import ui
from views.create import CreateView
import traceback
import re
import asyncio

async def setup(bot):
    await bot.add_cog(Owner(bot))

class InvitePaginator(menus.ListPageSource):
    async def format_page(self, menu, item):
        format = ' \n'.join(item)
        embed = discord.Embed(description=format, color=0x2F3136)
        return embed
        
class InviteMenu(ui.View, menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=600)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None

    async def start(self, ctx, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @ui.button(emoji='\U000023ea', style=discord.ButtonStyle.blurple)
    async def first_page(self, interaction, button):
        await self.show_page(0)
        await interaction.response.edit_message(view=self)

    @ui.button(emoji='\U000025c0', style=discord.ButtonStyle.blurple)
    async def before_page(self, interaction, button):
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.edit_message(view=self)

    @ui.button(emoji='\U0000274c', style=discord.ButtonStyle.blurple)
    async def stop_page(self, interaction, button):
        self.stop()
        await interaction.response.edit_message(view=None)

    @ui.button(emoji='\U000025b6', style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction, button):
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.edit_message(view=self)

    @ui.button(emoji='\U000023e9', style=discord.ButtonStyle.blurple)
    async def last_page(self, interaction, button):
        await self.show_page(self._source.get_max_pages() - 1)
        await interaction.response.edit_message(view=self)
      
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
        embed = discord.Embed(title='`` T `` `` I `` `` C `` `` K `` `` E `` `` T ``', description='**open a ticket to**:\n - hire me free or paid\n- mass with me\n\n**to mass**:\n - type `-mass` in the ticket\n- 2 ads pr ticket; 1 ticket per user\n\n__follow the instructions in the ticket after__', color=0x2F3136)
        await ctx.send(embed=embed, view=CreateView())

    @commands.command()
    async def invcheck(self, ctx):
        category_id = [1098196661148340284, 1105461295060353025, 1105462128107859978, 1105462240523600004, 1105462517586739240, 1105463989099565106, 1098198286772469840]
        item = []
        async with ctx.typing():
            for id in category_id:
                category = self.bot.get_channel(id)
                for channel in category.channels:
                    async for message in channel.history(limit=1, oldest_first=True):
                        match = re.findall(r'(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?', message.content)
                        if match:
                            try:
                                await asyncio.sleep(1)
                                await self.bot.fetch_invite(match[0])
                                item.append(f'{channel.mention} - `1/1` found \U0001f7e2')
                            except discord.NotFound:
                                item.append(f'{channel.mention} - `1/1` found\U0001f534')
                        else:
                            pass
        pages = InvitePaginator(item, per_page=20)
        menu = InviteMenu(pages)
        await menu.start(ctx)

    @commands.command()
    async def status(self, ctx, *, option):
        total = 0
        channel = self.bot.get_channel(1119650620387897355)
        servers = [1098196661148340284, 1116684077236490290, 1105461295060353025, 1105462128107859978, 1105462240523600004, 1105462517586739240, 1105463989099565106]
        for x in servers: 
            category = self.bot.get_channel(x)
            total = total + len(category.channels)
        embed = discord.Embed(title='`` S `` `` T `` `` A `` `` T `` `` U `` `` S ``', description=f'\n**﹐mass** ``⟢`` **{option}**\n**﹢ hire** ``⟢`` **open**\n**﹐servercount** ``⟢`` **{total}**', color=0x2F3136)
        message = channel.get_partial_message(1119670765139271781)
        await message.edit(embed=embed)
        await ctx.message.delete()


