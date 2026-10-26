---
slug: liga-ibtech
titulo: Liga Acadêmica IbTech
sub: Diretoria acadêmica na chapa unificada: trilhas de formação, revisão das entregas e credenciais verificáveis
data: 2026-08-16
stack: [Node.js, Ethereum, Open Badges 3.0, Blockcerts, SHA-256]
competencias: [liderança, criptografia aplicada, revisão de código, processo]
areas: [Liderança e ligas, Segurança e privacidade, Educação, Código aberto]
link: https://www.ligastechibmec.com.br
repo: https://github.com/joshazze/ibtech-credenciais
---

## Contexto

A IbTech é a liga de software do Ibmec BH. Sou diretor acadêmico na chapa unificada, e o trabalho tem três frentes bem diferentes: montar as trilhas de formação, revisar as entregas dos membros e resolver uma questão que toda liga acadêmica enfrenta no fim do ciclo.

É o certificado. Ele serve para o membro mostrar no LinkedIn e para o recrutador confiar no que está lendo. O certificado acadêmico mais comum, porém, é um PDF com assinatura escaneada, fácil de refazer em poucos minutos com outro nome. Todo mundo sabe.

![Logo da IbTech](/img/liga-ibtech/ibtech.svg)

*Logo da IbTech.*

## O que eu fiz

Na formação, cuido das trilhas e da revisão das entregas. Cada trabalho aprovado vai para um repositório central da liga por branch e pull request, com revisão nominal, em vez de ficar perdido no Drive de quem fez.

Nas credenciais, construí um emissor próprio, com a prova de cada lote gravada na blockchain. Ele virou um tópico separado: [Certificados verificáveis para o LinkedIn](/blog/credenciais-verificaveis).

## O que aprendi

Na operação, não criei fluxo de e-mail nem resgate individual. O lote inteiro é gerado de uma vez e cada pessoa recebe o link pronto. Se cada membro precisasse entrar e clicar em "reivindicar minha credencial", boa parte das trinta e duas ficaria sem resgate.

## Resultados

- 32 certificados emitidos e ancorados numa única transação, com verificação criptográfica ao vivo.
- Cada credencial tem URL própria, que é o que o botão "Mostrar credencial" do LinkedIn pede.
- Nenhum custo de plataforma, contra uma alternativa comercial que exige CNPJ e mensalidade.
- Código público em `joshazze/ibtech-credenciais`, com uma explicação didática de como a árvore de Merkle sustenta a prova.
- Instagram da liga: [@ibtechbh](https://www.instagram.com/ibtechbh).
