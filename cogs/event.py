from discord.ext import commands
import traceback
import sys
import discord
class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener()
    async def on_message_edit(self, before : discord.Message, after : discord.Message):
        #if before.content != after.content:
        #    ctx = await self.bot.get_context(after)
        #    await self.bot.invoke(ctx)
        channel = self.bot.get_channel(1097334267060682873)
        embed = discord.Embed(title="Message Edited", description=f"**Before:** ``{before.content}``\n**After:** ``{after.content}``", color=0x2F3136)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message : discord.Message):
        channel = self.bot.get_channel(1097334267060682873)
        embed = discord.Embed(title="Message Deleted", description=f"Message by {message.author}: ``{message.content}``", color=0x2F3136)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log = self.bot.get_channel(1097334267060682873)
        channel = self.bot.get_channel(1097198382969274399)
        embed = discord.Embed(description=f"welc {member.mention}\nenjoy your stay", color=0x2F3136)
        loge = discord.Embed(title="Member Joined", description=f"{member.mention} has joined the server.", color=0x2F3136)
        await log.send(embed=loge)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log = self.bot.get_channel(1097334267060682873)
        loge = discord.Embed(title="Member Left", description=f"{member.mention} has left the server.", color=0x2F3136)
        await log.send(embed=loge)

            

        
async def setup(bot):
    await bot.add_cog(Event(bot))