import discord
from discord.ext import commands
import random

class Futuro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.previsoes = [
            "🔮 Vejo você encontrando **5 LC$** no sofá amanhã... Sorte ou magia?",
            "⚡ Um dragão emocional vai bagunçar seu dia. Evite tretas no grupo hoje.",
            "💘 Você vai se apaixonar por algo... provavelmente comida.",
            "💼 Seu chefe espiritual disse que você vai ganhar uma promoção imaginária.",
            "🍀 Seus caminhos se cruzarão com um meme raro. Prepare-se.",
            "🧙‍♂️ Uma força mística te dará vontade de trabalhar... mas você vai ignorar.",
            "🚀 Você será abduzido por ideias geniais em breve.",
            "🕰️ O tempo está do seu lado hoje. Aproveite... ou durma mais um pouco.",
            "💣 Alguém vai te mandar um 'oi sumido(a)'. Corra.",
            "🧊 Você está gelando corações por onde passa. Cuidado com os crushes."
        ]

    @commands.command(name="futuro")
    async def futuro(self, ctx):
        previsao = random.choice(self.previsoes)
        await ctx.send(f"{ctx.author.mention} {previsao}")

async def setup(bot):
    await bot.add_cog(Futuro(bot))