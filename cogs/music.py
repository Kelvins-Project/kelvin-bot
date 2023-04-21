import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from yt_dlp import YoutubeDL


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpegopts = {
    'before_options': '-nostdin ',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=True):

        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        embed = discord.Embed(description=f'added `{data["title"]}` to the queue', color=0x2F3136)
        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None 
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300): 
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)
            
            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            embed = discord.Embed(description=f'now playing: `{source.title}` requested by {source.requester.mention}', color=0x2F3136)
            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.hybrid_command(name='join', description='Joins a voice channel. If no channel is given, joins the channel you are in.')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')
            
        embed = discord.Embed(description=f'connected to: {channel.mention}', color=0x2F3136)
        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='play', description='Plays a song. If a song is already playing, it will be added to the queue.')
    async def play_(self, ctx, *, search: str):

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.hybrid_command(name='pause', description='Pauses the currently playing song.')
    async def pause_(self, ctx):
        nothing = discord.Embed(description=f'nothing is being played', color=0x2F3136)
        embed = discord.Embed(description=f'{ctx.author.mention} paused the song', color=0x2F3136)
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send(embed=nothing)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='resume', description='Resumes the currently paused song.')
    async def resume_(self, ctx):
        nothing = discord.Embed(description=f'nothing is being played', color=0x2F3136)
        embed = discord.Embed(description=f'{ctx.author.mention} resumed the song', color=0x2F3136)
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=nothing)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='skip', description='Skips the currently playing song.')
    async def skip_(self, ctx):
        nothing = discord.Embed(description=f'nothing is being played', color=0x2F3136)
        embed = discord.Embed(description=f'{ctx.author.mention} skipped the song', color=0x2F3136)
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=nothing)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='queue', description='Retrieves a basic queue of upcoming songs.')
    async def queue_info(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')

        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'`{_["title"]}`' for _ in upcoming)
        embed = discord.Embed(description=f'next up: {len(upcoming)}\n{fmt}', color=0x2F3136)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='np', description='Displays the currently playing song.')
    async def now_playing_(self, ctx):
        nothing = discord.Embed(description=f'nothing is being played', color=0x2F3136)
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send(embed=nothing)
        embed = discord.Embed(description=f'now playing: `{vc.source.title}` requested by {vc.source.requester.mention}', color=0x2F3136)
        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(embed=embed)

    @commands.hybrid_command(name='volume', description='Changes the volume of the player.')
    async def change_volume(self, ctx, *, vol: float):
        embed = discord.Embed(description=f'{ctx.author.mention}: set the volume to `{vol}%`', color=0x2F3136)
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='leave', description='Stops the currently playing song and destroys the player.')
    async def leave_(self, ctx):
        vc = ctx.voice_client
        embed = discord.Embed(description=f'disconnected from: {ctx.author.voice.channel.mention}', color=0x2F3136)
        if not vc or not vc.is_connected():
            pass

        await self.cleanup(ctx.guild)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))