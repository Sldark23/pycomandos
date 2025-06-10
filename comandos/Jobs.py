import discord
from discord.ext import commands
import json
import os

class Jobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "database.json"
        self.inicializar_empregos()

    def carregar_dados(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)
        with open(self.db_path, "r") as f:
            return json.load(f)

    def salvar_dados(self, dados):
        with open(self.db_path, "w") as f:
            json.dump(dados, f, indent=4)

    def inicializar_empregos(self):
        dados = self.carregar_dados()
        if "empregos" not in dados:
            dados["empregos"] = {
                "Programador": {"salario": 250, "cooldown": 1800},
                "Designer": {"salario": 230, "cooldown": 1800},
                "Entregador": {"salario": 150, "cooldown": 1200},
                "Mecânico": {"salario": 200, "cooldown": 1500},
                "Faxineiro": {"salario": 100, "cooldown": 900},
                "Professor": {"salario": 280, "cooldown": 2000},
                "Médico": {"salario": 350, "cooldown": 2400},
                "Garçom": {"salario": 130, "cooldown": 1000},
                "Motorista": {"salario": 170, "cooldown": 1300},
                "Segurança": {"salario": 160, "cooldown": 1400},
                "DJ": {"salario": 220, "cooldown": 1600},
                "Fotógrafo": {"salario": 210, "cooldown": 1500},
                "Youtuber": {"salario": 260, "cooldown": 1900},
                "Streamer": {"salario": 240, "cooldown": 1800},
                "Agricultor": {"salario": 180, "cooldown": 1200}
            }
            self.salvar_dados(dados)

    @commands.command(name="jobs")
    async def listar_empregos(self, ctx):
        dados = self.carregar_dados()
        empregos = dados.get("empregos", {})
        empregos_formatados = "\n".join([
            f"- {nome} | 💰 {info['salario']} LC$ | ⏱️ {info['cooldown'] // 60} min"
            for nome, info in empregos.items()
        ])
        await ctx.send(
            "**💼 Lista de empregos disponíveis:**\n\n"
            f"{empregos_formatados}\n\n"
            "Use `prefix!job [nome_do_emprego]` para escolher um."
        )

    @commands.command(name="job")
    async def escolher_emprego(self, ctx, *, nome_do_emprego: str = None):
        if nome_do_emprego is None:
            return await ctx.send("❌ Você precisa especificar um emprego. Ex: `prefix!job Programador`")

        nome_do_emprego = nome_do_emprego.title()
        dados = self.carregar_dados()
        empregos = dados.get("empregos", {})

        if nome_do_emprego not in empregos:
            return await ctx.send("❌ Esse emprego não está disponível. Use `prefix!jobs` para ver a lista.")

        user_id = str(ctx.author.id)
        if user_id not in dados:
            dados[user_id] = {}

        dados[user_id]["emprego"] = nome_do_emprego
        self.salvar_dados(dados)

        salario = empregos[nome_do_emprego]["salario"]
        cooldown = empregos[nome_do_emprego]["cooldown"] // 60

        await ctx.send(
            f"✅ Você agora está empregado como **{nome_do_emprego}**!\n"
            f"💰 Salário: **{salario} LC$**\n"
            f"⏱️ Cooldown: **{cooldown} minutos**"
        )

async def setup(bot):
    await bot.add_cog(Jobs(bot))