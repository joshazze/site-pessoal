---
slug: dino-vs-ia
titulo: Dino contra a máquina
sub: O jogo do dinossauro num display de 16 colunas, com um adversário automático calibrado para perder de vez em quando
data: 2026-06-05
stack: [C++, Arduino, LCD HD44780, Python]
competencias: [sistemas embarcados, simulação, aprendizado por reforço, design de jogo]
areas: [Hardware e fabricação, IA aplicada]
---

## Contexto

Foi meu primeiro projeto de hardware. Eu queria um jogo em que uma pessoa disputasse contra uma máquina num aparelho físico, e comecei pelo menor que cabia na bancada: o jogo do dinossauro do navegador, num display de caracteres de 16 colunas por 2 linhas, com um Arduino Uno.

Escolhi esse jogo porque ele é reflexo e pontuação. Jogo da velha tem solução conhecida, e a máquina nunca perde. Aqui existe tempo de reação, e dá para errar.

## O que eu fiz

A primeira versão era só para humano. O dinossauro corre numa coluna fixa, os cactos vêm da direita e um botão faz pular. O recorde fica gravado na memória permanente da placa e a pontuação sai pela serial.

Na segunda versão a partida virou disputa. A pessoa joga uma rodada, a máquina joga outra, e o display compara os dois placares.

Para acertar o adversário, escrevi um simulador do jogo em Python com a mesma mecânica do firmware: 16 colunas, pulo de 4 ticks, velocidade que cresce com a pontuação.

## Como funciona

O display aceita só 8 caracteres personalizados, de 5 por 8 pontos. Usei cinco: dois quadros do dinossauro correndo, um pulando e dois cactos.

O mundo é um vetor de 16 posições que rola uma casa para a esquerda a cada tick. O tick começa em 140 ms e encolhe até 70 ms.

O adversário não é uma rede neural. É uma regra: quando um cacto chega a 3 colunas de distância, ele pula. A cada cacto existe 3% de chance de ele vacilar e não pular.

## O que aprendi

Minha primeira regra pulava no último instante, com o cacto a uma coluna. No simulador, em 500 partidas, a mediana foi 31 pontos. Qualquer pessoa ganhava.

Troquei para pular com o cacto a 3 colunas e rodei de novo. As 500 partidas bateram no teto da simulação. Imortal. Um adversário que nunca perde é tão sem graça quanto um que perde sempre.

A dificuldade de um jogo não está em fazer a máquina jogar bem. Está em escolher quanto ela erra. Testei taxas de vacilo de 2% a 8% e fiquei com 3%, que dá mediana de 177 pontos: difícil, mas vencível.

Rodei também um aprendizado por reforço no simulador, 500 episódios partindo do zero. A pontuação média subiu de 41 para 285. Serviu para confirmar a regra. No Arduino continua indo a versão de duas linhas, que eu consigo explicar.

O hardware cobrou a parte dele. Com um teclado matricial ligado, o display passou a mostrar lixo: uma coluna do teclado dividia fio com o LCD. Voltei para um botão só.

## Resultados

- Mediana do adversário de 31 para 177 pontos, medida em 500 partidas simuladas por configuração.
- Seis taxas de erro testadas, de 2% a 8%, para escolher a dificuldade.
- Firmware de 202 linhas e simulador de 149.
- Tick do jogo de 140 ms no início e 70 ms no limite.
