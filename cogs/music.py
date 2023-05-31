import discord
from discord.ext import commands
import asyncio
import wavelink
from wavelink.ext import spotify
import random

async def setup(bot):
    await bot.add_cog(Music(bot))
    
class Music(commands.Cog):

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}


    @commands.hybrid_command(name='join', description='Joins a voice channel. If no channel is given, joins the channel you are in.')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):

        if not channel:
            channel = ctx.author.voice.channel
            
        embed = discord.Embed(description=f'connected to: {channel.mention}', color=0x2F3136)
        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                pass
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                pass

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='play', description='Plays a song. If a song is already playing, it will be added to the queue.')
    async def play_(self, ctx, search: str):
        embed = discord.Embed(color=0x2F3136)
        queue = discord.Embed(color=0x2F3136)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        vc.autoplay = True

        if spotify.decode_url(search):
        
            if search.startswith('https://open.spotify.com/playlist'):
                async for tracks in spotify.SpotifyTrack.iterator(query=search, type=spotify.SpotifySearchType.playlist):
                    track = vc.queue.put(tracks)
                    names = ', '.join(tracks.artists)
                    embed.description = f'playing: `{tracks.name}` by {names} requested by {ctx.author.mention}'
                    queue.description = f'queued: `{tracks.name}` requested by {ctx.author.mention}'
            elif search.startswith('https://open.spotify.com/track'):
                track = await spotify.SpotifyTrack.search(search)
                names = ', '.join(track.artists)
                embed.description = f'playing: `{track.name}` by {names} requested by {ctx.author.mention}'
                queue.description = f'queued: `{track.name}` by {names} requested by {ctx.author.mention}'
        else:
            track = await wavelink.YouTubeTrack.search(search, return_first=True)
            embed.description = f'playing: `{track.title}` by {track.author} requested by {ctx.author.mention}'
            queue.description = f'queued: `{track.title}` by {track.author} requested by {ctx.author.mention}'

        if not vc.is_playing():
            if vc.queue.is_empty:
                await vc.play(track)
                await ctx.send(embed=embed)
            else:
                await vc.play(vc.queue.get())
                await ctx.send(embed=embed)
        elif vc.is_playing():
            await vc.queue.put_wait(track)
            await ctx.send(embed=queue)

    @commands.hybrid_command(name='pause', description='Pauses the currently playing song.')
    async def pause_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'paused `{vc.current.title}` by {vc.current.author}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass

        await vc.set_pause(True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='resume', description='Resumes the currently playing song.')
    async def resume_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'resumed `{vc.current.title}` by {vc.current.author}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass

        await vc.set_pause(False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='skip', description='Skips the currently playing song.')
    async def skip_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'skipped `{vc.current.title}` by {vc.current.author}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass
        await vc.stop()
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='shuffle', description='Shuffles the queue.')
    async def shuffle_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'shuffled the queue.', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass
        random.shuffle(vc.queue._queue)
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='queue', description='Shows the current queue.')
    async def queue_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'queue for {ctx.guild.name}', color=0x2F3136)

        if not vc or not vc.is_playing():
            pass
        if vc.queue.is_empty:
            embed.description = 'there is nothing in the queue.'
        else:
            num = 1
            for track in vc.queue:
                try:
                    embed.add_field(name=f'{num}. {track.title}', value=f'by `{track.author}`', inline=False)
                except:
                    names = ', '.join(track.artists)
                    embed.add_field(name=f'{num}. {track.name}', value=f'by `{names}`', inline=False)
                num += 1

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='volume', description='Changes the volume of the player.')
    async def volume_(self, ctx, volume: int):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'volume set to {volume}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass

        await vc.set_volume(volume)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='stop', description='Stops the currently playing song and destroys the player.')
    async def stop_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'disconnected from: {ctx.author.voice.channel.mention}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass

        await vc.disconnect()
        await ctx.send(embed=embed)

