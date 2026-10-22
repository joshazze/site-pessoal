---
slug: handshake
titulo: Handshake
sub: Trilha diária de estudo no estilo Duolingo, com repetição espaçada por conceito
data: 2026-10-22
stack: [Python, stdlib, Caddy, Oracle Cloud, PWA]
competencias: [produto, algoritmo de repetição espaçada, segurança web, infraestrutura]
---

## Contexto

Redes de Computadores é uma disciplina com muito conteúdo para memorizar e muito cálculo para treinar: camadas, protocolos, sub-redes, endereçamento IPv6. Reler slides na véspera rende pouco. Rever um pouco por dia rende mais.

Eu queria uma trilha diária parecida com a do Duolingo. Vinte e cinco questões por dia, explicação depois de cada resposta, certa ou errada, e o que eu errasse voltando com mais frequência até ficar firme. Só questões fechadas. Nunca a mesma duas vezes do mesmo jeito.

## O que eu fiz

Um app web chamado Handshake, multiusuário e com espaço para mais de uma disciplina, em que cada dia tem uma lição de 25 questões e completá-la mantém acesa a chama que conta a sequência de dias.

O conteúdo de Redes começa num texto-base de 90 seções, uma para cada questão das listas da disciplina, com cerca de 14 mil palavras e a página da fonte citada em cada seção. As questões saem desse texto: 225 fatos, cada um com quatro formas diferentes de perguntar. Para os cálculos, como sub-rede, broadcast, faixa de hosts, CIDR e EUI-64, há nove geradores que criam questões novas a cada vez, com alternativas erradas tiradas de erros comuns.

Quando erro, o app abre a seção do texto de onde a questão saiu.

## Como funciona

A unidade de memória é o conceito. Cada conceito fica numa de seis caixas, revistas a cada 1, 2, 4, 8, 16 e 32 dias; quando dominado, passa a voltar a cada 60. Um erro devolve o conceito para a primeira caixa, e ele reaparece três questões depois e outra vez no fim da lição, sempre com outra variante.

A lição junta primeiro os conceitos vencidos, depois os novos, na sequência da trilha, e por fim reforço dos mais fracos.

O servidor é Python puro, sem framework, com os dados em arquivos. Roda numa VM gratuita da Oracle Cloud, com Caddy cuidando do HTTPS por Let's Encrypt. Segurança veio desde o início. O gabarito só chega ao navegador depois da resposta, a política de conteúdo é estrita, há proteção contra requisição forjada e uma trava contra tentativas repetidas de login.

## O que aprendi

Custo zero era exigência. A primeira versão foi desenhada para serviços gratuitos da AWS, com Lambda e DynamoDB em capacidade provisionada mínima, porque a capacidade sob demanda gera cobrança. Acabei migrando para uma VM da Oracle no plano sempre gratuito, que é mais simples de operar para um app desse tamanho.

A VM trouxe uma restrição: a porta 443 já era usada como porta alternativa de SSH, porque a rede da faculdade bloqueia a porta 22. A solução foi colocar na 443 um multiplexador que separa conexões TLS de conexões SSH e encaminha cada uma para o serviço certo. Há um efeito colateral, documentado. Atrás do multiplexador, o app vê todo cliente como vindo do próprio servidor, então a trava de login por IP passa a valer para todos de uma vez, enquanto a trava por usuário continua funcionando normalmente.

## Resultados

- No ar com HTTPS e certificado renovado automaticamente.
- 225 fatos com quatro variantes cada e 9 geradores de cálculo, cobrindo as 90 seções do texto-base.
- Repetição espaçada em seis caixas, de 1 a 32 dias, mais a de 60 para o que já foi dominado.
- 20 testes automáticos, e o motor de revisão conferido em três fusos horários diferentes.
