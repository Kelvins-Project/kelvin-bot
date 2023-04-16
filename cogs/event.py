from discord.ext import commands
import traceback
import sys
import discord
import datetime
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
        channel = self.bot.get_channel(1097214136460517476)
        await channel.send(f'{after.author} editted "{before.content}" to "{after.content}" in {after.channel.mention}')
    

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        if message.channel.id != 1097200149035483238:
            return 
        if message.content.lower() != "verify me":
            await message.delete()
        else:
            logs = self.bot.get_channel(1097214136460517476)
            channel = self.bot.get_channel(1097198382969274399)
            await message.delete()
            await message.author.add_roles(message.guild.get_role(1097199833917444237))
            await channel.send(f'{message.author.mention} welcome to the server!')
            await logs.send(f'{message.author} verified themselves')

    @commands.Cog.listener()
    async def on_message_delete(self, message : discord.Message):
        channel = self.bot.get_channel(1097214136460517476)
        await channel.send(f'{message.author} deleted "{message.content}" in {message.channel.mention}') 

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1097214136460517476)
        await channel.send(f'member {member} joined the server')
        
    
        
async def setup(bot):
    await bot.add_cog(Event(bot))