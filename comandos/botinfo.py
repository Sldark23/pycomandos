import discord
from discord.ext import commands
import platform
import psutil
import time

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.owner_id = 1242430100184502303  # Seu ID fixo

    @commands.command(name="botinfo")
    async def botinfo(self, ctx):
        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{hours}h {minutes}m {seconds}s"

        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_usage = memory.percent

        os_info = f"{platform.system()} {platform.release()}"

        latency = round(self.bot.latency * 1000)

        owner_user = self.bot.get_user(self.owner_id)
        owner_name = f"slbimp"

        embed = discord.Embed(title="🤖 Informações do Bot", color=discord.Color.blue())
        embed.add_field(name="Nome", value=f"{self.bot.user.name}#{self.bot.user.discriminator}", inline=True)
        embed.add_field(name="ID do Bot", value=str(self.bot.user.id), inline=True)
        embed.add_field(name="Dono", value=owner_name, inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Servidores", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="Usuários totais", value=f"{len(set(self.bot.get_all_members()))}", inline=True)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="Discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="CPU Uso", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="Memória Uso", value=f"{memory_usage}%", inline=True)
        embed.add_field(name="Sistema Operacional", value=os_info, inline=True)
        embed.add_field(name="Latência", value=f"{latency} ms", inline=True)

        embed.set_footer(text=f"Requisitado por {ctx.author.display_name}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))