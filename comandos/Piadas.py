import discord
from discord.ext import commands
import random

class Piadas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Lista de piadas, aqui a variável chama "piadas"
        self.piadas = [
            "Por que o computador foi ao médico? Porque estava com um vírus!",
            "Qual é o café que não é para beber? O Java!",
            # Adicione suas piadas aqui...
        ]

    @commands.command(name="piada")
    async def piada(self, ctx):
        # Usa o atributo self.piadas para escolher uma piada
        piada_escolhida = random.choice(self.piadas)
        await ctx.send(f"😂 {piada_escolhida}")

async def setup(bot):
    await bot.add_cog(Piadas(bot))