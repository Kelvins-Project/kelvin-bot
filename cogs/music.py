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

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        track = await wavelink.YouTubeTrack.search(search, return_first=True)
        await vc.play(track)


    @commands.hybrid_command(name='leave', description='Stops the currently playing song and destroys the player.')
    async def leave_(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        embed = discord.Embed(description=f'disconnected from: {ctx.author.voice.channel.mention}', color=0x2F3136)
        if not vc or not vc.is_connected():
            pass

        await vc.disconnect()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))