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

VERSAO = "1"  # cache buster do forum.css

MES_FORUM = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

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


def data_forum(d):
    """o formato que o phpBB imprimia: 15 Ago 2026."""
    return f"{d.day:02d} {MES_FORUM[d.month - 1]} {d.year}"


def mes_ano(d):
    return f"{MES_FORUM[d.month - 1]} {d.year}"


# ------------------------------------------------------------------ montagem

def marcas(itens):
    return "".join(
        f'<span class="marca-item">{html.escape(str(i), quote=True)}</span>' for i in itens
    )


def linha_topico(p):
    """uma linha da tabela do índice. sem coluna de respostas e sem 'última mensagem':
    as duas gritam vazio ou abandono, que é o que não pode aparecer."""
    return f"""      <tr>
        <td class="assunto">
          <span class="pasta" aria-hidden="true"></span><a class="titulo" href="/blog/{p['slug']}">{html.escape(p['titulo'], quote=True)}</a>
          <span class="resumo">{html.escape(p['sub'], quote=True)}</span>
          <span class="marcas">{marcas(p['stack'][:6])}</span>
        </td>
        <td class="autor esconde-estreito">joshazze</td>
        <td class="data esconde-estreito">{data_forum(p['data'])}</td>
      </tr>"""


def bloco_links(p):
    linhas = []
    if p.get("link"):
        u = url_segura(p["link"])
        rotulo = re.sub(r"^https?://(www\.)?", "", u).rstrip("/")
        linhas.append(f'              <dt>No ar</dt><dd><a href="{html.escape(u, quote=True)}">'
                      f"{html.escape(rotulo, quote=True)}</a></dd>")
    if p.get("repo"):
        u = url_segura(p["repo"])
        rotulo = re.sub(r"^https?://(www\.)?github\.com/", "", u).rstrip("/")
        linhas.append(f'              <dt>Código</dt><dd><a href="{html.escape(u, quote=True)}">'
                      f"{html.escape(rotulo, quote=True)}</a></dd>")
    return "\n".join(linhas)


def bloco_nav(posts, i):
    """paginação de fórum. a lista desce do mais novo pro mais velho, então
    'anterior' anda pro passado."""
    esq = dir_ = ""
    if i + 1 < len(posts):
        v = posts[i + 1]
        esq = (f'<a href="/blog/{v["slug"]}">&laquo; Tópico anterior: '
               f'{html.escape(v["titulo"], quote=True)}</a>')
    if i - 1 >= 0:
        n = posts[i - 1]
        dir_ = (f'<a href="/blog/{n["slug"]}">Próximo tópico: '
                f'{html.escape(n["titulo"], quote=True)} &raquo;</a>')
    if not esq and not dir_:
        return ""
    return ('  <p class="rodape-info">\n'
            f"    <span>{esq}</span>\n"
            f"    <span>{dir_}</span>\n"
            "  </p>")


def preencher(modelo, campos):
    for chave, valor in campos.items():
        modelo = modelo.replace("{{" + chave + "}}", valor)
    sobrando = re.findall(r"\{\{([A-Z_]+)\}\}", modelo)
    if sobrando:
        raise SystemExit(f"erro: placeholder sem valor no modelo: {set(sobrando)}")
    return modelo


def escrever_sitemap(posts):
    """só as três rotas públicas. posts/ e modelo/ ficam de fora, e o robots.txt repete."""
    urls = ["https://jadistel.com/", "https://jadistel.com/producao",
            "https://jadistel.com/blog"]
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
        "CONTAGEM": f"{total} tópico" + ("s" if total != 1 else ""),
        "TOPICOS": "\n".join(linha_topico(p) for p in posts),
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
            "DATA": data_forum(p["data"]),
            "MEMBRO_DESDE": mes_ano(posts[-1]["data"]),
            "TOTAL": str(total),
            "STACK": marcas(p["stack"]),
            "COMPETENCIAS": marcas(p["competencias"]),
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
