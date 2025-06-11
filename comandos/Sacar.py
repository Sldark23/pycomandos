import discord
from discord.ext import commands
from database import criar_usuario, obter_dados_usuario, atualizar_dado_usuario

class Sacar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sacar")
    async def sacar(self, ctx, valor):
        criar_usuario(ctx.author.id)
        user_data = obter_dados_usuario(ctx.author.id)

        if valor.lower() in ["tudo", "all", "max"]:
            valor = user_data["bank"]
        else:
            try:
                valor = int(valor)
            except ValueError:
                return await ctx.send("❌ Valor inválido.")

        if valor <= 0:
            return await ctx.send("❌ O valor precisa ser maior que zero.")
        if user_data["bank"] < valor:
            return await ctx.send("❌ Você não tem dinheiro suficiente no banco.")

        atualizar_dado_usuario(ctx.author.id, "bank", user_data["bank"] - valor)
        atualizar_dado_usuario(ctx.author.id, "wallet", user_data["wallet"] + valor)

        await ctx.send(f"🏦 Você sacou {valor} LC$ da sua conta bancária!")

async def setup(bot):
    await bot.add_cog(Sacar(bot))