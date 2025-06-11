import discord
from discord.ext import commands
from database import cursor, criar_usuario, obter_dados_usuario
import sqlite3

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rank", aliases=["ranking", "top"])
    async def rank(self, ctx):
        # Garante que o usuário está no banco
        criar_usuario(ctx.author.id)

        # Consulta os top 10 usuários com maior total (wallet + bank)
        cursor.execute("""
            SELECT _id, wallet + bank as total
            FROM users
            ORDER BY total DESC
            LIMIT 10
        """)
        top_usuarios = cursor.fetchall()

        embed = discord.Embed(
            title="🏆 Ranking dos Mais Ricos",
            description="Top 10 usuários com mais LC$",
            color=discord.Color.gold()
        )

        for i, (user_id, total) in enumerate(top_usuarios, start=1):
            user = await self.bot.fetch_user(int(user_id))
            embed.add_field(name=f"{i}º - {user.name}", value=f"💰 {total} LC$", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rank(bot))