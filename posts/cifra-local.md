---
slug: cifra-local
titulo: Dados cifrados no aparelho
sub: Um padrão de app pessoal que não tem servidor para vazar, com o myco como caso
data: 2026-06-02
stack: [WebCrypto, PBKDF2, AES-GCM, IndexedDB, Vite]
competencias: [criptografia aplicada, privacidade por desenho, PWA]
repo: https://github.com/joshazze/myco
---

## Contexto

Todo app pessoal começa igual: você quer registrar uma coisa sua, num lugar que seja seu. Plantas, treinos, gastos, o que for.

E aí vem a pergunta chata. Onde isso mora? A resposta padrão é um banco no servidor, com login e senha, o que significa que agora existe um servidor com os seus dados dentro, e você virou responsável por ele. Backup, atualização de dependência, um dia um vazamento. Para um app que só você usa, isso é uma responsabilidade enorme em troca de nada.

A outra resposta padrão é guardar tudo em claro no navegador, o que resolve o servidor e cria outro problema: qualquer script na página, qualquer extensão, qualquer pessoa com o aparelho na mão lê tudo.

## O que eu fiz

Um padrão que eu usei em mais de um app: os dados nascem cifrados no aparelho e nunca saem dele em claro. Não existe conta, não existe servidor, e não existe nada meu para vazar, porque eu não tenho nada.

O caso nomeado aqui é o **myco**, um app de jardinagem que guarda vasos, setores, adubação e compostagem. É público, é bobo, e é justamente por ser bobo que serve de exemplo: se o padrão vale a pena para um caderno de plantas, ele vale para qualquer coisa. O mesmo módulo de criptografia roda hoje em outro app pessoal meu, com dados bem menos triviais.

## Como funciona

A senha nunca é guardada e nunca vira chave diretamente.

Ela passa por PBKDF2 com 250.000 iterações e SHA-256, junto com um sal aleatório gerado na criação da base, e o que sai é uma chave AES-GCM de 256 bits. As iterações existem para tornar cara a tentativa de adivinhação: quem capturar a base cifrada precisa pagar 250 mil derivações por palpite, o que transforma um ataque de dicionário de minutos em algo impraticável.

Cada gravação é cifrada com AES-GCM e um vetor de inicialização novo, o que dá confidencialidade e integridade na mesma operação: um byte alterado no armazenamento faz a decifragem falhar em vez de devolver lixo silenciosamente. Tudo roda pela WebCrypto do próprio navegador, sem biblioteca de criptografia de terceiro, e o resultado cifrado descansa em IndexedDB.

Existe um verificador curto gravado junto, cifrado com a mesma chave. Ele serve para dizer "senha errada" na hora de destravar, em vez de tentar decifrar a base inteira e falhar de um jeito confuso.

## O que aprendi

O backup é onde o desenho todo quase morreu.

Sem servidor, não existe recuperar senha. Se a pessoa esquece, os dados acabaram, e isso não é bug, é a consequência direta da promessa. Foi a parte mais difícil de aceitar, e a que quase me fez colocar um servidor de volta só para ter um "esqueci minha senha" que funciona.

A saída foi exportar a base cifrada como arquivo, que a pessoa guarda onde quiser. O arquivo é inútil sem a senha, então pode viver no Drive, no e-mail, num pendrive, sem que nada disso vire superfície de ataque. E aí o modelo fica honesto de verdade: o app não protege você de esquecer a senha, e diz isso na cara, em vez de fingir que existe uma porta dos fundos que na prática é a porta da frente de qualquer atacante.

Segurança que depende de o usuário não errar é teatro. Segurança que declara o que não faz é engenharia.

## Resultados

- Padrão em produção em dois apps pessoais, com o mesmo módulo de criptografia compartilhado entre eles.
- PBKDF2 com 250.000 iterações e SHA-256 derivando chave AES-GCM de 256 bits, tudo pela WebCrypto nativa, sem dependência de biblioteca externa de criptografia.
- Zero servidor e zero conta: nenhum dado do usuário existe fora do aparelho dele.
- Exportação da base cifrada como caminho de backup, guardável em qualquer lugar sem virar risco.
- O caso nomeado, `myco`, é público sob licença aberta, instalável como app e com o código de cifra em um arquivo só, legível de uma sentada.
