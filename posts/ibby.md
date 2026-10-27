---
slug: ibby
titulo: Ibby: chassi de um carrinho de seis rodas
sub: Modelagem 3D da base, dos encaixes e do suporte da eletrônica, a partir das peças de corte a laser
data: 2026-10-23
stack: [Python, CadQuery, OpenCascade, Three.js, CAD, corte a laser]
competencias: [modelagem 3D, projeto mecânico, fabricação digital, desenho técnico]
areas: [Hardware e fabricação, Design]
---

## Contexto

O Ibby é um carrinho de seis rodas da liga de robótica IbBot. O projeto prevê controle pelo celular, por uma rede WiFi criada pelo próprio carrinho. Trabalhei no chassi de acrílico: a base, os pinos que prendem os motores e o suporte da placa Mega +WiFi.

![Chassi do Ibby em vista isométrica, com base azul clara, seis pinos altos azuis e suporte da Mega em bege](/img/ibby/montagem-frente.png)

*Montagem das 17 peças de acrílico. As cores distinguem os componentes; motores, rodas, placas e bateria ainda não fazem parte deste modelo.*

## O que eu fiz

Modelei o conjunto em 3D a partir das mesmas especificações que geram os arquivos de corte na [biblioteca de corte a laser](/blog/laser). A base mede 415 por 160 mm. A espessura de projeto é de 3 mm. Na montagem, cada furo e rasgo do desenho plano ocupa sua posição em relação às outras peças, o que permite conferir o conjunto antes de cortar a chapa.

![Chassi do Ibby visto por trás e pela direita, mostrando o berço elevado sobre os cavaletes](/img/ibby/montagem-tras.png)

*Na ponta, o berço da Mega fica sobre dois cavaletes e uma travessa. As aberturas dos cavaletes deixam passagem para os fios.*

Em cada uma das seis posições de motor há dois pinos: o alto entra no entalhe aberto da borda, e o curto entra no rasgo fechado, por dentro. Os pés descem abaixo da base e deixam entre eles o espaço para prender o motor TT.

![Vista inferior do Ibby, com os pés dos pinos atravessando a base](/img/ibby/vista-inferior.png)

*Vista por baixo. Os pés dos pinos descem 25 mm abaixo da chapa.*

Também gerei uma vista explodida e um detalhe ampliado do encaixe. Conferi as interferências no OpenCascade.

![Vista explodida do chassi, com os pinos, cavaletes, travessa e berço separados acima da base](/img/ibby/vista-explodida.png)

*As peças separadas na vertical mostram onde cada pino e cada parte do suporte se encaixam.*

## O que aprendi

Com as peças espalhadas na chapa, o desenho de corte não explica toda a montagem. No Ibby, foi preciso definir em qual rasgo cada pino entra e para que lado sua face larga fica voltada. Olhar por baixo ajudou.

![Detalhe de um par de pinos do Ibby, com o pino alto na borda e o curto por dentro](/img/ibby/detalhe-encaixe.png)

*Detalhe de um par de pinos. O vão entre as faces internas é de 18,4 mm; os três furos do pino alto permitem ajustar a fixação da carcaça.*

A conferência de interferência resolve a geometria nominal. O ajuste físico também depende da espessura medida da chapa e do material removido pelo laser. Mantive essas duas etapas distintas ao documentar o conjunto para a modelagem da carcaça.

## Resultados

- 17 peças na montagem: uma base, seis pinos altos, seis pinos curtos, um berço, dois cavaletes e uma travessa.
- Cinco vistas renderizadas do conjunto, incluindo montagem, vista inferior, explodida e detalhe de encaixe.
- Nenhuma interferência de volume entre as peças na verificação do modelo nominal.
- Modelos STEP e STL, documento técnico de 14 páginas e tabela de coordenadas gerados para orientar a modelagem da carcaça.
