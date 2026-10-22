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

O enunciado pedia um cartão de visita pessoal em HTML, CSS e JavaScript puros. Sem framework, sem build.

É um formato muito repetido na web: foto redonda, nome grande, alguns parágrafos sobre gostar de tecnologia e os ícones de rede social no rodapé, quase sempre na mesma ordem e com o mesmo peso visual. Fecha-se a aba e pouco fica.

Me interessou a restrição. Numa página que cabe em três arquivos, ficar sem framework quase não limita.

## O que eu fiz

A página é um quarto de chalé em pixel art, visto de dentro, de frente para a parede.

![A janela do quarto, tema de dia](/img/cartao-de-visita/dia.png)

*A janela, primeira seção da página.*

Cada seção é uma parte do quarto e guarda uma informação que num cartão comum seria um bloco de texto:

- **A janela** mostra as montanhas e uma frase de apresentação que vai mudando.
- **A mesa de estudos** tem um monitor com um terminal rodando `whoami`, onde ficam o sobre e as competências.
- **O mural de cortiça** tem três polaroides, três frases emolduradas e uma TV de tubo.
- **A prateleira** tem treze livros, um por marco, e o troféu.
- **A mesa de cabeceira** tem luminária, um despertador com a hora real e o contato com botão de copiar.

![A mesa de estudos](/img/cartao-de-visita/mesa.png)

*A mesa de estudos, com o sobre e as competências.*

![O mural de cortiça](/img/cartao-de-visita/mural.png)

*O mural de cortiça.*

![A prateleira com os treze livros](/img/cartao-de-visita/prateleira.png)

*A prateleira: um livro por marco.*

A estética é de jogo em pixel art, com cor chapada, sombra sólida e uma única fonte na página. O ponto de vista em primeira pessoa é o que sustenta a ideia: em vez de uma página sobre alguém, o visitante está no quarto dessa pessoa.

## Como funciona

Três decisões técnicas.

Os temas de dia e de noite trocam **apenas variáveis CSS na raiz**. Nenhuma regra é reescrita e nenhuma classe é adicionada aos elementos: o botão altera uma dúzia de variáveis e a página toda acompanha, sombras incluídas. A preferência fica no `localStorage`. Na primeira visita vale o tema do sistema.

![A prateleira no tema noturno](/img/cartao-de-visita/noite.png)

*A mesma prateleira no tema noturno. Só as variáveis da raiz mudaram.*

A animação de entrada usa `IntersectionObserver` em vez de escutar a rolagem. Cada seção recebe a classe de visível uma vez, quando aparece na tela, e o observador deixa de acompanhá-la. Escutar `scroll` repetiria o mesmo cálculo centenas de vezes por segundo, um trabalho que o navegador já faz por conta própria e de forma mais eficiente.

O modal é o `<dialog>` nativo com `showModal()`, que já traz o foco preso dentro dele, o fechamento pelo Esc e o fundo inerte. Feito à mão, isso costuma quebrar o teclado.

## O que aprendi

Foram 237 commits num único dia.

Pixel art depende de decisões difíceis de prever no papel: se a sombra tem dois ou três pixels, se a paleta continua legível no tema noturno, se o livro da prateleira parece um livro ou só um retângulo colorido. Trabalho visual se resolve olhando e ajustando. Cada volta precisa ser barata.

Sem build, ela era. Salvar e apertar F5 levava um instante. Com um empacotador no meio, cada uma das 237 iterações levaria alguns segundos e traria a dúvida sobre estar vendo a versão nova ou não. Dispensar o framework acabou ajudando a qualidade da página, além de cumprir o enunciado.

## Resultados

- Página no ar no GitHub Pages, com repositório público.
- Nenhuma dependência: sem Bootstrap, Tailwind, jQuery, React, Vue ou Svelte, e uma única fonte externa.
- HTML semântico, com metadados para redes sociais, `<dialog>` nativo no modal e navegação por teclado sem código extra.
- Dois temas completos trocando uma dúzia de variáveis CSS, com a preferência do sistema respeitada na primeira visita.
- Cinco seções, treze marcos na prateleira e um despertador que mostra a hora certa.
