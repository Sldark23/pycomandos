import discord
from discord.ext import commands
import time
from estruturadb import criar_usuario, obter_dados_usuario, atualizar_dado_usuario, registrar-tran

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="daily")
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        criar_usuario(user_id)
        dados = obter_dados_usuario(user_id)

        ultimo_daily = dados.get("ultimo_daily", 0)
        combo = dados.get("combo_daily", 1)
        agora = int(time.time())
        um_dia = 86400

        if agora - ultimo_daily < um_dia:
            restante = um_dia - (agora - ultimo_daily)
            horas = restante // 3600
            minutos = (restante % 3600) // 60
            segundos = restante % 60
            return await ctx.send(
                f"⏳ Você já coletou sua recompensa diária hoje!\n"
                f"Tente novamente em {horas}h {minutos}m {segundos}s."
            )

        # Reinicia o combo se passaram mais de 2 dias sem coletar
        if agora - ultimo_daily > um_dia * 2:
            combo = 1
        else:
            combo += 1
            if combo > 7:
                combo = 1

        recompensa = 2500 * (2 ** (combo - 1))
        novo_saldo = dados["wallet"] + recompensa

        # Atualiza os dados
        atualizar_dado_usuario(user_id, "wallet", novo_saldo)
        atualizar_dado_usuario(user_id, "ultimo_daily", agora)
        atualizar_dado_usuario(user_id, "combo_daily", combo)

        await ctx.send(
            f"🎁 Você coletou **LC$ {recompensa:,}** de recompensa diária!\n"
            f"🔥 Combo diário: {combo}/7"
        )

async def setup(bot):
    await bot.add_cog(Daily(bot))