const fs = require('fs');
const path = require('path');
const Owners = require('../../../Schemas/owners');
const emoji = require('../../emoji.json');

module.exports = {
    name: 'cmd-criar',
    aliases: ['cmdcreate', 'criarcomando'],
    description: '➕ Cria um novo comando manualmente e salva na pasta commands/repo.',

    run: async ({ client, message }) => {
        // Verifica se é owner
        const donoDb = await Owners.findOne({ userId: message.author.id });
        if (!donoDb) {
            return message.reply(`${emoji.escudo} | Apenas **donos** podem usar este comando.`);
        }

        const filtro = m => m.author.id === message.author.id;

        // Pergunta o nome do arquivo
        await message.reply(`${emoji.texto} | Envie o **nome do arquivo** (sem .js):`);
        const nomeColetor = await message.channel.awaitMessages({ filter: filtro, max: 1, time: 60000 }).catch(() => {});
        if (!nomeColetor || nomeColetor.size === 0) {
            return message.reply(`${emoji.tempo} | Tempo esgotado para enviar o nome do arquivo.`);
        }
        const nomeArquivo = nomeColetor.first().content.toLowerCase();

        // Verifica se já existe
        const pastaRepo = path.join(__dirname, '../repo');
        const arquivoComando = path.join(pastaRepo, `${nomeArquivo}.js`);
        if (!fs.existsSync(pastaRepo)) fs.mkdirSync(pastaRepo);
        if (fs.existsSync(arquivoComando)) {
            return message.reply(`${emoji.alerta_de_reacao} | O comando \`${nomeArquivo}\` já existe em \`commands/repo/${nomeArquivo}.js\`.`);
        }

        // Tenta mandar DM para o usuário
        let dmChannel;
        try {
            dmChannel = await message.author.createDM();
            await dmChannel.send(`${emoji.codigo} | Agora envie o **código completo** do comando (em formato \`\`\`js ...\`\`\`):`);
        } catch (err) {
            return message.reply(`${emoji.erro} | Não consegui enviar mensagem no seu PV. Verifique se está habilitado.`);
        }

        // Coleta o código no PV
        const codigoColetor = await dmChannel.awaitMessages({ filter: filtro, max: 1, time: 300000 }).catch(() => {});
        if (!codigoColetor || codigoColetor.size === 0) {
            return dmChannel.send(`${emoji.tempo} | Tempo esgotado para enviar o código do comando.`);
        }
        const codigoComando = codigoColetor.first().content.replace(/```(js)?/g, '').trim();

        // Preview do código no canal público
        const previewEmbed = {
            title: `${emoji.codigo} Preview do Comando`,
            description: `\`\`\`js\n${codigoComando.substring(0, 1900)}\n\`\`\``,
            color: 0x00b0f4,
            footer: { text: `Confirme para salvar como ${nomeArquivo}.js` }
        };

        const previewMsg = await message.channel.send({ embeds: [previewEmbed] });
        await previewMsg.react('✅'); // Confirmar
        await previewMsg.react('❌'); // Cancelar

        const reacaoFiltro = (reaction, user) =>
            ['✅', '❌'].includes(reaction.emoji.name) && user.id === message.author.id;

        const reacaoColetor = previewMsg.createReactionCollector({ filter: reacaoFiltro, max: 1, time: 60000 });

        reacaoColetor.on('collect', async (reaction) => {
            if (reaction.emoji.name === '✅') {
                fs.writeFileSync(arquivoComando, codigoComando);
                await message.channel.send(`${emoji.reaction_success} | Comando salvo com sucesso em \`commands/repo/${nomeArquivo}.js\`.`);
            } else {
                await message.channel.send(`${emoji.parar} | Criação de comando cancelada.`);
            }
        });

        reacaoColetor.on('end', (_, reason) => {
            if (reason === 'time') {
                message.channel.send(`${emoji.tempo} | Tempo esgotado para confirmar a criação do comando.`);
            }
        });
    }
};