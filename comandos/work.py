import discord
from discord.ext import commands
import json
import os
import time

class Trabalhar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "database.json"

    def carregar_dados(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)
        with open(self.db_path, "r") as f:
            return json.load(f)

    def salvar_dados(self, dados):
        with open(self.db_path, "w") as f:
            json.dump(dados, f, indent=4)

    @commands.command(name="trabalhar")
    async def trabalhar(self, ctx):
        user_id = str(ctx.author.id)
        dados = self.carregar_dados()

        # Verifica se o usuário tem emprego
        if user_id not in dados or "emprego" not in dados[user_id]:
            prefixo = await self.get_prefix(ctx)
            return await ctx.send(f"❌ Você não tem um emprego ainda. Use `{prefixo}jobs` para arrumar um.")

        emprego = dados[user_id]["emprego"]
        empregos_disponiveis = dados.get("empregos", {})

        if emprego not in empregos_disponiveis:
            return await ctx.send("❌ O seu emprego não existe mais. Escolha outro com `jobs`.")

        salario = empregos_disponiveis[emprego]["salario"]
        cooldown = empregos_disponiveis[emprego]["cooldown"]

        tempo_atual = int(time.time())
        ultimo_trabalho = dados[user_id].get("ultimo_trabalho", 0)

        if tempo_atual - ultimo_trabalho < cooldown:
            restante = cooldown - (tempo_atual - ultimo_trabalho)
            minutos = restante // 60
            segundos = restante % 60
            return await ctx.send(f"⏳ Você está cansado! Tente novamente em **{minutos}m {segundos}s**.")

        # Pagar salário
        saldo = dados[user_id].get("saldo", 0)
        saldo += salario
        dados[user_id]["saldo"] = saldo
        dados[user_id]["ultimo_trabalho"] = tempo_atual

        self.salvar_dados(dados)

        await ctx.send(
            f"💼 Você trabalhou como **{emprego}** e recebeu **{salario} LC$**!\n"
            f"💰 Saldo atual: **{saldo} LC$**"
        )

    async def get_prefix(self, ctx):
        # Método para tentar pegar o prefixo atual do servidor
        try:
            with open("database.json", "r") as f:
                db = json.load(f)
            prefix = db.get(str(ctx.guild.id), {}).get("prefix", "li!")
        except:
            prefix = "li!"
        return prefix


async def setup(bot):
    await bot.add_cog(Trabalhar(bot))