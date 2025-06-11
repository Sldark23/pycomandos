import discord
from discord.ext import commands
from database import criar_usuario, obter_dados_usuario, atualizar_dado_usuario

class Depositar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="depositar")
    async def depositar(self, ctx, valor: int):
        criar_usuario(ctx.author.id)
        user_data = obter_dados_usuario(ctx.author.id)

        if valor <= 0:
            return await ctx.send("❌ O valor precisa ser maior que zero.")
        if user_data["wallet"] < valor:
            return await ctx.send("❌ Você não tem dinheiro suficiente na carteira.")

        atualizar_dado_usuario(ctx.author.id, "wallet", user_data["wallet"] - valor)
        atualizar_dado_usuario(ctx.author.id, "bank", user_data["bank"] + valor)

        await ctx.send(f"💰 Você depositou {valor} LC$ no banco com sucesso!")

async def setup(bot):
    await bot.add_cog(Depositar(bot))