import discord
from discord.ext import commands
import sqlite3
import asyncio

class Extrato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="extrato")
    async def extrato(self, ctx):
        user_id = str(ctx.author.id)
        conn = sqlite3.connect("lioranbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tipo, valor, descricao, data 
            FROM extrato 
            WHERE user_id = ? 
            ORDER BY id DESC
        """, (user_id,))
        transacoes = cursor.fetchall()
        conn.close()

        if not transacoes:
            await ctx.send("📄 Você ainda não tem transações registradas.")
            return

        itens_por_pagina = 5
        total_paginas = (len(transacoes) + itens_por_pagina - 1) // itens_por_pagina
        pagina_atual = 0

        def gerar_embed(pagina):
            inicio = pagina * itens_por_pagina
            fim = inicio + itens_por_pagina
            embed = discord.Embed(
                title=f"📄 Extrato de {ctx.author.display_name}",
                description=f"Página {pagina + 1} de {total_paginas}",
                color=discord.Color.green()
            )
            for tipo, valor, descricao, data in transacoes[inicio:fim]:
                emoji = "📥" if tipo == "entrada" else "📤"
                embed.add_field(
                    name=f"{emoji} {descricao}",
                    value=f"💰 {valor} LC$ • 🕒 {data}",
                    inline=False
                )
            return embed

        mensagem = await ctx.send(embed=gerar_embed(pagina_atual))

        botoes = ["⏮", "⏪", "⏩", "⏭"]
        for botao in botoes:
            await mensagem.add_reaction(botao)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in botoes and reaction.message.id == mensagem.id

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if reaction.emoji == "⏮":
                    pagina_atual = 0
                elif reaction.emoji == "⏪" and pagina_atual > 0:
                    pagina_atual -= 1
                elif reaction.emoji == "⏩" and pagina_atual < total_paginas - 1:
                    pagina_atual += 1
                elif reaction.emoji == "⏭":
                    pagina_atual = total_paginas - 1

                await mensagem.edit(embed=gerar_embed(pagina_atual))
                await mensagem.remove_reaction(reaction.emoji, user)

            except asyncio.TimeoutError:
                break

# Setup async para discord.py 2.x
async def setup(bot):
    await bot.add_cog(Extrato(bot))