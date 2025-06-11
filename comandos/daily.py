import discord
from discord.ext import commands
import time
from estruturadb import criar_usuario, obter_dados_usuario, atualizar_dado_usuario

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="daily")
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        criar_usuario(user_id)
        dados = obter_dados_usuario(user_id)

        # Recupera o timestamp e o streak atual (dias consecutivos)
        ultimo_daily = dados.get("ultimo_daily", 0)
        streak = dados.get("streak", 0)

        agora = int(time.time())
        um_dia = 86400  # 24 horas em segundos

        if agora - ultimo_daily < um_dia:
            restante = um_dia - (agora - ultimo_daily)
            horas = restante // 3600
            minutos = (restante % 3600) // 60
            segundos = restante % 60
            return await ctx.send(f"⏳ Você já coletou sua recompensa diária hoje!\nTente novamente em {horas}h {minutos}m {segundos}s.")

        # Atualiza o streak (reinicia se passou mais de 2 dias sem coletar)
        if agora - ultimo_daily > um_dia * 2:
            streak = 0

        streak += 1
        if streak > 7:
            streak = 1

        # Cálculo da recompensa
        recompensa = 2500 * (2 ** (streak - 1))
        novo_saldo = dados["wallet"] + recompensa

        # Atualiza o usuário
        atualizar_dado_usuario(user_id, "wallet", novo_saldo)
        atualizar_dado_usuario(user_id, "ultimo_daily", agora)
        atualizar_dado_usuario(user_id, "streak", streak)

        await ctx.send(
            f"🎁 Você coletou sua recompensa diária de **LC$ {recompensa:,}**!\n"
            f"📅 Dias consecutivos: {streak}/7"
        )

async def setup(bot):
    await bot.add_cog(Daily(bot))