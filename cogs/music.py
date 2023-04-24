import discord
from discord.ext import commands
import asyncio
import wavelink


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
    async def play_(self, ctx, *, search: str):
        embed = discord.Embed(color=0x2F3136)
        queue = discord.Embed(color=0x2F3136)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        vc.autoplay = True
        track = await wavelink.YouTubeTrack.search(search, return_first=True)
        embed.description = f'playing: {track.title} requested by {ctx.author.mention}'
        queue.description = f'queued: {track.title} requested by {ctx.author.mention}'

        if not vc.is_playing():
            await vc.play(track, populate=True)
            await ctx.send(embed=embed)
        else:
            await vc.queue.put_wait(track)
            await ctx.send(embed=queue)

    @commands.hybrid_command(name='pause', description='Pauses the currently playing song.')
    async def pause_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'paused {vc.current.title} by {ctx.author.mention}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass

        await vc.set_pause(True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='resume', description='Resumes the currently playing song.')
    async def resume_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'resumed {vc.current.title} by {ctx.author.mention}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass

        await vc.set_pause(False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='skip', description='Skips the currently playing song.')
    async def skip_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'skipped {vc.current.title} by {ctx.author.mention}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass
        await vc.stop()
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
            async for track in vc.queue:
                embed.add_field(name=track.title, value=track.author, inline=False)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='leave', description='Stops the currently playing song and destroys the player.')
    async def leave_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'disconnected from: {ctx.author.voice.channel.mention}', color=0x2F3136)
        if not vc or not vc.is_playing():
            pass

        await vc.disconnect()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))