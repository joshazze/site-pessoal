# site-pessoal

Registro público de Joshua Azze Distel em `jadistel.com`, com a assinatura acadêmica J. A.
Distel. Duas páginas, HTML e CSS puros, sem build e sem dependência além das fontes do Google
Fonts.

- `index.html` — resumo, quadro dos três registros canônicos (Lattes, LinkedIn, GitHub) e as
  referências em NBR 6023.
- `producao.html` — servida em `/producao`: software em operação, repositórios públicos, artigo
  de iniciação científica, prêmios e atuação nas ligas.
- `estilo.css` — identidade compartilhada.
- `vivo.js` — o que se mexe sozinho.

## Design

Tipografia de publicação científica como referência, não como fac-símile: Tinos (métrica de
Times New Roman) justificado com hifenização, seções numeradas, resumo com palavras-chave,
quadro com legenda e "Fonte:", referências ABNT e nota de rodapé de filiação. Em tela larga o
número da seção sai para a margem esquerda, como em periódico. Nada de folha A4 desenhada na
tela; a folha aparece ao imprimir, e aí sai A4 com margens 3/2 cm de verdade.

Mobile primeiro: coluna única, nada abaixo de 16px, linhas do quadro com 76px de alvo de toque,
tema seguindo `prefers-color-scheme` e `prefers-reduced-motion` respeitado.

## O que é vivo, não reativo

Coisas que acontecem sem ninguém tocar na tela:

1. **Relógio da sessão** no cabeçalho e data de acesso das referências, sempre no formato
   `26 jul. 2026` da NBR 6023.
2. **Pulso do GitHub**: a última atividade pública é buscada na API a cada dois minutos e o
   "há 26 min" é recalculado a cada trinta segundos. A contagem de repositórios no Quadro 1
   também vem da API, não está digitada no HTML.
3. **Quadro que respira**: uma linha visível acende de cada vez, em ciclo de 3,4 s. Qualquer
   toque, movimento de ponteiro ou tecla cala o ciclo por 12 s, porque quem interage manda.

Reativo, isso o documento também é: citação, referência e linha do quadro acendem juntas quando
uma delas recebe o cursor, o toque ou o foco do teclado.

## Deploy no Cloudflare Pages

Cada push na `main` republica. Framework preset **None**, sem build command, output `/` (raiz).
O Pages serve `producao.html` em `/producao` sozinho. O apex convive com os MX do email por
CNAME flattening.

## Conferir localmente

```sh
python3 -m http.server 8000
# http://localhost:8000  e  http://localhost:8000/producao.html
```
