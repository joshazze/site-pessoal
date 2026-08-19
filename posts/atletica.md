---
slug: atletica
titulo: Atlética Ibmec BH
sub: Site institucional, catálogo com reservas e gestão de estoque
data: 2026-07-24
stack: [Flask, Jinja, HTMX, PostgreSQL, Docker]
competencias: [backend, produto, operação, entrega com prazo]
link: https://atleticaibmecbh.com.br
---

## Contexto

Atlética universitária vende. Camisa, caneca, ingresso de festa, kit de calouro. E vende do jeito que dá: um post no Instagram com a foto do produto, um formulário para o pedido, e uma planilha compartilhada onde alguém da diretoria tenta lembrar quantas camisas tamanho M ainda existem.

Isso funciona até o dia em que duas pessoas reservam a última peça ao mesmo tempo. Aí o problema deixa de ser de software e vira de constrangimento, porque alguém precisa mandar mensagem cancelando.

## O que eu fiz

Um site que faz as três coisas de uma vez: a página institucional que apresenta a atlética, o catálogo em que o aluno reserva, e o painel em que a diretoria administra o que existe em estoque.

A pilha é deliberadamente sem graça. Flask com Jinja para as páginas, HTMX para as partes que precisam responder sem recarregar, PostgreSQL para os dados, tudo em Docker. Sem framework de frontend, sem processo de build de JavaScript, sem camada de API separada do servidor que renderiza.

## Como funciona

HTMX é a escolha que carrega o projeto, e ela merece explicação porque é contraintuitiva em 2026.

Um catálogo com reserva precisa de umas cinco interações que não podem recarregar a página: mudar o tamanho selecionado, atualizar a quantidade, ver o preço mudar, reservar sem perder a rolagem. A resposta padrão hoje é montar um frontend em React ou Svelte, o que traz junto uma API para servir aquele frontend, um build, e a duplicação do modelo de dados nos dois lados.

Com HTMX o servidor continua devolvendo HTML e o navegador troca só o pedaço que mudou. O modelo de dados vive num lugar só, o Jinja que já renderiza a página também renderiza o fragmento, e não existe passo de build para quebrar. Para um catálogo de dezenas de itens mantido por uma diretoria que troca todo ano, isso é o que decide se o sistema sobrevive à formatura de quem escreveu.

## O que aprendi

O usuário mandou um print e escreveu "GRID CARALHO".

Eu tinha acabado de mudar a grade de produtos para três por três, deployado, conferido na máquina, e estava tudo certo. O CSS no servidor era o novo. E o navegador dele insistia em mostrar o layout antigo.

O template linka o CSS com um `?v=` fixo, escrito à mão, e eu tinha alterado a folha de estilo sem tocar naquele número. Do ponto de vista do navegador, o endereço era idêntico ao de ontem, então não havia motivo nenhum para baixar de novo. O arquivo estava correto no servidor e errado na tela, que é a pior combinação possível para depurar, porque tudo o que você verifica dá certo.

A lição não é sobre cache, é sobre onde a verificação termina. Eu tinha conferido o deploy e chamado aquilo de pronto. Deploy conferido no servidor não é mudança entregue: entregue é o que aparece na tela de quem usa, num navegador que já esteve ali antes. Desde então, mexer em CSS e bumpar a versão do asset é uma edição só, nunca duas.

E o print continua sendo o relatório de bug mais eficiente que eu já recebi.

## Resultados

- Site institucional, catálogo com reservas e painel de estoque no ar em `atleticaibmecbh.com.br`, servindo o corpo discente do Ibmec BH.
- Reserva com controle de estoque no banco, o que elimina a dupla reserva do mesmo item que a planilha compartilhada permitia.
- Zero dependência de frontend e zero passo de build, com o mesmo template servindo página completa e fragmento.
- Roda em contêiner na mesma máquina que hospeda outros dois sistemas das entidades acadêmicas, dividindo custo de infraestrutura.
