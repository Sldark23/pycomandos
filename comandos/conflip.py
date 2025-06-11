import discord
from discord.ext import commands
import random

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", aliases=["caraoucoroa", "flip", "moeda"])
    async def coinflip(self, ctx):
        """Jogue cara ou coroa!"""
        resultado = random.choice(["🪙 Cara", "🪙 Coroa"])
        await ctx.send(f"{ctx.author.mention}, deu **{resultado}**!")

async def setup(bot):
    await bot.add_cog(Coinflip(bot))