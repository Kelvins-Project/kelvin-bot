from discord.ext import commands
import discord

async def setup(bot):
    await bot.add_cog(Economy(bot))

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.hybrid_command(name='daily', description='Get daily rewards!')
    async def daily(self, ctx):
        embed = discord.Embed(description=f'you claimed your daily reward of 150 coins!', color=0x2F3136)
        query = await self.bot.db.fetch('SELECT user_id FROM economy WHERE user_id = $1', ctx.author.id)
        if bool(query) == False:
            await self.bot.db.execute('INSERT INTO economy (user_id, balance) VALUES ($1, $2)', ctx.author.id, 0)
            await self.bot.db.execute('UPDATE economy SET balance = balance + 150 WHERE user_id = $1', ctx.author.id)
            await ctx.send(embed=embed)
        else:
            await self.bot.db.execute('UPDATE economy SET balance = balance + 150 WHERE user_id = $1', ctx.author.id)
            await ctx.send(embed=embed)

    @commands.hybrid_command(name='balance', description='Get your balance')
    async def balance(self, ctx):
        embed = discord.Embed(color=0x2F3136)
        balance = await self.bot.db.fetchval('SELECT balance FROM economy WHERE user_id = $1', ctx.author.id)
        embed.description = f'you have {balance} coins'
        await ctx.send(embed=embed)
    


