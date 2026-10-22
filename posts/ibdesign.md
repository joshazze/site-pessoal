---
slug: ibdesign
titulo: Site da IbDesign
sub: Reconstrução do site da liga de design e arquitetura do Ibmec BH, em contas da própria liga
data: 2026-10-11
stack: [HTML, CSS, JavaScript, Python, Supabase, Cloudflare Pages]
competencias: [frontend, migração, performance, documentação]
link: https://ibdesign.org
---

## Contexto

A IbDesign é a liga de design e arquitetura do Ibmec BH. Seu primeiro site foi feito em Next.js e publicado na conta pessoal de quem o desenvolveu, numa plataforma de hospedagem. Com o tempo, o acesso a essa conta se perdeu. O site seguia no ar, intocável: ninguém conseguia corrigir um texto, publicar uma mudança ou apontar um domínio.

A liga criou uma conta própria. Meu trabalho foi trazer o site para ela sem que o visitante percebesse.

## O que eu fiz

Reconstruí o site sobre contas da liga. Páginas estáticas no Cloudflare Pages, conteúdo dinâmico no Supabase, custo zero.

![Abertura do site da IbDesign no computador](/img/ibdesign/desktop.png)

*A primeira tela de [ibdesign.org](https://ibdesign.org) no computador.*

![Site da IbDesign no celular](/img/ibdesign/celular.png)

*A mesma tela no celular.*

Como o deploy antigo era pré-renderizado, o HTML servido já trazia a página pronta. Escrevi um script em Python que remove o runtime do Next, aponta CSS, fontes e imagens para arquivos locais e preserva classes e estilos, o que mantém a aparência idêntica. As interações que dependiam de React viraram cerca de 150 linhas de JavaScript puro: a abertura com contador, o menu do celular, a barra que se esconde ao rolar e a linha do tempo arrastável.

Aproveitei para corrigir o que estava quebrado. Os dez links do menu apontavam todos para a página inicial, os botões de contato levavam a um email num domínio que nunca existiu, e faltavam `robots.txt`, `sitemap.xml` e uma página 404.

## Como funciona

O conteúdo que muda com frequência (projetos, linha do tempo, vivências e integrantes) fica em quatro tabelas no Supabase, com leitura pública e escrita restrita. Mas o HTML já sai preenchido. Se o banco ficar fora do ar ou for bloqueado na rede da faculdade, o site continua completo, e o script só atualiza o que estiver diferente.

Depois da migração vieram rodadas de design: as manchas de cor no fundo se movem em velocidades diferentes conforme o tamanho, e a linha do tempo fica presa no topo enquanto o scroll percorre os nove marcos. Com a logo nova, o site inteiro passou a usar um laranja só.

Escrevi também um manual de posse, guardado no repositório e no Drive da liga, explicando as contas, como mudar conteúdo sem programar, como publicar e como passar o site para a próxima diretoria.

## O que aprendi

A linha do tempo presa ao topo não funcionava. O `position: sticky` depende de qual elemento faz a rolagem, e um `overflow-x: hidden` no `html` e no `body` transformava a página num contêiner de rolagem próprio, o que anulava o efeito. Trocar `hidden` por `clip` resolveu, porque `clip` corta o conteúdo sem criar esse contêiner.

Também aprendi a medir animação. A bancada de testes usa o Chrome sem interface e precisa desligar o cache explicitamente. Senão, mede a versão velha.

## Resultados

- Site no ar em `ibdesign.org` desde 14 de setembro de 2026, em contas da própria liga, com custo zero.
- Imagens convertidas para WebP, de 9,0 MB para 2,1 MB.
- Página de projeto com similaridade estrutural de 0,977 em relação à original, conferida por imagem.
- Site completo mesmo com JavaScript desligado, e verificador automático conferindo rotas, imagens, cabeçalhos de segurança e as quatro tabelas.
