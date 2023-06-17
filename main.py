import discord 
from discord.ext import commands
import os
from config import bot_token, lava_token, client_id, client_secret, db_link
import aiohttp
from views.create import CreateView
from views.close import CloseView
from views.dm_close import DMCloseView
import asyncpg

prefix = ['-']

os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=0x2F3136)
        for cog, commands in mapping.items():
           command_signatures = [self.get_command_signature(c) for c in commands]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "\n\u200b")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = prefix, 
                        case_insensitive = True, 
                        trip_after_prefix=True, 
                        help_command=MyHelp(),
                        activity = discord.Activity(name='tickets', type=discord.ActivityType.watching), 
                        status = discord.Status.online, 
                        intents=discord.Intents.all(), 
                        owner_ids = [675104167345258506])

    async def setup_hook(self):
        self.add_view(CreateView())
        self.add_view(CloseView())
        self.add_view(DMCloseView())
        self.session = aiohttp.ClientSession()
        #self.db = await asyncpg.create_pool(db_link)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} has been loaded!")

    async def on_ready(self):
        print(self.user.id)

if __name__ == '__main__':
    bot = Bot()
    bot.run(bot_token)