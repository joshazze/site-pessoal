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

Quem usa um assistente de IA com frequência acumula instruções. "Escreva sem travessão." "Quando eu estiver estudando, não me dê a resposta pronta." "Reorganize minhas notas sem perder informação."

Reunidas num único arquivo grande, essas regras entram em conflito e perdem força. A regra de estudo aparece no trabalho de produção, e o assistente se recusa a escrever um código que precisa ser entregue. A de voz some depois de vinte mil tokens. E o arquivo cresce até custar trinta mil bytes de instrução em cada turno.

A questão central é de isolamento e persistência. Regras de estudo e de produção não deveriam estar ativas ao mesmo tempo, uma regra de voz precisa durar a conversa inteira, e uma palavra de segurança precisa funcionar como um estado do sistema, não como um pedido gentil.

## O que eu fiz

Fernando Pessoa não usava pseudônimos. Usava heterônimos: autores completos e distintos, cada um com biografia, estética e visão de mundo próprias, convivendo na mesma pessoa. Caeiro era o mestre bucólico, Reis o classicista estoico, Campos o modernista intenso. Pessoa assinava por si.

![Fernando Pessoa por volta de 1915](/img/fernando-pessoa/pessoa-1915.jpg) ![Fernando Pessoa no Abel Pereira, 1929](/img/fernando-pessoa/pessoa-1929.jpg)

*Fernando Pessoa por volta de 1915 e no Abel Pereira, em 1929. Fotos: acervo da [Casa Fernando Pessoa](https://casafernandopessoa.pt/en/fernando-pessoa).*

Apliquei essa estrutura a um assistente. Em vez de um prompt único tentando dar conta de tudo, há um ortônimo (o assistente padrão) que aciona heterônimos: personas estreitas, cada uma dedicada a uma tarefa, com voz e regras próprias. O ortônimo escolhe qual chamar.

![Marcus, Rogi e Stefano](/img/fernando-pessoa/heteronimos.svg)

*Os heterônimos que mais uso, com o gatilho e a camada de persistência de cada um.*

## Como funciona

A metáfora ajuda a explicar, mas a contribuição está na arquitetura de persistência, que tem três camadas:

- **Definição**: um bloco carregado em toda sessão, com a especificação da persona.
- **Hook**: um script disparado por evento, que pode reforçar a persona a cada turno ou interceptar uma ação antes que ela aconteça.
- **Memória**: um arquivo que dura entre sessões e volta quando o assunto aparece.

A regra que organiza tudo é que **o gatilho define a camada**.

![As três camadas de persistência](/img/fernando-pessoa/camadas-persona.svg)

*As três camadas de persistência de uma persona e a escala de tempo em que cada uma age.*

Uma persona chamada pelo nome precisa só da primeira camada, porque quem chama já fornece o contexto. Uma persona ambiente, que deve ficar ativa o tempo todo, precisa de um hook que a reforce a cada turno; sem isso ela se dilui em conversas longas e a voz muda sem que ninguém tenha pedido. Já uma persona de guarda, que existe para impedir uma ação, não pode depender de instrução. Ela precisa de um hook que intercepte a chamada da ferramenta e a recuse, porque uma persona escrita em texto ainda pode ser convencida.

Os quatro heterônimos do repositório cobrem os três casos. O Marcus transforma material bruto em nota de vault sem perder informação e é chamado pelo nome. O Rogi cuida da escrita e usa as três camadas. O Stefano ensina sem resolver, com uma guarda que bloqueia a escrita do arquivo de exercício. O quarto é uma palavra de segurança.

## O que aprendi

Persona ambiente sem hook não dura.

Descobri isso testando: escrevi a especificação de voz, coloquei no arquivo carregado em toda sessão e funcionou bem por dez turnos. No turno quarenta, com o contexto cheio de código e logs, a voz tinha desaparecido. A instrução continuava presente, mas disputava atenção com tudo o que entrou depois dela, e uma instrução dada só no início da sessão vai perdendo força conforme a conversa cresce.

A segunda lição foi sobre a persona de guarda. Uma persona que precisa impedir uma ação não funciona como texto, por melhor que seja a redação, porque texto pode ser negociado. Um hook que intercepta a ferramenta e devolve erro é código rodando fora do modelo e não negocia. A persona explica o motivo. O hook garante o resultado.

## Resultados

- Framework público sob licença MIT, com instalador, registro de heterônimos e três modelos para criar os seus.
- Quatro heterônimos prontos, cobrindo os três modos de ativação: chamada pelo nome, persona ambiente e guarda que bloqueia ação.
- O repositório anterior de um dos agentes foi incorporado ao framework como heterônimo de referência, e o antigo foi arquivado como somente leitura.
- Documentação com manifesto e arquivo de citação, para que o método possa ser referenciado.
