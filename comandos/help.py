import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot, categorias_comandos):
        self.bot = bot
        # categorias_comandos deve ser um dict {categoria: comandos_string}
        # Exemplo: {"Diversão": "piada, 8ball", "Economia": "trabalhar, sacar"}
        self.categorias = {}
        for categoria, cmds_str in categorias_comandos.items():
            # Transforma string separada por vírgulas em lista, tirando espaços extras
            self.categorias[categoria] = [cmd.strip() for cmd in cmds_str.split(",") if cmd.strip()]

    @commands.command(name="help")
    async def help_command(self, ctx):
        if not self.categorias:
            return await ctx.send("❌ Nenhum comando disponível no momento.")

        embed = discord.Embed(
            title="📜 Lista de Comandos",
            color=discord.Color.blue()
        )

        for categoria, cmds in self.categorias.items():
            # Formata a lista em string com um comando por linha e um emoji antes
            comandos_formatados = "\n".join(f"• `{cmd}`" for cmd in cmds)
            embed.add_field(name=f"📂 {categoria}", value=comandos_formatados, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    # Exemplo de categorias com comandos (strings separados por vírgula)
    categorias = {
        "Diversão": "piada, 8ball, coinflip",
        "Economia": "trabalhar, jobs, sacar, depositar, daily, rank",
        "Informações": "userinfo, avatar, serverinfo, botinfo",
        "Utilitários": "help, ping, sorteio, conselho, futuro"
    }
    await bot.add_cog(Help(bot, categorias))