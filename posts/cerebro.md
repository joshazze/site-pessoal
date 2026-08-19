---
slug: cerebro
titulo: Cérebro
sub: Memória permanente para assistente de IA, com o custo de contexto medido
data: 2026-08-09
stack: [Bash, jq, Obsidian, Markdown]
competencias: [arquitetura, análise de grafos, medição de desempenho, documentação]
repo: https://github.com/joshazze/cerebro-claude
---

## Contexto

Seu assistente esquece tudo quando a sessão fecha. Amanhã ele não sabe qual decisão foi tomada hoje, qual erro já custou três horas de depuração, nem que você detesta responder duas vezes a mesma pergunta.

A saída óbvia é escrever um arquivo de instruções. Funciona por uma semana. Depois o arquivo tem trinta mil bytes, e aí você descobre a parte cara: o que entra no início da sessão é reenviado em cada turno. Você não paga uma vez por aquele arquivo. Você paga por ele em toda mensagem que trocar até fechar a janela.

Foi o que aconteceu comigo. A primeira versão do meu cérebro despejava conteúdo, e custava 426 KB por sessão. Todo turno.

## O que eu fiz

Troquei conteúdo por endereço.

O acervo virou um vault de markdown organizado como grafo, uma nota por assunto, com wikilinks ligando o que se relaciona. O que entra na sessão não é o acervo, é um índice que entrega **caminhos, não conteúdo**: uma linha por arquivo, dizendo do que ele trata e onde está. O assistente lê o índice, decide o que interessa para a conversa de hoje, e abre só aquilo.

A manutenção do grafo (quem cita quem, quais notas viraram centro por acumular backlinks, quanto custou a última sessão) roda em shell, antes do primeiro prompt. Zero token gasto para manter a casa arrumada.

## Como funciona

O índice é o produto inteiro, e ele tem um orçamento. Cada linha precisa ser específica o suficiente para o assistente decidir se abre o arquivo, e curta o suficiente para caber. É uma restrição de compressão com uma métrica óbvia: quantos saltos o assistente precisa dar para chegar da porta de entrada até a informação.

Num vault de 183 notas em produção, o grafo tem caminho médio de 2,70 saltos entre duas notas quaisquer, e 97% do acervo está a dois saltos do índice. Isso não é enfeite de relatório: é a garantia de que abrir um arquivo quase sempre resolve, e abrir dois sempre resolve.

A manutenção tem seu próprio número. O laço ingênuo que descobre backlinks comparando cada nota com todas as outras levava 1,9 segundo em 260 notas. A versão que lê só o corpo e indexa uma vez leva 20 milissegundos.

Um instalador separado monta tudo em dez a quinze minutos: você cola um link no assistente, ele pergunta cinco coisas numa mensagem só (onde fica o vault, seu nome, sua stack em uma linha, se quer registro de gasto, se estuda), instala as camadas, verifica e termina explicando o que você digita amanhã.

## O que aprendi

Memória de assistente é problema de orçamento, não de armazenamento.

Guardar é barato e sempre foi. Markdown em disco não custa nada, e a tentação é guardar tudo e mandar tudo, porque tudo pode ser útil. O que custa é o que você reenvia, e reenviar é justamente o que a arquitetura ingênua faz por padrão, em silêncio, em todo turno. A conta só aparece no fim do mês.

Quando eu tratei isso como orçamento, a pergunta mudou de "o que o assistente precisa saber" para "o que cabe em mil tokens fixos, e como o resto fica alcançável". As duas perguntas têm respostas completamente diferentes, e só a segunda escala.

A outra lição foi sobre medir. Eu podia ter escrito que a arquitetura é eficiente, e ninguém ia conferir. Medir o caminho médio no grafo, o alcance em dois saltos e o tempo da manutenção transformou opinião em número, e o número é o que sobrevive quando outra pessoa avalia se vale a pena adotar. Escrevi trinta e uma páginas de método e figuras por isso.

## Resultados

- Custo fixo por sessão caiu de **426 KB para 4,3 KB**, cerca de 1.100 tokens, com o acervo inteiro continuando alcançável.
- Caminho médio de **2,70 saltos** no grafo, com **97%** do acervo a dois saltos do índice.
- Manutenção do grafo de **1,9 s para 20 ms** em 260 notas, e custo zero em tokens porque roda em shell.
- Medido num vault real de **183 notas** em uso diário, não num exemplo de brinquedo.
- Documento de teoria com 31 páginas, mais um instalador que monta o sistema inteiro em dez a quinze minutos.
