import discord
from discord.ext import commands
from discord.ui import View, Button

class Help(commands.Cog):
    def __init__(self, bot, comandos_str):
        self.bot = bot
        self.comandos = [cmd.strip() for cmd in comandos_str.split(",") if cmd.strip()]
        self.comandos_por_pagina = 8

    def gerar_embed(self, pagina):
        total_paginas = (len(self.comandos) + self.comandos_por_pagina - 1) // self.comandos_por_pagina
        inicio = (pagina - 1) * self.comandos_por_pagina
        fim = inicio + self.comandos_por_pagina
        cmds_pagina = self.comandos[inicio:fim]
        comandos_formatados = "\n".join(f"• `{cmd}`" for cmd in cmds_pagina)

        embed = discord.Embed(
            title=f"📜 Lista de Comandos - Página {pagina}/{total_paginas}",
            description=comandos_formatados,
            color=discord.Color.blue()
        )
        return embed

    @commands.command(name="help")
    async def help_command(self, ctx):
        pagina = 1
        total_paginas = (len(self.comandos) + self.comandos_por_pagina - 1) // self.comandos_por_pagina
        embed = self.gerar_embed(pagina)

        view = HelpButtons(self, pagina, total_paginas)
        await ctx.send(embed=embed, view=view)


class HelpButtons(View):
    def __init__(self, help_cog, pagina_atual, total_paginas):
        super().__init__(timeout=60)
        self.help_cog = help_cog
        self.pagina_atual = pagina_atual
        self.total_paginas = total_paginas

        self.atualizar_botoes()

    def atualizar_botoes(self):
        self.clear_items()

        if self.pagina_atual > 1:
            self.add_item(Button(label="⬅️ Anterior", style=discord.ButtonStyle.primary, custom_id="anterior"))
        if self.pagina_atual < self.total_paginas:
            self.add_item(Button(label="Próxima ➡️", style=discord.ButtonStyle.primary, custom_id="proxima"))

    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.primary, custom_id="anterior", row=0)
    async def anterior(self, interaction: discord.Interaction, button: Button):
        self.pagina_atual -= 1
        embed = self.help_cog.gerar_embed(self.pagina_atual)
        self.atualizar_botoes()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Próxima", style=discord.ButtonStyle.primary, custom_id="proxima", row=0)
    async def proxima(self, interaction: discord.Interaction, button: Button):
        self.pagina_atual += 1
        embed = self.help_cog.gerar_embed(self.pagina_atual)
        self.atualizar_botoes()
        await interaction.response.edit_message(embed=embed, view=self)


async def setup(bot):
    comandos = "trabalhar, jobs, ping, help, userinfo, avatar, serverinfo, sorteio, futuro, conselho, botinfo, daily, sacar, depositar, rank, coinflip, 8ball, piada"
    await bot.add_cog(Help(bot, comandos))