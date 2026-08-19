---
slug: liga-ibtech
titulo: Liga Acadêmica IbTech
sub: Vice-presidência: trilhas de formação, revisão das entregas e credenciais verificáveis
data: 2026-08-16
stack: [Node.js, Ethereum, Open Badges 3.0, Blockcerts, SHA-256]
competencias: [liderança, criptografia aplicada, revisão de código, processo]
link: https://www.ligastechibmec.com.br
repo: https://github.com/joshazze/ibtech-credenciais
---

## Contexto

A IbTech é a liga de software do Ibmec BH. Eu sou vice-presidente, e o trabalho tem três frentes que não se parecem: montar as trilhas de formação, revisar o que os membros entregam, e resolver o problema chato que toda liga acadêmica tem no fim do ciclo.

O problema chato é o certificado. Ele existe para o membro colocar no LinkedIn e para o recrutador acreditar. Só que o certificado acadêmico brasileiro típico é um PDF com uma assinatura escaneada, e a única coisa que ele prova é que alguém tem Canva. Qualquer pessoa refaz o seu em dez minutos, com o nome trocado. A liga sabe disso, o membro sabe disso, e o recrutador também.

## O que eu fiz

Do lado da formação, as trilhas e a revisão das entregas. Cada trabalho aprovado vai para um repositório central da liga por branch e pull request, com revisão nominal, e não some no Drive de quem fez.

Do lado das credenciais, construí um emissor próprio. Cada certificado vira um JSON no padrão Open Badges 3.0, no formato Blockcerts. Calcula-se o SHA-256 de cada um, monta-se uma árvore de Merkle do lote inteiro, e só a raiz vai para a blockchain, numa única transação. Verificar é recalcular o hash do certificado, subir a árvore até a raiz e conferir se ela bate com a que está registrada na rede.

O detalhe que faz isso valer a pena é o custo. Trinta e dois certificados poderiam ser trinta e duas transações. Com a árvore de Merkle são trinta e duas provas e uma transação só, e ainda assim adulterar qualquer nome quebra a raiz.

## Como funciona

O pipeline é Node enxuto, três comandos: `build` gera os JSON, `anchor` monta a árvore e grava a raiz, `verify` refaz a conta. Não usei a tooling oficial do Blockcerts porque ela é Python e não roda na versão que eu tenho instalada, e reescrever o essencial em Node saiu mais rápido que resolver a incompatibilidade.

A rede é Ethereum Sepolia, escolha feita pelo torneirinha: o faucet do Google Cloud oferece Sepolia e não oferece as alternativas. O código é agnóstico de rede, o RPC vive em variável de ambiente, e trocar de rede é trocar uma linha.

Também descartei a plataforma comercial brasileira de badges. Ela cobra, exige CNPJ, e o que ela mostra ao recrutador no fim é um hash impresso na tela. A nossa não custa plataforma, não exige personalidade jurídica e verifica ao vivo, refazendo a criptografia no navegador de quem está olhando.

## O que aprendi

Nenhum recrutador vai abrir um verificador. Essa foi a lição que me obrigou a jogar fora a primeira versão da página.

A primeira versão era honesta e feia: um formulário, um campo de id, um "válido" em verde. Tecnicamente completa, e ninguém ia clicar duas vezes. A segunda versão trata a verificação como cerimônia. O certificado aparece emoldurado, a conferência acontece na frente de quem está olhando, com o painel mostrando o que está sendo recalculado, e no fim tem QR e exportação em PDF. O design reproduz o certificado oficial da liga, com o logo extraído do PDF original, para que a página não pareça um sistema de terceiro.

A criptografia é a mesma nas duas versões. A diferença é que a segunda é vista.

A outra lição foi de operação, não de código: não montei fluxo de e-mail e claim individual. Gera-se o lote inteiro de uma vez e avisa-se cada pessoa com o link pronto. Esperar trinta e duas pessoas clicarem em "reivindicar minha credencial" é a forma mais confiável de emitir doze.

## Resultados

- 32 certificados emitidos e ancorados numa única transação, com verificação criptográfica ao vivo.
- Cada credencial tem URL própria, que é exatamente o que o botão "Mostrar credencial" do LinkedIn pede.
- Custo de plataforma zero, contra uma alternativa comercial que exige CNPJ e mensalidade.
- O código é público em `joshazze/ibtech-credenciais`, com uma explicação didática de como a árvore de Merkle sustenta a prova.
