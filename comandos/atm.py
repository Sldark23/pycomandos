import discord
from discord.ext import commands
import json

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "database.json"

    def get_user_data(self, user_id):
        with open(self.db_path, "r") as f:
            data = json.load(f)
        user_id = str(user_id)
        if user_id not in data:
            data[user_id] = {"carteira": 0, "banco": 0}
            with open(self.db_path, "w") as f:
                json.dump(data, f, indent=4)
        return data[user_id]

    @commands.command(name="atm")
    async def atm(self, ctx):
        user = ctx.author
        data = self.get_user_data(user.id)

        embed = discord.Embed(title="🏦 ATM", color=discord.Color.blue())
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.add_field(name="💵 Carteira", value=f"R$ {data['carteira']:,}", inline=True)
        embed.add_field(name="🏦 Banco", value=f"R$ {data['banco']:,}", inline=True)
        embed.set_footer(text="Sistema de Economia - Lioran Bot")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economia(bot))
