import discord
from discord.ext import commands
import random

class Magic8Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball", aliases=["bola", "pergunta"])
    async def _8ball(self, ctx, *, pergunta: str = None):
        """Faça uma pergunta e a bola mágica responderá."""
        if not pergunta:
            await ctx.send("🎱 Você precisa fazer uma pergunta!")
            return

        respostas = [
            "Sim.",
            "Com certeza!",
            "Não tenho certeza, tente novamente.",
            "Definitivamente não.",
            "Parece promissor.",
            "Não conte com isso.",
            "Sim, sem dúvidas!",
            "Minha resposta é não.",
            "Melhor não te dizer agora.",
            "Provavelmente sim.",
            "Talvez.",
            "Não posso prever agora.",
            "Altamente provável.",
            "Pouco provável.",
        ]

        resposta = random.choice(respostas)
        await ctx.send(f"🎱 **Pergunta:** {pergunta}\n**Resposta:** {resposta}")

async def setup(bot):
    await bot.add_cog(Magic8Ball(bot))