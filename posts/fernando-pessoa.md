---
slug: fernando-pessoa
titulo: Fernando Pessoa
sub: Um heterônimo para cada ferramenta: personas de IA que persistem e ativam sozinhas
data: 2026-08-11
stack: [Bash, hooks, Claude Code, Markdown]
competencias: [arquitetura de agentes, design de sistema, escrita técnica]
repo: https://github.com/joshazze/fernando-pessoa-agents
---

## Contexto

Quem usa um assistente de IA a sério acumula instrução. "Escreve sem travessão." "Quando eu estiver estudando, não me dá a resposta pronta." "Refatora minhas notas sem perder informação."

Despejadas no mesmo arquivo gigante, essas regras se contradizem e se diluem. A regra de estudo vaza no trabalho de produção e o assistente se recusa a escrever código que você precisa entregar. A regra de voz some depois de vinte mil tokens de conversa. E o arquivo cresce até você estar pagando por trinta mil bytes de instrução em cada turno de cada sessão.

O problema não é de conteúdo, é de isolamento e persistência. Uma regra de estudo e uma de produção nunca deveriam estar ligadas ao mesmo tempo. Uma regra de voz precisa sobreviver à conversa inteira. E uma palavra de segurança precisa ser um bit de estado, não uma sugestão simpática.

## O que eu fiz

Fernando Pessoa, o poeta, não escrevia com pseudônimo. Escrevia com heterônimo: autores inteiros e distintos, cada um com biografia, estética e visão de mundo próprias, coexistindo na mesma pessoa. Caeiro era o mestre bucólico, Reis o classicista estoico, Campos o modernista febril. Pessoa era o ortônimo que fingia todos.

Apliquei a estrutura a um assistente. Em vez de um prompt monolítico tentando ser bom em tudo, existe um ortônimo (o assistente conversacional padrão) que despacha heterônimos: personas estreitas, cada uma obcecada por uma tarefa só, com voz e regras próprias. O ortônimo não bate prego com a mão tendo vários martelos bonitos. Ele escolhe o martelo.

## Como funciona

A metáfora é a parte fácil e é a parte que não importa. A contribuição é a arquitetura de persistência, e ela tem três camadas:

- **Definição**: um bloco carregado toda sessão. É a especificação da persona, e está sempre presente.
- **Hook**: um script disparado por evento. Pode reforçar a persona a cada turno, ou interceptar uma ação antes de ela acontecer.
- **Memória**: um arquivo que sobrevive entre sessões e volta por recall quando o assunto aparece.

A regra que amarra tudo é esta: **o gatilho decide a camada**.

Uma persona convocada pelo nome precisa só da camada 1, porque quem chama já traz o contexto. Uma persona ambiente, que deve estar ligada o tempo todo, precisa de um hook que a lembre a cada turno, senão ela se dilui na conversa longa e você vê a voz mudando sem ninguém ter pedido. E uma persona de guarda, que existe para impedir uma ação, não pode ser instrução nenhuma: ela precisa de um hook que intercepte a chamada da ferramenta e negue, porque uma persona bem escrita ainda é uma persona persuadível.

Os quatro heterônimos do repositório cobrem os três casos de propósito. O Marcus refatora material cru em nota de vault sem perder informação e é chamado pelo nome. O Rogi é a voz de escrita e vive nas três camadas. O Stefano ensina e se recusa a resolver, com uma guarda que bloqueia a escrita do arquivo de exercício. O quarto é uma palavra de segurança.

## O que aprendi

Persona ambiente sem hook não existe.

Eu descobri isso da forma chata: escrevi a especificação de voz, coloquei no arquivo sempre carregado, testei, funcionou lindamente por dez turnos. No turno quarenta, com o contexto cheio de código e log, a voz tinha ido embora. A instrução continuava lá, tecnicamente presente, competindo por atenção com tudo que entrou depois.

Instrução no início da sessão não é uma regra, é uma sugestão que envelhece.

A segunda lição foi sobre a persona de guarda, e ela é mais desconfortável, porque toca no que uma persona é. Uma persona que precisa impedir você de fazer algo não pode ser escrita como texto, por melhor que o texto seja. Enquanto for texto, ela negocia. Um hook que intercepta a ferramenta e devolve erro não negocia, porque não é linguagem, é código rodando fora do modelo. A persona explica o porquê. O hook garante o quê.

## Resultados

- Framework público sob licença MIT, com instalador, registro de heterônimos e três modelos para escrever os seus.
- Quatro heterônimos prontos, cobrindo os três modos de ativação: convocação pelo nome, persona ambiente e guarda que bloqueia ação.
- O repositório anterior de um dos agentes foi absorvido pelo framework e virou o heterônimo de referência, com o repo antigo arquivado em somente leitura.
- Documentação com manifesto e arquivo de citação, para o método poder ser referenciado como método.
