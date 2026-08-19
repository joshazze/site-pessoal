# site-pessoal

Registro público de Joshua Azze Distel em `jadistel.com`, com a assinatura acadêmica J. A.
Distel. HTML e CSS puros, sem build e sem dependência além das fontes do Google Fonts.

- `index.html` — resumo, quadro dos registros canônicos (Lattes, LinkedIn, GitHub) e as
  referências em NBR 6023.
- `blog.html` — servida em `/blog`: o arquivo **oqojfr?**, um registro por projeto. **Gerado.**
- `blog/<slug>.html` — um post por projeto. **Gerados.**
- `posts/*.md` — a fonte dos posts, o que se escreve à mão.
- `modelo/` — os dois templates que o gerador preenche.
- `gerar.py` — transforma `posts/*.md` em `blog.html`, `blog/*.html` e `sitemap.xml`.
- `estilo.css` / `vivo.js` — identidade e movimento da home.
- `retro.css` / `retro.js` — identidade e movimento do blog.

## Design

**Home:** tipografia de publicação científica como referência, não como fac-símile. Tinos
justificado com hifenização, seções numeradas, quadro com legenda e "Fonte:", referências ABNT.
Segue `prefers-color-scheme`.

**Blog (`oqojfr?`):** retro futurista de 1985, com o painel de time circuits do DeLorean como
cabeçalho. Tema escuro fixo, porque é cena noturna. Neon e LED só em título, moldura, mostrador e
acento; corpo de texto sempre em alto contraste, nunca em neon. Wordmark cromado em Alfa Slab One,
corpo do post em Tinos para não sacrificar legibilidade.

Os três mostradores nunca falam de atualização, só de posição na cronologia:

| Mostrador | O que mostra |
|---|---|
| `DESTINATION TIME` | data do post em foco |
| `PRESENT TIME` | agora, contando sozinho |
| `LAST TIME DEPARTED` | o post anterior na linha do tempo |

A lista é cronológica com o mais recente no topo. Não existe "atualizado há X dias", nem contador
de respostas, nem qualquer marca que sugira projeto abandonado.

## Escrever um post

Um arquivo em `posts/<slug>.md`, frontmatter mais as seções obrigatórias. O gerador recusa o post
que não tiver **Contexto**, **O que eu fiz**, **O que aprendi** e **Resultados**. `Como funciona`
é opcional.

```markdown
---
slug: ibsala
titulo: ibsala
sub: uma linha do que é
data: 2026-08-15
stack: [Flask, PostgreSQL]
competencias: [backend, deploy]
link: https://ibsala.com.br
repo: https://github.com/joshazze/algum-repo
---

## Contexto
## O que eu fiz
## Como funciona
## O que aprendi
## Resultados
```

Convenção da data: um pouco depois do fim do projeto, tipicamente o último commit do repo mais uns
dias. O frontmatter sempre ganha.

Antes de commitar um post, a revisão de vazamento é obrigatória e é leitura humana, nenhum scanner
pega: sem URL de painel administrativo, sem IP ou hostname de máquina, sem token ou chave (mesmo
revogada), sem print com nome ou matrícula de aluno, sem nada sob acordo de terceiro.

Depois:

```sh
python3 gerar.py          # só stdlib, sem pip
git add posts blog.html blog sitemap.xml && git commit
```

O HTML gerado **vai commitado**: é isso que mantém o Pages servindo arquivo cru, sem build.
Apagar um `.md` e rodar o gerador remove a página órfã de `blog/`.

## O que é vivo, não reativo

Coisas que acontecem sem ninguém tocar na tela:

1. **Relógio da sessão** na home e data de acesso das referências, no formato `26 jul. 2026` da
   NBR 6023.
2. **Pulso do GitHub**: a última atividade pública vem da API a cada dois minutos e o "há 26 min"
   é recalculado a cada trinta segundos.
3. **Quadro que respira**: uma linha acende de cada vez, em ciclo. Qualquer toque cala o ciclo por
   12 s, porque quem interage manda.
4. **Time circuits**: `PRESENT TIME` conta de segundo em segundo e `DESTINATION TIME` percorre o
   arquivo sozinho, com a mesma regra dos 12 s.

`prefers-reduced-motion: reduce` desliga o movimento decorativo e mantém o dado vivo.

## Deploy no Cloudflare Pages

Cada push na `main` republica. Framework preset **None**, sem build command, output `/` (raiz).
O Pages serve `blog.html` em `/blog` e `blog/ibsala.html` em `/blog/ibsala` sozinho. `_redirects`
manda `/producao` para `/blog` com 301. O apex convive com os MX do email por CNAME flattening.

## Conferir localmente

```sh
python3 gerar.py
python3 -m http.server 8000
# http://localhost:8000  ·  /blog.html  ·  /blog/ibsala.html
```

Conferir o deploy por `https://site-pessoal-39d.pages.dev`, não por `jadistel.com`: na rede de
casa o domínio cai numa página de bloqueio FortiGuard e parece que o site caiu.
