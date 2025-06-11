import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot, comandos_str):
        self.bot = bot
        # Pode receber string ou lista
        if isinstance(comandos_str, str):
            # Transforma string separada por vírgulas em lista, tirando espaços extras
            self.comandos = [cmd.strip() for cmd in comandos_str.split(",") if cmd.strip()]
        elif isinstance(comandos_str, list):
            self.comandos = comandos_str
        else:
            self.comandos = []

    @commands.command(name="help")
    async def help_command(self, ctx):
        if not self.comandos:
            return await ctx.send("❌ Nenhum comando disponível no momento.")

        # Formata a lista em string com um comando por linha e um emoji antes
        comandos_formatados = "\n".join(f"• `{cmd}`" for cmd in self.comandos)

        embed = discord.Embed(
            title="📜 Lista de Comandos",
            description=comandos_formatados,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    # Exemplo de comandos passados como string com vírgulas
    comandos = "trabalhar, jobs, ping, help, userinfo, avatar, serverinfo, sorteio, futuro, conselho, botinfo, daily, sacar, depositar"
    await bot.add_cog(Help(bot, comandos))