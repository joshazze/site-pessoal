---
slug: blank-page
titulo: Blank Page
sub: Plugin do Obsidian que tira o atrito entre querer escrever e estar escrevendo
data: 2026-08-14
stack: [TypeScript, Obsidian API, esbuild]
competencias: [produto, ferramenta de autor, design de interação]
repo: https://github.com/joshazze/obsidian-blank-page
---

## Contexto

A aula começou e eu preciso anotar.

No Obsidian, entre querer anotar e estar anotando há alguns passos: criar a nota, escolher o nome, mover para a pasta certa e lembrar da tag. São quatro decisões antes da primeira palavra, tomadas justamente no momento em que a atenção deveria estar no professor.

Um template ajuda com o conteúdo da nota, mas não com o caminho até ela. Ainda é preciso abrir o seletor, encontrar o template e responder ao modal.

## O que eu fiz

Um plugin com uma única função: com um clique, a nota já existe com nome, pasta e tag.

Um clique com o botão direito na pasta `Física` cria `Física 2026-07-26.md` dentro dela. A mesma ação está na barra lateral, num comando que aceita atalho de teclado e numa URI (`obsidian://blank-page?vault=...&profile=...`), o que permite a um atalho global do sistema abrir o Obsidian já numa nota nova, mesmo com o app fechado.

Tudo é configurado por perfil, para que o plugin se adapte ao fluxo de quem usa: pasta de destino, padrão de nome com marcadores, template curto e uma agenda opcional no formato `mon 08:00-11:40 > Courses/Data Engineering`, que ativa sozinho o perfil da disciplina no horário da aula.

## Como funciona

Duas decisões de desenho.

A primeira é aproveitar o comando "Nova nota" nativo. Uma nota vazia criada numa pasta que pertence a um perfil recebe nome e template automaticamente, então não há gesto novo para aprender.

A segunda é a fila. Cada captura pode ser registrada num arquivo de entrada, uma linha por nota, separando o material cru do material já revisado. Mais tarde, com calma, quem revisa (uma pessoa, um script ou um agente) sabe exatamente o que falta. As linhas são wikilinks e continuam válidas quando a nota muda de nome.

Também existe o caminho inverso, que muitos sistemas de captura não oferecem. Um item no menu de qualquer nota a devolve para a fila: tira a tag de revisada, limpa as propriedades escritas na revisão e recoloca a linha no arquivo de entrada. Com dez notas selecionadas no explorador, as dez voltam juntas.

## O que aprendi

Templater e QuickAdd já resolvem esse problema, e o README diz isso logo no início. São ótimos plugins, e ambos são maiores do que a necessidade aqui.

Essa foi a decisão mais difícil do projeto. O Templater é um motor de templates e o QuickAdd é um sistema de macros; com qualquer um deles dá para montar o Blank Page inteiro, depois de aprender a ferramenta. A pergunta era se havia lugar para algo que faz só uma parte disso e não exige estudo.

Concluí que havia, por causa do momento de uso. Uma ferramenta configurada com tempo, num domingo, pode pedir algum aprendizado. Já uma ferramenta usada com a aula em andamento não deveria pedir nada, porque o custo de uma linguagem de template aparece toda vez que é preciso mexer nela com pressa. Manter o escopo pequeno foi uma escolha consciente.

## Resultados

- Plugin publicado em repositório público sob licença MIT, instalável pelo BRAT enquanto não entra na loja da comunidade.
- Cinco pontos de entrada para a mesma ação: menu de pasta, barra lateral, comando com atalho, URI do sistema e o "Nova nota" nativo.
- Onze marcadores de nome, entre data, hora, pasta, contador e título.
- Fila de captura nos dois sentidos, com reabertura de várias notas de uma vez.
