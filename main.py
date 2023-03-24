import discord 
from discord.ext import commands
import os
import asyncpg
from config import bot_token, db_token

prefix = ['kelvin ', 'kel ', 'kelkel ', '<@944623479523774464> ', '<@944623479523774464>']

os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = prefix, 
                        case_insensitive = True, 
                        trip_after_prefix=True, 
                        activity = discord.Activity(name='e', type=discord.ActivityType.watching), 
                        status = discord.Status.idle, 
                        intents=discord.Intents.all(), 
                        owner_ids = [675104167345258506])
        self.produce = 0

    async def setup_hook(self):
        self.db = await asyncpg.create_pool(db_token)
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS user_inventory (
                user_id BIGINT NOT NULL,
                user_name TEXT NOT NULL,
                drug_amount BIGINT NULL
            );
        ''')
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS drug_stock (
                meth_amount BIGINT NOT NULL
            );
        ''')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} has been loaded!")

    async def on_ready(self):
        print(self.user.id)

if __name__ == '__main__':
    bot = Bot()
    bot.run(bot_token)