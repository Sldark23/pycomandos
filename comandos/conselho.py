import discord
from discord.ext import commands
import random

class Conselho(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conselhos = [
            "🧠 Pense antes de agir... ou finja que pensou.",
            "😎 O segredo do sucesso é parecer que você sabe o que está fazendo.",
            "📴 Se tudo falhar, reinicie. Inclusive você mesmo.",
            "💡 A vida é curta. Use o comando `li!futuro` antes que acabe.",
            "🧂 Nunca discuta com gente burra. Eles têm mais experiência.",
            "📚 Estudar é importante, mas saber usar memes na hora certa é vital.",
            "🔥 Faça o seu melhor... e depois culpe o estagiário.",
            "🚪 Portas se abrem para quem sabe chutar.",
            "🧊 Mantenha a calma. Ou finja muito bem.",
            "📈 Um bom conselho: aceite bons conselhos."
        ]

    @commands.command(name="conselho")
    async def conselho(self, ctx):
        conselho = random.choice(self.conselhos)
        await ctx.send(f"{ctx.author.mention} {conselho}")

async def setup(bot):
    await bot.add_cog(Conselho(bot))