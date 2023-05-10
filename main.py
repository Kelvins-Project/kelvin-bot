import discord 
from discord.ext import commands
import os
from config import bot_token, lava_token, client_id, client_secret
import aiohttp
from views.create import CreateView
from views.close import CloseView
import wavelink
from wavelink.ext import spotify

prefix = ['-']

os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
os.environ['JISHAKU_HIDE'] = 'True'

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = prefix, 
                        case_insensitive = True, 
                        trip_after_prefix=True, 
                        activity = discord.Activity(name='tickets', type=discord.ActivityType.watching), 
                        status = discord.Status.online, 
                        intents=discord.Intents.all(), 
                        owner_ids = [675104167345258506])

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        self.add_view(CreateView())
        self.add_view(CloseView())
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} has been loaded!")
        sc = spotify.SpotifyClient(client_id=client_id, client_secret=client_secret)
        node: wavelink.Node = wavelink.Node(uri='167.235.231.92:25011', password=lava_token)
        await wavelink.NodePool.connect(client=self, nodes=[node], spotify=sc)

    async def on_ready(self):
        print(self.user.id)

if __name__ == '__main__':
    bot = Bot()
    bot.run(bot_token)