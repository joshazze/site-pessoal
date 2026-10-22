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

Nas credenciais, construí um emissor próprio. Cada certificado é um JSON em Open Badges 3.0. O sistema calcula o SHA-256 de cada um, monta uma árvore de Merkle com o lote inteiro e registra apenas a raiz na blockchain, numa única transação. Para verificar, basta recalcular o hash do certificado, subir pela árvore até a raiz e conferir se ela corresponde à registrada na rede.

O ganho está no custo. Trinta e dois certificados poderiam exigir trinta e duas transações. Com a árvore de Merkle, são trinta e duas provas e uma transação, e alterar qualquer nome continua quebrando a raiz.

## Como funciona

O pipeline é um Node enxuto com três comandos: `build` gera os JSON, `anchor` monta a árvore e grava a raiz, `verify` refaz a conta. Não usei a ferramenta oficial do Blockcerts porque ela é em Python e não roda na versão que tenho instalada, e reescrever o essencial em Node foi mais rápido do que resolver a incompatibilidade.

A rede é a Ethereum Sepolia, escolhida porque o faucet do Google Cloud oferece Sepolia e não as alternativas. O código não depende da rede: o RPC fica numa variável de ambiente, e trocar de rede é mudar uma linha.

Também descartei a plataforma comercial brasileira de badges, que é paga, exige CNPJ e, depois de tudo isso, mostra ao recrutador apenas um hash impresso na tela, sem refazer conta nenhuma. A nossa não tem custo de plataforma, não exige pessoa jurídica e faz a verificação ao vivo, recalculando a criptografia no navegador de quem está conferindo.

## O que aprendi

Recrutador não abre verificador. Foi isso que me levou a refazer a primeira versão da página.

A primeira versão era correta e sem graça: um formulário, um campo de identificador e um "válido" em verde. Ninguém voltaria. A segunda apresenta a verificação como parte da experiência. O certificado aparece emoldurado, a conferência acontece na tela, com um painel mostrando o que está sendo recalculado, e no final há QR code e exportação em PDF. O design reproduz o certificado oficial da liga, com o logo extraído do PDF original, para que a página não pareça um sistema de terceiros. A criptografia é a mesma nas duas versões. A diferença é que a segunda é vista.

A outra lição foi de operação: não criei fluxo de e-mail nem resgate individual: o lote inteiro é gerado de uma vez e cada pessoa recebe o link pronto. Se cada membro precisasse entrar e clicar em "reivindicar minha credencial", boa parte das trinta e duas ficaria sem resgate.

## Resultados

- 32 certificados emitidos e ancorados numa única transação, com verificação criptográfica ao vivo.
- Cada credencial tem URL própria, que é o que o botão "Mostrar credencial" do LinkedIn pede.
- Nenhum custo de plataforma, contra uma alternativa comercial que exige CNPJ e mensalidade.
- Código público em `joshazze/ibtech-credenciais`, com uma explicação didática de como a árvore de Merkle sustenta a prova.
- Instagram da liga: [@ibtechbh](https://www.instagram.com/ibtechbh).
