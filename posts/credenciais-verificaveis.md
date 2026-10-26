---
slug: credenciais-verificaveis
titulo: Certificados verificáveis para o LinkedIn
sub: Emissor de credenciais em Open Badges 3.0 com a prova gravada na blockchain, uma transação por lote
data: 2026-08-14
stack: [Node.js, Ethereum, Open Badges 3.0, Blockcerts, SHA-256, árvore de Merkle]
competencias: [criptografia aplicada, design de produto, processo]
areas: [Segurança e privacidade, Código aberto, Web, Educação]
---

## Contexto

O certificado de curso, liga ou evento quase sempre é um PDF com assinatura escaneada. Trocar o nome leva dois minutos num editor de imagem. Quem recebe sabe. O recrutador também.

O LinkedIn tem um campo para isso, "Licenças e certificados", com um botão "Mostrar credencial" que só pede uma URL. Ele não confere nada: se a URL abre um PDF, a prova continua sendo um PDF, com todos os problemas do parágrafo anterior.

Eu queria que a URL levasse a uma página que provasse sozinha que aquele documento é o que foi emitido, sem depender de ninguém responder um e-mail.

## O que eu fiz

Construí um emissor próprio. Cada certificado é um JSON no padrão Open Badges 3.0, com campos separados para quem recebeu, o que foi reconhecido, quem emitiu, quando e por quais critérios. O sistema calcula o SHA-256 de cada JSON, monta uma árvore de Merkle com o lote inteiro e grava só a raiz na blockchain, numa transação.

Para conferir, a página recalcula o hash do certificado no navegador de quem está olhando, sobe pela árvore até a raiz e compara com a raiz registrada na rede. Uma vírgula a mais e a conta não fecha.

Cada credencial ganha uma URL própria, que é exatamente o que o botão do LinkedIn pede.

## Como funciona

O pipeline é Node, em três comandos: `build` gera os JSON, `anchor` monta a árvore e grava a raiz, `verify` refaz a conta inteira. Por que não a ferramenta oficial do Blockcerts? Ela é em Python e não roda na versão que tenho instalada, e reescrever o essencial em Node saiu mais rápido do que brigar com a incompatibilidade.

Quem segura o custo é a árvore de Merkle. Trinta e dois certificados seriam trinta e duas transações. Com a árvore, viram trinta e duas provas curtas e uma transação só.

A rede hoje é a Ethereum Sepolia, porque o faucet do Google Cloud oferece Sepolia. O código não depende dela: o RPC fica numa variável de ambiente, e trocar de rede é mudar uma linha.

Descartei a plataforma comercial brasileira de badges. Ela cobra, exige CNPJ e, no fim, mostra ao recrutador um hash impresso na tela sem refazer conta nenhuma.

## O que aprendi

Recrutador não abre verificador. A primeira versão da página era correta e sem graça: um campo de identificador e um "válido" em verde. Refiz. Na segunda, o certificado aparece emoldurado, a conferência acontece na tela com um painel mostrando o que está sendo recalculado, e no fim há QR code e exportação em PDF. Criptografia idêntica nas duas.

Fluxo de resgate individual também não funciona. Se cada pessoa precisa entrar e clicar em "reivindicar minha credencial", metade não clica. O lote sai inteiro de uma vez e cada um recebe o link pronto. Para as emissões maiores, juntei todos os links num PDF só, com o passo a passo do LinkedIn na primeira página, para mandar uma vez no grupo.

Por último: o documento só vale o que os registros sustentam. Numa das levas, a primeira ideia era atestar frequência, mas não havia chamada registrada. Então o certificado passou a atestar conclusão e carga horária, que era o que dava para provar.

## Resultados

- 32 certificados ancorados numa única transação, verificados ao vivo no navegador.
- Mais 36 credenciais publicadas no mesmo modelo de página, com o banco conferido campo a campo contra o que cada página serve: zero divergência.
- Um único PDF com os 36 links clicáveis no lugar de 36 mensagens.
- Custo de plataforma zero, contra uma alternativa que exige CNPJ e mensalidade.
- Próximo passo: levar a âncora para a Polygon, onde um lote custa centavos e a emissão deixa de ser em rede de teste.
