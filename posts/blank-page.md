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

O professor começou a falar e eu preciso despejar aquilo em algum lugar, agora.

Esse é o problema inteiro. No Obsidian, o caminho entre "preciso anotar isso" e "estou anotando" passa por criar a nota, decidir o nome, arrastar para a pasta certa e lembrar de marcar. São quatro decisões antes da primeira palavra, e são quatro decisões que acontecem exatamente quando a sua atenção deveria estar na aula.

A saída óbvia é um template. Só que template resolve o corpo da nota, não o caminho até ela: você ainda tem que abrir o seletor, achar o template e responder o modal.

## O que eu fiz

Um plugin que faz uma coisa. Um clique, e a nota já existe nomeada, arquivada e marcada.

Clique com o botão direito na pasta `Física` e sai `Física 2026-07-26.md` dentro dela. A mesma ação está na barra lateral, num comando que aceita atalho de teclado, e numa URI (`obsidian://blank-page?vault=...&profile=...`), o que permite um atalho global do sistema abrir o Obsidian direto numa nota nova, mesmo com o app fechado.

Tudo é perfil, então o plugin se dobra ao fluxo de quem usa em vez do contrário: pasta de destino, padrão de nome com marcadores, template curto, e uma agenda opcional no formato `mon 08:00-11:40 > Courses/Data Engineering`, que faz o perfil da aula ficar ativo sozinho no horário da aula.

## Como funciona

Duas decisões de desenho carregam o plugin.

A primeira é sequestrar o "Nova nota" nativo. Uma nota vazia criada dentro de uma pasta que pertence a um perfil recebe o nome e o template automaticamente. Não há nada novo para aprender, o gesto continua sendo o de sempre.

A segunda é a fila. Toda captura pode ser registrada num arquivo de entrada, uma linha por nota, e é isso que separa o material cru do material tratado. Depois, numa passada calma, você (ou um script, ou um agente) sabe exatamente o que ainda está por limpar. As linhas são wikilinks, então sobrevivem a renomear a nota, e a fila não apodrece.

E existe o caminho de volta, que quase todo sistema de captura esquece: um item no menu de qualquer nota devolve ela para a fila, tirando a tag de pronta, limpando as propriedades que a revisão escreveu e recolocando a linha no arquivo de entrada. Selecione dez notas no explorador e ele reabre as dez.

## O que aprendi

Templater e QuickAdd fazem isso. Os dois são excelentes, e os dois são maiores que este problema.

Essa frase está no README porque foi a decisão mais difícil do projeto. Templater é um motor de templates, QuickAdd é um sistema de macros. Com qualquer um deles você constrói o Blank Page inteiro, depois de aprender o motor. A pergunta que eu tive que responder é se existe espaço para uma ferramenta que faz um pedaço do que os grandes fazem e não pede estudo nenhum.

Existe, e o motivo é o momento de uso. Uma ferramenta que você configura no domingo pode exigir aprendizado. Uma ferramenta que você usa quando o professor já começou a falar não pode exigir nada. O custo de aprender uma linguagem de template não aparece no dia em que você aprende, aparece toda vez que você precisa mexer nela sob pressão.

Escopo pequeno defendido é funcionalidade, não limitação.

## Resultados

- Plugin publicado em repositório público sob licença MIT, instalável por BRAT enquanto não entra na loja da comunidade.
- Cinco pontos de entrada para a mesma ação: menu de pasta, barra lateral, comando com atalho, URI de sistema e o "Nova nota" nativo sequestrado.
- Onze marcadores de nome disponíveis, entre data, hora, pasta, contador e título.
- A fila de captura fecha o ciclo nos dois sentidos, com reabertura em lote de várias notas ao mesmo tempo.
