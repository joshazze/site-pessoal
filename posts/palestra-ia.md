---
slug: palestra-ia
titulo: Palestra de IA aplicada
sub: 40 minutos para calouros de engenharia, com deck só de imagens e prática ao vivo no terminal
data: 2026-08-23
stack: [HTML, SVG, Chrome headless, Claude Code]
competencias: [comunicação, didática, pesquisa de fontes, design de apresentação]
areas: [IA aplicada, Educação, Liderança e ligas]
---

## Contexto

Em 20 de agosto de 2026 dei uma palestra de 40 minutos sobre IA aplicada para calouros de engenharia e membros das ligas IbTech e IbBot. Boa parte da plateia já usava ferramentas de IA, mas tinha pouca noção de como elas funcionam e do que é possível construir com elas.

Eu queria uma ideia central que fosse simples sem ser simplista. Escolhi esta: um modelo de linguagem é, em escala industrial, o experimento que Claude Shannon fez em 1948 com papel e lápis. A pergunta continua a mesma desde então, qual é o próximo pedaço de texto.

## O que eu fiz

Dez minutos de história, vinte e seis de terminal, quatro de perguntas.

A parte histórica tem 16 slides sem texto, com fotos de Shannon, Turing, Asimov, o Colossus, o ENIAC e suas programadoras, McCarthy, Minsky, o Deep Blue e Hinton, além de páginas renderizadas dos artigos originais de Turing e Shannon. O conteúdo vem da fala. Para não depender de memória, preparei um guia de narração de cinco páginas, com a frase a dizer em cada foto, e uma cola de duas páginas com o relógio minuto a minuto.

A prática tinha cinco demonstrações. Primeiro, um sistema de memória para o assistente. Depois, a criação de um agente ao vivo, para mostrar que ele é basicamente um arquivo de texto. Uma conversa em que vários agentes discordam entre si. Um desenho para corte a laser. E, por último, uma tarefa sugerida pela própria plateia, a única parte que ninguém poderia dizer que foi ensaiada.

## Como funciona

O deck é um único arquivo HTML, gerado por um script que percorre a pasta de imagens, embute todas em base64 e produz um arquivo que roda sem internet, num projetor qualquer, sem depender do Wi-Fi do auditório. Cada foto aparece inteira sobre um fundo desfocado dela mesma, para caber em qualquer proporção de tela.

O slide sobre modelos de difusão não usa nenhuma imagem externa. Ele mostra, em cinco quadros, ruído se transformando em imagem, feito só com filtros SVG.

O penúltimo slide tem dois QR codes para os repositórios que mostrei. Antes da palestra, conferi os dois lendo cada código com o leitor de imagem do sistema. No final voltei para esse slide e o deixei na tela durante as perguntas.

## O que aprendi

Conferi cada data e cada número na fonte. Fiz isso porque, meses antes, uma auditoria no meu artigo de iniciação científica encontrou uma referência que não existia. Para a palestra, montei um dossiê de 14 páginas com as fontes de cada número, vinte perguntas difíceis com resposta e dez mitos comuns sobre IA que eu não deveria repetir.

As fotos também exigiram cuidado. Seis delas têm licença Creative Commons e exigem atribuição, então todas as imagens levam crédito no canto do slide, mesmo as de domínio público.

Também aprendi a cortar. Antes da versão final houve uma de 33 slides teóricos e outra de 13 com tópicos escritos. Tirei o texto da tela. Assim a atenção fica em quem fala.

## Resultados

- Palestra de 40 minutos dada em 20 de agosto de 2026 para calouros de engenharia e membros de duas ligas.
- Deck de 16 slides num único HTML que funciona sem internet, mais um guia de narração de 5 páginas, uma cola de 2 páginas e um dossiê de 14 páginas.
- Todos os números com fonte conferida, entre eles o AlexNet a 15,3% de erro contra 26,2% do segundo colocado em 2012 e o ChatGPT chegando a 1 milhão de usuários em 5 dias.
- Material reaproveitável: atualizar o deck é editar um modelo e rodar um script.
