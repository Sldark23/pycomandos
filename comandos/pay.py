import discord
from discord.ext import commands
import asyncio
from estruturadb import get_saldo, atualizar_saldo

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pay(self, ctx, destinatario: discord.Member, valor: int):
        pagador = ctx.author
        if valor <= 0:
            return await ctx.send("❌ O valor precisa ser maior que zero.")

        saldo_pagador = get_saldo(pagador.id)
        if saldo_pagador < valor:
            return await ctx.send(f"❌ Você não tem saldo suficiente. Seu saldo atual é {saldo_pagador} LC$.")

        if destinatario.bot:
            return await ctx.send("❌ Não é possível pagar um bot.")

        if destinatario == pagador:
            return await ctx.send("❌ Você não pode pagar para si mesmo.")

        msg_dest = await ctx.send(
            f"{destinatario.mention}, você recebeu uma solicitação de pagamento de {pagador.mention} no valor de **{valor} LC$**.\n"
            "Reaja com ✅ para aceitar ou ❌ para recusar."
        )

        msg_pag = await ctx.send(
            f"{pagador.mention}, confirme o pagamento de **{valor} LC$** para {destinatario.mention}.\n"
            "Reaja com ✅ para confirmar ou ❌ para cancelar."
        )

        await msg_dest.add_reaction("✅")
        await msg_dest.add_reaction("❌")
        await msg_pag.add_reaction("✅")
        await msg_pag.add_reaction("❌")

        def check_dest(reaction, user):
            return user == destinatario and reaction.message.id == msg_dest.id and str(reaction.emoji) in ["✅", "❌"]

        def check_pag(reaction, user):
            return user == pagador and reaction.message.id == msg_pag.id and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction_dest, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check_dest)
            if str(reaction_dest.emoji) == "❌":
                return await ctx.send(f"❌ {destinatario.mention} recusou a solicitação de pagamento.")

            reaction_pag, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check_pag)
            if str(reaction_pag.emoji) == "❌":
                return await ctx.send(f"❌ {pagador.mention} cancelou o pagamento.")

            if str(reaction_dest.emoji) == "✅" and str(reaction_pag.emoji) == "✅":
                # Atualiza os saldos no banco
                atualizar_saldo(pagador.id, saldo_pagador - valor)
                saldo_dest = get_saldo(destinatario.id)
                atualizar_saldo(destinatario.id, saldo_dest + valor)

                await ctx.send(f"✅ Pagamento de **{valor} LC$** realizado com sucesso de {pagador.mention} para {destinatario.mention}!")

        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo para confirmação expirou. Pagamento cancelado.")

async def setup(bot):
    await bot.add_cog(Pay(bot))