import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot, comandos_str):
        self.bot = bot
        # transforma string em lista
        self.comandos = [cmd.strip() for cmd in comandos_str.split(",") if cmd.strip()]
        self.comandos_por_pagina = 8

    @commands.command(name="help")
    async def help_command(self, ctx, pagina: int = 1):
        if pagina < 1:
            return await ctx.send("❌ A página precisa ser 1 ou maior.")

        total_paginas = (len(self.comandos) + self.comandos_por_pagina - 1) // self.comandos_por_pagina
        if pagina > total_paginas:
            return await ctx.send(f"❌ Essa página não existe. O máximo é {total_paginas}.")

        inicio = (pagina - 1) * self.comandos_por_pagina
        fim = inicio + self.comandos_por_pagina
        cmds_pagina = self.comandos[inicio:fim]

        comandos_formatados = "\n".join(f"• `{cmd}`" for cmd in cmds_pagina)

        embed = discord.Embed(
            title=f"📜 Lista de Comandos - Página {pagina}/{total_paginas}",
            description=comandos_formatados,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    comandos = "trabalhar, jobs, ping, help, userinfo, avatar, serverinfo, sorteio, futuro, conselho, botinfo, daily, sacar, depositar, rank, coinflip, 8ball, piada"
    await bot.add_cog(Help(bot, comandos))