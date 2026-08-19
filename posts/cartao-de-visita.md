---
slug: cartao-de-visita
titulo: Cartão de visita sem framework
sub: Um quarto de chalé pixelado em primeira pessoa, zero dependência
data: 2026-05-03
stack: [HTML5, CSS3, JavaScript, Vanilla]
competencias: [frontend, acessibilidade, design de interação]
repo: https://github.com/joshazze/ibtech-projeto01-joshua
---

## Contexto

O enunciado era um cartão de visita pessoal em HTML, CSS e JavaScript puros. Sem framework, sem build.

Cartão de visita pessoal é o gênero mais gasto da web. Foto redonda, nome grande, três parágrafos sobre paixão por tecnologia, ícones de rede social no rodapé. Todo mundo faz o mesmo, e o resultado é uma página que ninguém lembra dez segundos depois de fechar.

Eu queria a restrição, não o gênero. Sem framework não é limitação quando a página inteira cabe em três arquivos.

## O que eu fiz

A página é um quarto de chalé pixelado, e você está dentro dele, olhando para a parede.

Cada seção é uma parte do quarto, e cada parte carrega uma informação que num cartão de visita comum seria um bloco de texto:

- **A janela** tem a vista das montanhas e a frase de apresentação, que rotaciona.
- **A mesa de estudos** tem um monitor com um terminal rodando `whoami`, e é ali que ficam o sobre e as competências.
- **O mural de cortiça** tem três polaroides, três frases emolduradas e uma TV de tubo.
- **A prateleira** tem treze livros, um por marco, e o troféu.
- **A mesa de cabeceira** tem luminária, um despertador que marca a hora de verdade, e o contato com botão de copiar.

A estética é de jogo pixelado, com cor chapada, sombra sólida e uma fonte só na página inteira. O ponto de vista é o que faz a peça funcionar: não é um portfólio sobre alguém, é o quarto de alguém, e você entrou.

## Como funciona

Três decisões técnicas seguram tudo.

Os dois temas, dia e noite, trocam **apenas variáveis CSS na raiz**. Nenhuma regra é reescrita, nenhuma classe é adicionada em elemento nenhum: o botão troca o valor de uma dúzia de variáveis e a página inteira muda junto, incluindo as sombras. A preferência fica no `localStorage` e a primeira visita respeita o `prefers-color-scheme` do sistema.

A animação de entrada usa `IntersectionObserver`, não escuta de rolagem. Cada seção ganha a classe de visível uma única vez, quando entra na tela, e o observador para de observar aquela seção. Escutar `scroll` dispara centenas de vezes por segundo para fazer a mesma conta que o navegador já faz de graça.

E o modal é o `<dialog>` nativo com `showModal()`, o que traz de brinde o foco preso dentro dele, o fechar no Escape e o fundo inerte. Reimplementar isso à mão é onde a maioria dos cartões de visita quebra a navegação por teclado.

## O que aprendi

Foram 237 commits num único dia.

Não é orgulho, é diagnóstico. Aquilo é o número de vezes que eu mudei um valor, olhei, e mudei de novo, porque pixel art depende de decisões que você não consegue prever no papel: a sombra tem dois ou três pixels, a paleta aguenta o tema noite sem virar borrão, o livro na prateleira lê como livro ou como retângulo colorido. Trabalho visual não se planeja, se itera olhando, e o ciclo tem que custar quase nada para o processo funcionar.

O que tornou o ciclo barato foi exatamente a ausência de build. Salvar o arquivo e apertar F5 é instantâneo. Com um empacotador no meio, mesmo rápido, cada uma daquelas 237 iterações teria custado alguns segundos e alguma dúvida sobre se o que eu vejo é a versão nova. Multiplicado por 237, a ferramenta que existe para acelerar teria me atrasado.

Não usar framework não foi obediência ao enunciado. Foi o que fez a peça ficar boa.

## Resultados

- Página no ar no GitHub Pages, com repositório público.
- Zero dependência: nada de Bootstrap, Tailwind, jQuery, React, Vue ou Svelte. Uma única fonte externa na página toda.
- HTML semântico com marcação de rede social configurada, `<dialog>` nativo para o modal e navegação por teclado funcionando sem código extra.
- Dois temas completos com a troca de uma dúzia de variáveis CSS, respeitando a preferência do sistema na primeira visita.
- Cinco seções, treze marcos na prateleira e um despertador que marca a hora certa.
