---
slug: laser
titulo: Biblioteca de corte a laser
sub: Peças de acrílico geradas por código, com um portão de validação antes de cada arquivo de corte
data: 2026-09-19
stack: [Python, DXF, SVG, PDF]
competencias: [geometria computacional, fabricação digital, testes, desenho técnico]
---

## Contexto

Comecei a cortar peças de acrílico para os projetos da liga de robótica: uma base para robô, um berço para uma placa Arduino Mega, suportes e caixas. Desenhar cada peça à mão num programa de CAD funcionava para uma peça. Para várias versões da mesma peça, ficava lento e sujeito a erro.

A máquina disponível é uma cortadora a laser com mesa de 1150 por 1000 milímetros. Erro de medida custa chapa.

## O que eu fiz

Uma biblioteca em Python puro, sem dependências, em que cada peça é descrita num arquivo JSON com as medidas. O código gera os arquivos de corte em DXF, SVG e PDF, com cotas e uma tabela de medidas para conferência.

A biblioteca tem módulos para geometria de polígonos, compensação de kerf, juntas (dedos, encaixe em T com bolso de porca, meia-madeira, rabo de andorinha, dobradiça viva e porca cativa em sanduíche), um registro de materiais que diferencia valor medido de valor estimado, um relatório de aproveitamento da chapa e um validador.

O validador é obrigatório. Nenhum arquivo vai para a máquina sem passar por `python3 -m laser validate`, que confere topologia, espessuras mínimas de ponte e se a peça cabe na mesa.

## Como funciona

O laser remove uma faixa fina de material, o kerf, e por isso a trajetória precisa ser deslocada em metade dessa largura. O sentido depende do papel do contorno: um contorno externo é deslocado para fora, para a peça não sair menor. Um furo é deslocado para dentro, porque o laser já alarga o vazio sozinho.

Para calibrar, a biblioteca gera uma chapa de teste de 182 por 257 milímetros com pente de kerf, escada de folgas de 0,00 a 0,35 mm, bolsos para porcas M3, M4 e M5, pente de espessura, tiras de ponte e três padrões de dobradiça viva. Tudo vem rotulado. Corta-se uma vez, mede-se com paquímetro, e os valores medidos substituem os estimados no registro do material.

## O que aprendi

Ao transformar o código solto em biblioteca, encontrei um erro de sinal na compensação de kerf. O contorno externo estava certo, mas os furos, rasgos e polígonos eram deslocados no sentido errado. Na prática, um furo de 3,2 mm para parafuso M3 sairia com 3,5 mm na chapa. O erro só não custou material porque a compensação estava desligada em todas as especificações.

Havia mais. O deslocamento era feito por escala a partir do centro, o que num retângulo de 415 por 160 mm move as arestas longas bem menos que as curtas. Reescrevi o deslocamento e o conferi contra uma biblioteca de geometria de referência em 20 combinações de forma e distância.

A lição foi não confiar numa função geométrica só porque o resultado parece certo na tela. Hoje cada erro desse tipo tem um teste que o pega.

## Resultados

- 42 testes passando, incluindo verificação de largura máxima pela mesa da máquina.
- Compensação de kerf corrigida e conferida em 20 combinações: um furo de 4 mm sai desenhado com 3,85 mm, e um contorno de 415 mm sai com 415,15 mm.
- Seis tipos de junta e uma chapa de calibração gerada por um único comando.
- Arquivos de corte gerados a partir de JSON, sem desenho manual, de modo que corrigir uma cota é editar um número e gerar de novo.
