import discord
from discord.ext import commands
import time
from database import criar_usuario, obter_dados_usuario, atualizar_dado_usuario

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="daily")
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        criar_usuario(user_id)
        user_data = obter_dados_usuario(user_id)

        tempo_atual = int(time.time())
        tempo_ultimo = user_data.get("ultimo_daily", 0)
        combo = user_data.get("combo_daily", 1)
        tempo_espera = 86400  # 24 horas

        if tempo_atual - tempo_ultimo < tempo_espera:
            restante = tempo_espera - (tempo_atual - tempo_ultimo)
            horas = restante // 3600
            minutos = (restante % 3600) // 60
            segundos = restante % 60
            return await ctx.send(
                f"⏳ Você já coletou seu daily!\n"
                f"Tente novamente em **{horas}h {minutos}m {segundos}s**."
            )

        # Cálculo da recompensa: 2500 * 2^(combo-1)
        recompensa_base = 2500
        recompensa = recompensa_base * (2 ** (combo - 1))

        # Adicionar ao saldo
        novo_saldo = user_data["wallet"] + recompensa
        atualizar_dado_usuario(user_id, "wallet", novo_saldo)
        atualizar_dado_usuario(user_id, "ultimo_daily", tempo_atual)

        # Atualiza combo
        proximo_combo = combo + 1 if combo < 7 else 1
        atualizar_dado_usuario(user_id, "combo_daily", proximo_combo)

        await ctx.send(
            f"🎁 **Daily de Dia {combo}** coletado!\n"
            f"💵 Você recebeu **LC$ {recompensa:,}**.\n"
            f"🔁 Combo atualizado para o dia {proximo_combo}!"
        )

def setup(bot):
    bot.add_cog(Daily(bot))