import discord
from discord.ext import commands
import asyncio

class Help(commands.Cog):
    def __init__(self, bot, comandos_str):
        self.bot = bot
        # Recebe string com comandos separados por vírgulas
        if isinstance(comandos_str, str):
            self.comandos = [cmd.strip() for cmd in comandos_str.split(",") if cmd.strip()]
        elif isinstance(comandos_str, list):
            self.comandos = comandos_str
        else:
            self.comandos = []

        self.comandos_por_pagina = 8  # máximo de comandos por página

    @commands.command(name="help")
    async def help_command(self, ctx):
        if not self.comandos:
            return await ctx.send("❌ Nenhum comando disponível no momento.")

        # Divide comandos em páginas
        paginas = [self.comandos[i:i + self.comandos_por_pagina] for i in range(0, len(self.comandos), self.comandos_por_pagina)]

        def criar_embed(pagina_num):
            cmds = paginas[pagina_num]
            comandos_formatados = "\n".join(f"• `{cmd}`" for cmd in cmds)
            embed = discord.Embed(
                title=f"📜 Lista de Comandos (Página {pagina_num + 1}/{len(paginas)})",
                description=comandos_formatados,
                color=discord.Color.blue()
            )
            return embed

        pagina_atual = 0
        mensagem = await ctx.send(embed=criar_embed(pagina_atual))

        if len(paginas) == 1:
            return  # Só tem uma página, não precisa de reação

        # Adiciona reações para navegação
        await mensagem.add_reaction("◀️")
        await mensagem.add_reaction("▶️")

        def checar(reaction, user):
            return user == ctx.author and reaction.message.id == mensagem.id and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=checar)

                if str(reaction.emoji) == "▶️":
                    if pagina_atual + 1 < len(paginas):
                        pagina_atual += 1
                        await mensagem.edit(embed=criar_embed(pagina_atual))
                    await mensagem.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️":
                    if pagina_atual > 0:
                        pagina_atual -= 1
                        await mensagem.edit(embed=criar_embed(pagina_atual))
                    await mensagem.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                # Timeout: remove as reações para indicar que a interação terminou
                try:
                    await mensagem.clear_reactions()
                except:
                    pass
                break

async def setup(bot):
    comandos = "trabalhar, jobs, ping, help, userinfo, avatar, serverinfo, sorteio, futuro, conselho, botinfo, daily, sacar, depositar, rank, coinflip, 8ball, piada"
    await bot.add_cog(Help(bot, comandos))