---
slug: laser
titulo: Biblioteca de corte a laser
sub: Peças de acrílico geradas por código, com um portão de validação antes de cada arquivo de corte
data: 2026-09-19
stack: [Python, DXF, SVG, PDF]
competencias: [geometria computacional, fabricação digital, testes, desenho técnico]
areas: [Hardware e fabricação, Ferramentas de desenvolvedor]
---

## Contexto

Comecei a cortar peças de acrílico para os projetos da liga de robótica: uma base para robô, um berço para uma placa Arduino Mega, suportes e caixas. Desenhar cada peça à mão num programa de CAD funcionava para uma peça. Para várias versões da mesma peça, ficava lento e sujeito a erro.

A máquina disponível é uma cortadora a laser com mesa de 1150 por 1000 milímetros. Erro de medida custa chapa.

## O que eu fiz

Uma biblioteca em Python puro, sem dependências, em que cada peça é descrita num arquivo JSON com as medidas. O código gera os arquivos de corte em DXF, SVG e PDF, com cotas e uma tabela de medidas para conferência.

![Chapa de corte completa](/img/laser/chapa.png)

*Chapa completa, com a base e as peças avulsas encaixadas.*

A biblioteca tem módulos para geometria de polígonos, compensação de kerf, juntas (dedos, encaixe em T com bolso de porca, meia-madeira, rabo de andorinha, dobradiça viva e porca cativa em sanduíche), um registro de materiais que diferencia valor medido de valor estimado, um relatório de aproveitamento da chapa e um validador.

O validador é obrigatório. Nenhum arquivo vai para a máquina sem passar por `python3 -m laser validate`, que confere topologia, espessuras mínimas de ponte e se a peça cabe na mesa.

![Prancha cotada dos seis pinos](/img/laser/pinos-cotados.png)

*Prancha cotada gerada junto com o arquivo de corte.*

## Como funciona

O laser remove uma faixa fina de material, o kerf, e por isso a trajetória precisa ser deslocada em metade dessa largura. O sentido depende do papel do contorno: um contorno externo é deslocado para fora, para a peça não sair menor. Um furo é deslocado para dentro, porque o laser já alarga o vazio sozinho.

![Vista isométrica da base](/img/laser/base-3d.svg)

*A base em 3D, gerada da mesma especificação que produz o corte.*

Para calibrar, a biblioteca gera uma chapa de teste de 182 por 257 milímetros com pente de kerf, escada de folgas de 0,00 a 0,35 mm, bolsos para porcas M3, M4 e M5, pente de espessura, tiras de ponte e três padrões de dobradiça viva. Tudo vem rotulado. Corta-se uma vez, mede-se com paquímetro, e os valores medidos substituem os estimados no registro do material.

O kerf não resolve a outra pergunta de quem chega numa máquina nova: com qual velocidade e potência cada material corta e grava. As tabelas de fábrica são ponto de partida, e na máquina do laboratório a primeira chapa de MDF mostrou que ela corta mais fraco do que a tabela diz. Para isso a biblioteca ganhou um comando que escreve direto o projeto do LightBurn: uma chapa com a grade de gravação e a grade de corte lado a lado, cada quadrado com a sua velocidade e potência já preenchidas, rótulos nas linhas e colunas, material e data no canto, e uma borda de corte que sai por último para soltar a placa. Material novo é um JSON de dez linhas e um comando. No mesmo dia saíram matrizes de MDF, acrílico leitoso de 2 e 3 mm e papel paraná.

## O que aprendi

Ao transformar o código solto em biblioteca, encontrei um erro de sinal na compensação de kerf. O contorno externo estava certo, mas os furos, rasgos e polígonos eram deslocados no sentido errado. Na prática, um furo de 3,2 mm para parafuso M3 sairia com 3,5 mm na chapa. O erro só não custou material porque a compensação estava desligada em todas as especificações.

Havia mais. O deslocamento era feito por escala a partir do centro, o que num retângulo de 415 por 160 mm move as arestas longas bem menos que as curtas. Reescrevi o deslocamento e o conferi contra uma biblioteca de geometria de referência em 20 combinações de forma e distância.

A lição foi não confiar numa função geométrica só porque o resultado parece certo na tela. Hoje cada erro desse tipo tem um teste que o pega.

A matriz trouxe dois limites que eu não conhecia. O LightBurn tem 30 camadas, e cada quadrado da matriz gasta uma, então as duas grades somadas cabem em 28 quadrados e o gerador recusa o que passar disso. O segundo apareceu na pré-visualização: a origem dessa máquina fica no canto de trás à direita, e o texto saiu de cabeça para baixo. O desenho passou a sair girado 180 graus, e um teste falha se o giro sumir.

## Resultados

- 47 testes passando, incluindo verificação de largura máxima pela mesa da máquina e do giro da matriz.
- Compensação de kerf corrigida e conferida em 20 combinações: um furo de 4 mm sai desenhado com 3,85 mm, e um contorno de 415 mm sai com 415,15 mm.
- Seis tipos de junta e uma chapa de calibração gerada por um único comando.
- Arquivos de corte gerados a partir de JSON, sem desenho manual, de modo que corrigir uma cota é editar um número e gerar de novo.
- Matriz de calibração de 29 camadas, numa chapa de 124 por 104 milímetros, gerada para quatro materiais a partir de JSON.
