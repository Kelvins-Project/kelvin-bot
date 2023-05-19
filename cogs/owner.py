import discord
from discord.ext import commands
from views.create import CreateView
import traceback
from views.embed_builder import BaseView
from discord import app_commands

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

    @app_commands.command(name='embed', description='Make an embed')
    async def messagemaker(self, interaction): 

        view = BaseView(interaction, self.bot.session)
        await interaction.response.send_message(view.content, view = view)
        message = await interaction.original_response()
        view.set_message(message)
        await view.wait()

async def setup(bot):
    await bot.add_cog(Owner(bot))
    