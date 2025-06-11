import discord
from discord.ext import commands
import random

piadas = [
    "Por que o JavaScript foi ao médico? Porque estava se sentindo mal interpretado!",
    "O que o zero disse para o oito? Que cinto maneiro!",
    "Por que o computador foi preso? Porque executou um código suspeito.",
    "Como o programador se despede? 'Logout!'",
    "Por que o programador sempre confunde Halloween com Natal? Porque OCT 31 == DEC 25.",
    "Como se chama um boi que toca violão? Um **boi-lão**!",
    "O que o tomate disse para o outro? — Vamos ketchup!",
    "Qual é o contrário de papelada? Pá ruim!",
    "Qual o cúmulo da paciência? Esperar o Wi-Fi voltar sem reclamar.",
    "Por que o Python não pode mentir? Porque ele é muito ‘interpretable’!",
    "Como o músico chama o servidor lento? Buffering!",
    "Qual é o animal mais antigo? A zebra, porque ela está em preto e branco.",
    "Por que o livro de matemática se suicidou? Porque tinha muitos problemas.",
    "O que o computador come no café da manhã? Cookies.",
    "Como o hacker se refresca? Com um ‘cooler’.",
    "Por que o pato atravessou a estrada? Para mostrar que ele tinha coragem.",
    "O que o peixe disse quando bateu na parede? ‘Droga!’",
    "Por que o morcego se deu mal na escola? Porque era um pouco ‘bat-man’.",
    "O que o chão falou para a mesa? ‘Você é de dar apoio!’",
    "Qual o cúmulo da inteligência? Colocar alarme para desligar o alarme.",
    "Por que o computador foi ao dentista? Para tirar o vírus.",
    "O que o telefone disse para o Wi-Fi? Estamos conectados.",
    "Por que o astronauta não usa Facebook? Porque ele já tem muitos seguidores no espaço.",
    "O que o relógio disse para o relógio? Vamos dar um tempo.",
    "Qual o animal que gosta de se esconder? O camuflado.",
    "O que a vaca foi fazer no espaço? Procurar a Via Láctea.",
    "Por que o DJ foi preso? Porque ele fazia batidas ilegais.",
    "Qual é o melhor time para trabalhar? O time de futebol de mesa.",
    "O que o semáforo disse para o carro? Não me olhe, estou mudando.",
    "Por que o pão não se dá bem com o leite? Porque ele é pão-duro.",
    "Qual é a comida favorita dos programadores? Pizza, porque tem muitas fatias.",
    "O que o gato disse para o cachorro? Estou de olho em você.",
    "Por que a abelha sempre é promovida? Porque ela é muito dedicada.",
    "O que o lápis falou para a borracha? Você me completa.",
    "Por que o músico levou escada para o show? Para alcançar as notas altas.",
    "O que o sol falou para a lua? Você me ilumina à noite.",
    "Por que o coelho é sempre o mais rápido? Porque ele está sempre pulando.",
    "Qual é o cúmulo da loucura? Jogar xadrez com um pombo.",
    "Por que o livro estava triste? Porque tinha uma história triste.",
    "O que o vento falou para a árvore? Pare de balançar!",
    "Por que o peixe nunca perde uma briga? Porque ele tem escamas fortes.",
    "O que o cavalo disse para o carro? Você é muito rápido para mim.",
]

class Piada(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="piada", aliases=["piadas", "joke"])
    async def piada(self, ctx):
        piada_escolhida = random.choice(piada)
        await ctx.send(f"😂 {piada_escolhida}")

async def setup(bot):
    await bot.add_cog(Piada(bot))