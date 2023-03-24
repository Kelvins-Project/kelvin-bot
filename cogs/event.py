from discord.ext import commands
import traceback
import sys
import discord
from io import BytesIO
class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener()
    async def on_message_edit(self, before : discord.Message, after : discord.Message):
        if before.content != after.content:
            ctx = await self.bot.get_context(after)
            await self.bot.invoke(ctx)

    @commands.Cog.listener()
    async def on_user_update(self, before : discord.User, after : discord.User):
        if before.id != 675104167345258506:
            return
        elif before.name != after.name:
            await self.bot.user.edit(username=after.name)
        elif before.avatar.url != after.avatar.url:
            image_bytes = await self.bot.session.get(after.avatar.url)
            image = BytesIO(await image_bytes.read())
            await self.bot.user.edit(avatar=image.getvalue())

    @commands.Cog.listener()
    async def on_presence_update(self, before : discord.Member, after : discord.Member):
        if before.id != 675104167345258506:
            return
        elif before.status != after.status:
            await self.bot.change_presence(status=after.status)


async def setup(bot):
    await bot.add_cog(Event(bot))