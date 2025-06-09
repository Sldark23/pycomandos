# comandos/atm.py

import discord
from discord.ext import commands
import json
import os

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="atm")
    async def atm(self, ctx):
        user_id = str(ctx.author.id)

        # Verifica se o arquivo database.json existe
        if not os.path.exists("database.json"):
            with open("database.json", "w") as f:
                json.dump({}, f)

        with open("database.json", "r") as f:
            db = json.load(f)

        if user_id not in db:
            db[user_id] = {"wallet": 0, "bank": 0}

        wallet = db[user_id].get("wallet", 0)
        bank = db[user_id].get("bank", 0)

        embed = discord.Embed(title=f"💳 Carteira de {ctx.author.name}", color=discord.Color.green())
        embed.add_field(name="💵 Dinheiro na Mão", value=f"R${wallet}", inline=False)
        embed.add_field(name="🏦 Banco", value=f"R${bank}", inline=False)

        await ctx.send(embed=embed)

        # Salvar novamente após possível criação de conta
        with open("database.json", "w") as f:
            json.dump(db, f, indent=4)

async def setup(bot):
    await bot.add_cog(Economia(bot))