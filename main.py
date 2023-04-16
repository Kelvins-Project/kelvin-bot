import discord 
from discord.ext import commands
import os
from config import bot_token


prefix = ['kelvin ', 'kel ', 'kelkel ', '<@944623479523774464> ', '<@944623479523774464>']

os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = prefix, 
                        case_insensitive = True, 
                        trip_after_prefix=True, 
                        activity = discord.Activity(name='the alive', type=discord.ActivityType.watching), 
                        status = discord.Status.online, 
                        intents=discord.Intents.all(), 
                        owner_ids = [675104167345258506])

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} has been loaded!")

    async def on_ready(self):
        print(self.user.id)

if __name__ == '__main__':
    bot = Bot()
    bot.run(bot_token)