---
slug: shield-arduino
titulo: Shield multifunção do Arduino
sub: Display de quatro dígitos, três botões e dois registradores de deslocamento, controlados por interrupção
data: 2026-10-27
stack: [C++, Arduino, AVR]
competencias: [sistemas embarcados, interrupções, multiplexação, depuração de hardware]
areas: [Hardware e fabricação]
---

## Contexto

Na disciplina de Sistemas Embarcados e Internet das Coisas, o laboratório usa um Arduino Uno com o shield multifunção HW 262 encaixado por cima. A placa junta num só lugar um display de sete segmentos com quatro dígitos, três botões, quatro LEDs, um buzzer e um potenciômetro.

O display não liga direto nos pinos do Arduino. Entre os dois ficam dois registradores de deslocamento 74HC595 em cascata, alcançados por três fios: latch no pino 4, clock no 7 e dado no 8. Só isso.

## O que eu fiz

Escrevi os sketches do semestre a partir do zero, sem a biblioteca pronta do shield, para entender o que cada bit faz.

Comecei pela função de envio. Cada atualização manda 16 bits, oito para os segmentos e oito para escolher o dígito. No display de ânodo comum, um segmento acende quando o bit dele vale 0, então o algarismo 0 é `B11000000` e o traço do sinal de menos é `B10111111`.

Depois veio uma tabela com os caracteres ASCII que cabem em sete segmentos e uma função que escreve texto no display. Com o Timer1 gerando uma interrupção a cada 300 ms, ela passou a animar a palavra CASA entrando e saindo pela lateral.

Por último, um contador: S1 soma, S2 subtrai, S3 zera. Vai de 999 negativo a 9999. Os LEDs e o buzzer, que ficam acesos ou apitando quando os pinos estão soltos, são desligados no início.

## Como funciona

Um dígito por vez. Uma interrupção do Timer1 dispara a cada 2 ms, apaga o display, acende o próximo dígito e lê os botões. A volta completa leva 8 ms, e o olho vê os quatro dígitos acesos ao mesmo tempo.

Apagar antes de trocar é o que impede o fantasma. Sem isso, durante os microssegundos da troca, os segmentos do dígito anterior aparecem fracos no vizinho, como riscos onde deveria estar vazio.

Na mesma interrupção entram os botões, e um aperto só conta depois de 25 leituras seguidas iguais, ou seja, 50 ms parado, e não conta de novo até o botão ser solto. Assim o contato que vibra ao ser apertado não vira dois ou três cliques.

Resultado: o `loop()` ficou vazio.

## O que aprendi

O contador parecia pular números: subia 1, 2, 3, 4 e depois mostrava 9. Tratei primeiro como vibração do botão e reforcei a filtragem, sem efeito.

A pista estava no padrão. Entre o 5 e o 9 a diferença é só o segmento de cima à direita, e entre o 6 e o 8 também. Se esse segmento ficar aceso o tempo todo, o 5 vira 9, o 6 vira 8, o traço do menos ganha uma perna vertical e os dígitos apagados mostram um risquinho. Era exatamente o que aparecia.

Um sketch de teste acendendo um segmento por segundo confirmou: defeito na placa, não no código. Resolvido o problema físico, a contagem ficou certa sem mudar uma linha do contador.

Quatro defeitos aparentemente diferentes, uma causa só. Hoje olho para o conjunto dos sintomas antes de mexer no código.

## Resultados

- Contador de 999 negativo a 9999 em 1640 bytes de programa, 5% da memória do Uno.
- Display e três botões atendidos por uma única interrupção de 2 ms, com o laço principal vazio.
- Filtro de 50 ms nos botões: um aperto gera exatamente uma contagem.
- Um teste de 8 segundos que separa defeito de placa de defeito de código.
