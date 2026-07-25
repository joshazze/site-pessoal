# site-pessoal

Página única com os links públicos do Joshua Azze Distel: Currículo Lattes, LinkedIn e GitHub.
HTML e CSS puros, sem build, sem dependência além das fontes do Google Fonts.

## Antes de publicar

Dois lugares no `index.html` estão marcados com `<!-- TROCAR -->`:

1. **LinkedIn**: `href` e o handle exibido (`/in/SEU-HANDLE`).
2. **Email**: `contato@SEUDOMINIO.com` no rodapé, assim que o domínio estiver registrado.

## Deploy no Cloudflare Pages

1. Criar o repo no GitHub e dar push da `main`.
2. Cloudflare > Workers & Pages > Create > Pages > Connect to Git, escolher o repo.
3. Framework preset: **None**. Build command: vazio. Output directory: `/` (raiz).
4. Custom domains > adicionar o domínio. A Cloudflare cria o CNAME sozinha se a zona já é dela.

Cada push na `main` republica. O apex do site convive com os MX do email sem conflito
(CNAME flattening).

## Conferir localmente

```sh
python3 -m http.server 8000
# abre http://localhost:8000
```

## Design

Registro de identidades no lugar da pilha de botões de linktree: cada linha traz o serviço à
esquerda e o identificador no vocabulário do próprio serviço à direita (o número do ID Lattes,
o `/in/` do LinkedIn, o `@` do GitHub). Paleta azul institucional, Newsreader no nome, IBM Plex
Sans e Mono no resto. Responsivo (empilha abaixo de 480px), foco visível no teclado,
`prefers-reduced-motion` e modo escuro respeitados.
