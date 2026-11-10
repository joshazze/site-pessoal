---
slug: matriz-led
titulo: Matriz de LED endereçável
sub: 64 LEDs WS2812B num fio só, primeiro com biblioteca e depois escrevendo o sinal direto na porta do microcontrolador
data: 2026-11-09
stack: [C++, Arduino, AVR, WS2812B]
competencias: [sistemas embarcados, temporização, interrupções, protocolo de um fio]
areas: [Hardware e fabricação, Código aberto]
repo: https://github.com/joshazze/sei-pos-ap1
---

## Contexto

Depois do shield de sete segmentos, a disciplina de Sistemas Embarcados passou para uma matriz 8x8 de LEDs WS2812B. São 64 LEDs coloridos ligados em fila, e todos recebem os dados por um único fio, no pino 6 do Arduino Uno.

Cada LED lê os primeiros 24 bits que chegam, fica com eles e repassa o resto ao vizinho. Não existe fio de clock. O que separa um bit 0 de um bit 1 é quanto tempo o fio fica em nível alto, numa janela de 1,25 microssegundo.

## O que eu fiz

Comecei com a biblioteca Adafruit NeoPixel, para ver a matriz acender. Saíram quatro sketches: letras fixas, animações, uma letra escolhida pela serial e três desenhos escolhidos por tecla.

Depois escrevi o jogo da cobrinha sem biblioteca nenhuma. O sinal sai por escrita direta no registrador `PORTD`.

Publiquei os dez sketches do período num repositório aberto, para os colegas de turma. Todos compilam para o Uno.

## Como funciona

A função `digitalWrite` leva alguns microssegundos, mais que um bit inteiro do WS2812B. Escrever no registrador com `PORTD |= B01000000` vira uma instrução só, de 2 ciclos de clock. A 16 MHz, isso dá 125 nanossegundos.

Com essa unidade eu monto o bit contando instruções. O fio sobe e fica alto por três escritas. Na quarta, ele continua alto se o bit for 1 e desce se for 0. Depois desce de vez.

A matriz é ligada em serpentina: a linha par corre da esquerda para a direita, a ímpar volta. Uma função converte coluna e linha na posição da fila, invertendo o x nas linhas ímpares.

O jogo usa dois timers. O Timer2 lê a direção digitada a cada 10 ms. Já o passo da cobra fica com o Timer1, a cada 300 ms. O `loop()` não faz nada.

## O que aprendi

Uma interrupção no meio do envio estica um bit, e o LED entende outro valor. Por isso o envio inteiro roda com as interrupções desligadas. São 64 LEDs vezes 24 bits vezes 1,25 microssegundo: 1,92 ms de silêncio a cada quadro.

Esse número limita o resto. O Timer2 dispara a cada 10 ms, então o atraso de 1,92 ms cabe com folga. Num timer de 1 ms, eu perderia interrupções a cada quadro.

No Uno, os pinos 0 e 1 da mesma porta são o RX e o TX da serial. Escrever o byte inteiro no `PORTD` derrubaria a comunicação. A escrita com `|=` e `&=` mexe só no bit 6.

A cobrinha ainda não está pronta. Compila, mas falta a colisão com o próprio corpo, e a temporização manual ainda precisa ser conferida na matriz. Um curto no pino 6 parou os testes na bancada.

## Resultados

- Dez sketches publicados, todos compilando para o Arduino Uno.
- Cobrinha sem biblioteca em 3360 bytes de programa, 10% da memória do Uno.
- Escrita no pino em 125 ns, contra alguns microssegundos do `digitalWrite`.
- Quadro completo de 64 LEDs enviado em 1,92 ms.
