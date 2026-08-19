#!/usr/bin/env python3
"""gera o blog oqojfr? a partir de posts/*.md

só biblioteca padrão: nada de pip, nada de build no Cloudflare. o html sai daqui
já pronto e vai commitado, que é o que mantém o Pages servindo arquivo cru.

    python3 gerar.py

todo texto vindo do .md é escapado antes de virar html. o subconjunto de markdown
é fixo e pequeno de propósito: se um dia o conteúdo vier de fora, não tem por onde
injetar tag.
"""

import html
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
POSTS = RAIZ / "posts"
MODELO = RAIZ / "modelo"
SAIDA_POSTS = RAIZ / "blog"

VERSAO = "1"  # cache buster de retro.css e retro.js

MES_LED = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
           "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
MES_CURTO = ["jan", "fev", "mar", "abr", "maio", "jun",
             "jul", "ago", "set", "out", "nov", "dez"]
MES_LONGO = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

# o esqueleto que todo post tem que ter. "Como funciona" é opcional: prêmio e
# artigo não têm como funcionar, projeto tem.
OBRIGATORIAS = ["Contexto", "O que eu fiz", "O que aprendi", "Resultados"]

ESQUEMAS_OK = ("https://", "http://", "mailto:", "/", "#")


# ---------------------------------------------------------------- frontmatter

def ler_frontmatter(texto, arquivo):
    if not texto.startswith("---"):
        erro(arquivo, "falta o frontmatter (bloco --- no topo)")
    _, bruto, corpo = texto.split("---", 2)
    dados = {}
    for linha in bruto.strip().splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        if ":" not in linha:
            erro(arquivo, f"linha de frontmatter sem dois-pontos: {linha!r}")
        chave, valor = linha.split(":", 1)
        valor = valor.strip()
        if valor.startswith("[") and valor.endswith("]"):
            itens = [v.strip() for v in valor[1:-1].split(",")]
            dados[chave.strip()] = [v for v in itens if v]
        else:
            dados[chave.strip()] = valor
    return dados, corpo.lstrip("\n")


# ------------------------------------------------------------------- markdown

def url_segura(u):
    """só deixa passar destino que o navegador abre sem executar nada."""
    limpo = u.strip()
    if limpo.lower().startswith(ESQUEMAS_OK) or limpo.startswith(("./", "../")):
        return limpo
    return "#"


def inline(txt):
    """escapa primeiro, formata depois. inverter a ordem é como se injeta tag."""
    txt = html.escape(txt, quote=True)

    # código inline sai de cena antes de negrito e itálico o alcançarem
    guardado = []

    def guardar(m):
        guardado.append(m.group(1))
        return f"\x00{len(guardado) - 1}\x00"

    txt = re.sub(r"`([^`]+)`", guardar, txt)

    txt = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)\)",
        lambda m: f'<img src="{url_segura(m.group(2))}" alt="{m.group(1)}" loading="lazy">',
        txt,
    )
    txt = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{url_segura(m.group(2))}">{m.group(1)}</a>',
        txt,
    )
    txt = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", txt)
    txt = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", txt)

    return re.sub(r"\x00(\d+)\x00",
                  lambda m: f"<code>{guardado[int(m.group(1))]}</code>", txt)


def markdown(corpo, arquivo):
    """subconjunto fixo: h2, h3, lista, lista numerada, citação, código, parágrafo."""
    saida = []
    lista = None          # 'ul' ou 'ol' quando uma lista está aberta
    codigo = False
    buffer_codigo = []
    paragrafo = []
    secoes = []

    def fechar_paragrafo():
        if paragrafo:
            saida.append(f"<p>{inline(' '.join(paragrafo))}</p>")
            paragrafo.clear()

    def fechar_lista():
        nonlocal lista
        if lista:
            saida.append(f"</{lista}>")
            lista = None

    for linha in corpo.splitlines():
        crua = linha.rstrip()
        seco = crua.strip()

        if seco.startswith("```"):
            if codigo:
                bloco = html.escape("\n".join(buffer_codigo), quote=True)
                saida.append(f"<pre><code>{bloco}</code></pre>")
                buffer_codigo.clear()
                codigo = False
            else:
                fechar_paragrafo()
                fechar_lista()
                codigo = True
            continue

        if codigo:
            buffer_codigo.append(crua)
            continue

        if not seco:
            fechar_paragrafo()
            fechar_lista()
            continue

        if seco.startswith("### "):
            fechar_paragrafo(); fechar_lista()
            saida.append(f"<h3>{inline(seco[4:])}</h3>")
            continue

        if seco.startswith("## "):
            fechar_paragrafo(); fechar_lista()
            titulo = seco[3:].strip()
            secoes.append(titulo)
            saida.append(f"<h2>{inline(titulo)}</h2>")
            continue

        if seco.startswith("> "):
            fechar_paragrafo(); fechar_lista()
            saida.append(f"<blockquote><p>{inline(seco[2:])}</p></blockquote>")
            continue

        if seco.startswith("- "):
            fechar_paragrafo()
            if lista != "ul":
                fechar_lista()
                saida.append("<ul>")
                lista = "ul"
            saida.append(f"<li>{inline(seco[2:])}</li>")
            continue

        numerada = re.match(r"^\d+\.\s+(.*)$", seco)
        if numerada:
            fechar_paragrafo()
            if lista != "ol":
                fechar_lista()
                saida.append("<ol>")
                lista = "ol"
            saida.append(f"<li>{inline(numerada.group(1))}</li>")
            continue

        if lista:
            fechar_lista()
        paragrafo.append(seco)

    if codigo:
        erro(arquivo, "bloco de código aberto e não fechado (```)")
    fechar_paragrafo()
    fechar_lista()

    faltando = [s for s in OBRIGATORIAS if s not in secoes]
    if faltando:
        erro(arquivo, "faltam seções obrigatórias: " + ", ".join(faltando))

    return "\n".join(saida)


# ---------------------------------------------------------------------- datas

def ler_data(txt, arquivo):
    try:
        return date.fromisoformat(str(txt).strip())
    except ValueError:
        erro(arquivo, f"data inválida: {txt!r} (use AAAA-MM-DD)")


def curta(d):
    return f"{MES_CURTO[d.month - 1]} {d.year}"


def longa(d):
    return f"{d.day} de {MES_LONGO[d.month - 1]} de {d.year}"


# ------------------------------------------------------------- time circuits

def celula(cap, largura, valor):
    """um mostrador: o fantasma dos segmentos apagados embaixo, o valor aceso em cima.
    valor vazio deixa a célula escura de propósito, que é mais honesto do que chutar."""
    aceso = html.escape(valor, quote=True) if valor else ""
    return (
        f'<span class="cel"><span class="cap">{cap}</span>'
        f'<span class="led"><span class="off">{"8" * largura}</span>'
        f'<span class="on">{aceso}</span></span></span>'
    )


def circuito(cor, rotulo, d, ids=""):
    """post só tem data, não tem hora: hora e minuto ficam com os segmentos apagados.
    o único mostrador com hora acesa é o PRESENT TIME, e quem acende é o retro.js."""
    if d:
        mes, dia, ano = MES_LED[d.month - 1], f"{d.day:02d}", str(d.year)
    else:
        mes = dia = ano = ""
    celulas = [
        celula("mês", 3, mes),
        celula("dia", 2, dia),
        celula("ano", 4, ano),
        celula("hora", 2, ""),
        celula("min", 2, ""),
    ]
    return (
        f'    <div class="circuito" data-cor="{cor}"{ids}>\n'
        f'      <span class="rotulo">{rotulo}</span>\n'
        f'      <div class="mostrador">{"".join(celulas)}</div>\n'
        f"    </div>"
    )


def bloco_circuitos(posts):
    destino = posts[0]["data"] if posts else None
    partida = posts[1]["data"] if len(posts) > 1 else None
    linhas = [
        '  <section class="circuitos" aria-label="Time circuits">',
        circuito("dest", "destination time", destino, ids=' id="c-destino"'),
        circuito("pres", "present time", None, ids=' id="c-presente"'),
        circuito("part", "last time departed", partida, ids=' id="c-partida"'),
        "  </section>",
    ]
    return "\n".join(linhas)


# ------------------------------------------------------------------ montagem

def tags(itens, classe=""):
    c = f"tag {classe}".strip()
    return "".join(f'<span class="{c}">{html.escape(str(i), quote=True)}</span>' for i in itens)


def linha_topico(p, numero):
    lista_tags = tags(p["stack"][:5]) + tags(p["competencias"][:3], "comp")
    return f"""    <a class="topico" href="/blog/{p['slug']}"
       data-ev="abrir-topico" data-alvo="{p['slug']}" data-data="{p['data'].isoformat()}">
      <span class="n">#{numero:02d}</span>
      <span class="titulo">{html.escape(p['titulo'], quote=True)}</span>
      <span class="resumo">{html.escape(p['sub'], quote=True)}</span>
      <span class="quando">{curta(p['data'])}</span>
      <span class="tags">{lista_tags}</span>
      <span class="views" hidden></span>
    </a>"""


def bloco_links(p):
    linhas = []
    if p.get("link"):
        u = url_segura(p["link"])
        rotulo = re.sub(r"^https?://(www\.)?", "", u).rstrip("/")
        linhas.append(
            f"        <div>\n          <dt>no ar</dt>\n"
            f'          <dd><a href="{html.escape(u, quote=True)}" data-ev="link-projeto">'
            f"{html.escape(rotulo, quote=True)}</a></dd>\n        </div>"
        )
    if p.get("repo"):
        u = url_segura(p["repo"])
        rotulo = re.sub(r"^https?://(www\.)?github\.com/", "", u).rstrip("/")
        linhas.append(
            f"        <div>\n          <dt>código</dt>\n"
            f'          <dd><a href="{html.escape(u, quote=True)}" data-ev="link-repo">'
            f"{html.escape(rotulo, quote=True)}</a></dd>\n        </div>"
        )
    return "\n".join(linhas)


def bloco_nav(posts, i):
    """cronologia: o de cima é mais novo. 'anterior' anda pro passado."""
    partes = []
    if i + 1 < len(posts):
        velho = posts[i + 1]
        partes.append(
            f'    <a href="/blog/{velho["slug"]}" data-ev="nav-anterior">◀ {curta(velho["data"])}'
            f'<b>{html.escape(velho["titulo"], quote=True)}</b></a>'
        )
    if i - 1 >= 0:
        novo = posts[i - 1]
        partes.append(
            f'    <a class="dir" href="/blog/{novo["slug"]}" data-ev="nav-proximo">'
            f'{curta(novo["data"])} ▶<b>{html.escape(novo["titulo"], quote=True)}</b></a>'
        )
    if not partes:
        return ""
    return '  <nav class="circuito-nav">\n' + "\n".join(partes) + "\n  </nav>"


def preencher(modelo, campos):
    for chave, valor in campos.items():
        modelo = modelo.replace("{{" + chave + "}}", valor)
    sobrando = re.findall(r"\{\{([A-Z_]+)\}\}", modelo)
    if sobrando:
        raise SystemExit(f"erro: placeholder sem valor no modelo: {set(sobrando)}")
    return modelo


def escrever_sitemap(posts):
    """só as três rotas públicas. posts/ e modelo/ ficam de fora, e o robots.txt repete."""
    urls = ["https://jadistel.com/", "https://jadistel.com/blog"]
    urls += [f"https://jadistel.com/blog/{p['slug']}" for p in posts]
    corpo = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{corpo}\n</urlset>\n",
        encoding="utf-8",
    )


# ----------------------------------------------------------------------- main

def erro(arquivo, msg):
    raise SystemExit(f"erro em {arquivo}: {msg}")


def main():
    if not POSTS.is_dir():
        raise SystemExit("erro: pasta posts/ não existe")

    arquivos = sorted(POSTS.glob("*.md"))
    if not arquivos:
        raise SystemExit("erro: nenhum post em posts/*.md")

    posts = []
    for caminho in arquivos:
        nome = caminho.name
        meta, corpo = ler_frontmatter(caminho.read_text(encoding="utf-8"), nome)
        for obrigatorio in ("slug", "titulo", "sub", "data"):
            if not meta.get(obrigatorio):
                erro(nome, f"frontmatter sem {obrigatorio}")
        if not re.fullmatch(r"[a-z0-9-]+", meta["slug"]):
            erro(nome, f"slug fora do padrão [a-z0-9-]: {meta['slug']!r}")
        posts.append({
            "slug": meta["slug"],
            "titulo": meta["titulo"],
            "sub": meta["sub"],
            "data": ler_data(meta["data"], nome),
            "stack": meta.get("stack", []),
            "competencias": meta.get("competencias", []),
            "link": meta.get("link", ""),
            "repo": meta.get("repo", ""),
            "corpo": markdown(corpo, nome),
        })

    duplicados = {p["slug"] for p in posts if [q["slug"] for q in posts].count(p["slug"]) > 1}
    if duplicados:
        raise SystemExit(f"erro: slug repetido: {duplicados}")

    # mais recente no topo. o número do tópico cresce com o tempo, como em fórum
    posts.sort(key=lambda p: (p["data"], p["slug"]), reverse=True)
    total = len(posts)

    modelo_indice = (MODELO / "indice.html").read_text(encoding="utf-8")
    modelo_post = (MODELO / "post.html").read_text(encoding="utf-8")

    indice = preencher(modelo_indice, {
        "V": VERSAO,
        "CONTAGEM": f"{total} registro" + ("s" if total != 1 else ""),
        "CIRCUITOS": bloco_circuitos(posts),
        "TOPICOS": "\n".join(linha_topico(p, total - i) for i, p in enumerate(posts)),
    })
    (RAIZ / "blog.html").write_text(indice, encoding="utf-8")

    SAIDA_POSTS.mkdir(exist_ok=True)

    # apagar um .md tem que tirar a página do ar. sem isso o post some do índice
    # e continua servido pela url direta
    vivos = {f"{p['slug']}.html" for p in posts}
    for orfao in SAIDA_POSTS.glob("*.html"):
        if orfao.name not in vivos:
            orfao.unlink()
            print(f"  removido: blog/{orfao.name}")

    for i, p in enumerate(posts):
        pagina = preencher(modelo_post, {
            "V": VERSAO,
            "SLUG": p["slug"],
            "TITULO": html.escape(p["titulo"], quote=True),
            "SUB": html.escape(p["sub"], quote=True),
            "DESC": html.escape(f"{p['titulo']}: {p['sub']}", quote=True),
            "DATA_LONGA": longa(p["data"]),
            "STACK": tags(p["stack"]),
            "COMPETENCIAS": tags(p["competencias"], "comp"),
            "LINKS": bloco_links(p),
            "CORPO": p["corpo"],
            "NAV": bloco_nav(posts, i),
        })
        (SAIDA_POSTS / f"{p['slug']}.html").write_text(pagina, encoding="utf-8")

    escrever_sitemap(posts)

    print(f"blog.html + {total} post(s) em blog/ + sitemap.xml")
    for i, p in enumerate(posts):
        print(f"  #{total - i:02d}  {p['data']}  {p['slug']}")


if __name__ == "__main__":
    sys.exit(main())
