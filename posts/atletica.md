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

Uma observação antes: me afastei da atlética e hoje não acompanho mais o andamento do site. O texto abaixo descreve o projeto até a minha saída.

Uma atlética universitária vende bastante coisa: camisa, caneca, ingresso de festa, kit de calouro. Na maioria delas a venda acontece por um post no Instagram com a foto do produto, um formulário para o pedido e uma planilha compartilhada em que alguém da diretoria anota quantas camisas M ainda restam.

O arranjo aguenta até duas pessoas reservarem a última peça no mesmo minuto. Aí alguém precisa escrever para uma delas, pedir desculpas e cancelar o pedido, e a planilha continua sem saber por que aquilo aconteceu.

## O que eu fiz

Um site com três partes. A página institucional da atlética, o catálogo em que o aluno reserva e o painel em que a diretoria cuida do estoque.

A pilha é simples de propósito: Flask com Jinja para as páginas, HTMX para as partes que respondem sem recarregar, PostgreSQL para os dados e tudo em Docker. Sem framework de frontend. Sem build.

## Como funciona

O HTMX é a escolha central.

Um catálogo com reserva tem umas cinco interações que não deveriam recarregar a página: trocar o tamanho, mudar a quantidade, ver o preço atualizar, reservar sem perder a posição da rolagem. O caminho mais comum hoje seria um frontend em React ou Svelte, o que traz uma API para alimentá-lo, um passo de build e o modelo de dados duplicado nos dois lados.

Com HTMX o servidor continua devolvendo HTML e o navegador troca apenas o trecho que mudou, de modo que o modelo de dados fica num lugar só e o mesmo template Jinja que monta a página inteira também monta o fragmento. Para um catálogo de dezenas de itens, mantido por uma diretoria que muda todo ano, isso pesa mais do que qualquer ganho de interface: o sistema precisa continuar compreensível depois que quem o escreveu se formar.

## O que aprendi

Pouco depois de eu mudar a grade de produtos para três por três, um usuário mandou um print com o layout antigo. Estranhei. Eu tinha feito o deploy, conferido na minha máquina, e o CSS no servidor já era o novo.

O template carregava a folha de estilo com um `?v=` fixo, escrito à mão, e eu alterei o CSS sem mexer nesse número. Para o navegador dele o endereço era o mesmo do dia anterior, então não havia motivo para baixar o arquivo de novo. O servidor estava certo e a tela, errada. Toda verificação feita do meu lado dava certo.

Desde então, para mim, entregue é o que aparece na tela de quem usa, num navegador que já visitou o site antes. Mexer no CSS e subir a versão virou uma edição só.

## Resultados

- Site institucional, catálogo com reservas e painel de estoque no ar em `atleticaibmecbh.com.br`, atendendo os alunos do Ibmec BH.
- Reserva com controle de estoque no banco, o que acaba com a dupla reserva do mesmo item que a planilha permitia.
- Nenhuma dependência de frontend e nenhum passo de build, com o mesmo template servindo a página completa e o fragmento.
- Roda em contêiner na mesma máquina de outros dois sistemas de entidades acadêmicas, dividindo o custo de infraestrutura.
