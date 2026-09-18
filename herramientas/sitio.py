"""Genera el sitio completo de Ramón Eduardo Haití Filiu.

Lee datos/ (textos, obras, cv, vistas) e img/manifiesto.json (de imagenes.py)
y escribe todas las páginas en los tres idiomas, más sitemap.xml, robots.txt,
llms.txt y 404.html. Todos los enlaces internos son relativos, así el sitio
funciona igual en el dominio y en una copia local de prueba. Canónicas,
hreflang y sitemap usan siempre el dominio.

Uso:  python herramientas/sitio.py
"""
import datetime
import html
import json
import posixpath
import urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = "https://ramonhaitifiliu.com"
# True desde el lanzamiento (15 sep 2026). En False, todas las páginas salen
# con noindex, por si alguna vez hace falta esconder el sitio.
LANZADO = True
VERSION = "8"  # súbela cada vez que cambien css/ o js/
IDIOMAS = ["en", "no", "es"]
SELECTOR = ["no", "en", "es"]
CORREO = "haitifiliu@yahoo.es"
FACEBOOK = "https://www.facebook.com/RamonHaitiFiliu/"
AMARE = "https://galleriamare.no/eduardo-haiti-filiu-ramon/"
SAMTIDSKUNST = {
    "en": "https://samtidskunst.com/become-better-acquainted-with-the-exciting-artist-ramon-eduardo-haiti-filiu/",
    "no": "https://samtidskunst.com/bli-bedre-kjent-med-den-spennende-kunstneren-ramon-eduardo-haiti-filiu/",
    "es": "https://samtidskunst.com/conociendo-mejor-al-impresionante-artista-ramon-eduardo-haiti-filiu/",
}
PADRE_WIKIDATA = "https://www.wikidata.org/wiki/Q131699504"
INDEXNOW = "50b4bba7fb1994877743ecfcfb601eb9"  # el archivo 50b4bba7fb1994877743ecfcfb601eb9.txt en la raíz demuestra que el sitio es nuestro
GSC = "hfJRBFzE-V4nuhZlSwdddRu3gsEHIV11B_nBc2wO50s"  # verificación de Google Search Console
TONY = "https://antoniolopezsanchez.art"
LIBRO = {"titulo": "The Soul Devoured in Darkness", "titulo_es": "El Alma devorada en la Oscuridad", "isbn": "979-8858149323",
         "url": "https://www.amazon.com/dp/B0CFZH9C75", "kindle": "https://www.amazon.com/dp/B0CGSMSK7T"}
TONY_WEB = {"en": TONY + "/en/", "no": TONY + "/en/", "es": TONY + "/"}


def tony(l):
    """El nombre de Antonio López Sánchez, enlazado a su web en otra pestaña."""
    return f'<a href="{TONY_WEB[l]}" target="_blank" rel="noopener">Antonio López Sánchez</a>'
NOMBRE = "Ramón Eduardo Haití Filiu"
NOMBRE_CORTO = "Ramón Haití Filiu"
HOY = datetime.date.today().isoformat()


def cargar(ruta):
    return json.loads((RAIZ / ruta).read_text(encoding="utf-8"))


T = cargar("datos/textos.json")
O = cargar("datos/obras.json")
CV = cargar("datos/cv.json")
V = cargar("datos/vistas.json")
P = cargar("datos/prensa.json")
M = cargar("img/manifiesto.json")
OBRAS = O["obras"]
esc = lambda s: html.escape(str(s), quote=True)


def ui(l, k):
    return T["ui"][l][k]


def pag(p, l):
    return T["paginas"][p][l]


def loc(v, l):
    return v if isinstance(v, str) else v[l]


def cod(l):
    return T["idiomas"][l]["codigo"]


# ---------- rutas ----------

def url(clave, l, slug=None):
    pre = T["idiomas"][l]["prefijo"]
    if clave == "portada":
        return pre + "/"
    base = f"{pre}/{T['rutas'][clave][l]}/"
    return f"{base}{slug}/" if slug else base


def rel(desde, hacia):
    r = posixpath.relpath(hacia.rstrip("/") or "/", desde.rstrip("/") or "/")
    if hacia.endswith("/"):
        return "./" if r == "." else r + "/"
    return r


def escribir(u, contenido):
    destino = RAIZ / (u.lstrip("/") + "index.html" if u.endswith("/") else u.lstrip("/"))
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")


# ---------- piezas ----------

def picture(desde, tipo, slug, alt, sizes, carga="lazy", prioridad=False, movil=False):
    m = M[tipo][slug]
    anchos = m["anchos"]
    mayor = anchos[-1]
    alto = round(m["alto"] * mayor / m["ancho"])
    medio = anchos[min(1, len(anchos) - 1)]
    def srcset(ext):
        return ", ".join(f"{rel(desde, f'/img/{tipo}/{slug}-{a}.{ext}')} {a}w" for a in anchos)
    fp = ' fetchpriority="high"' if prioridad else ""
    telefono = ""
    if movil and m.get("movil"):
        # En teléfonos, la franja 'movil' (un solo lienzo si es díptico)
        mv = m["movil"]
        def srcset_movil(ext):
            return ", ".join(f"{rel(desde, f'/img/{tipo}/{slug}-movil-{a}.{ext}')} {a}w" for a in mv["anchos"])
        telefono = "".join(f'<source media="{MOVIL}" type="image/{ext}" srcset="{srcset_movil(ext)}" sizes="100vw" '
                           f'width="{mv["ancho"]}" height="{mv["alto"]}">' for ext in ("avif", "webp"))
    return (f'<picture>{telefono}<source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="{rel(desde, f"/img/{tipo}/{slug}-{medio}.webp")}" width="{mayor}" height="{alto}" '
            f'alt="{esc(alt)}" loading="{carga}" decoding="async"{fp}></picture>')


MOVIL = "(max-width: 760px)"  # mismo corte que el CSS


def picture_detalle(desde, slug, alt):
    b = f"/img/obra/{slug}-detalle"
    return (f'<picture><source type="image/avif" srcset="{rel(desde, b + ".avif")}">'
            f'<img src="{rel(desde, b + ".webp")}" width="800" height="800" alt="{esc(alt)}" loading="lazy" decoding="async"></picture>')


def medidas(o, l):
    if o.get("medidas_texto"):
        t = o["medidas_texto"]
    elif o.get("alto"):
        t = f"{o['alto']} × {o['ancho']}"
    else:
        return None
    t = t.replace(",", ".") if l == "en" else t.replace(".", ",")
    return f"{t} cm"


def frase(o, l):
    if o.get("formato") == "diptico":
        que = ui(l, "que_diptico")
    elif o.get("tecnica") == "mixta":
        que = ui(l, "que_mixta")
    elif o.get("tecnica") == "pintura":
        que = ui(l, "que_pintura")
    else:
        que = ui(l, "que_sin")
    cabeza = f'{o["titulo"]}, {o["anio"]}' if o.get("anio") else o["titulo"]
    return ui(l, "frase").format(cabeza=cabeza, que=que)


def aviso_exposicion():
    """La exposición en curso o la próxima, según el CV."""
    for s in CV["secciones"]:
        for it in s["items"]:
            if it.get("hasta") and it["hasta"] >= HOY:
                return it
    return None


def aviso_html(l, clase=""):
    it = aviso_exposicion()
    if not it:
        return ""
    en_curso = it["desde"] <= HOY
    fechas = loc(it.get("fechas", ""), l)
    return (f'<span class="aviso{clase}" data-desde="{it["desde"]}" data-hasta="{it["hasta"]}">'
            f'<span data-estado="ahora"{"" if en_curso else " hidden"}>{ui(l, "ahora")}</span>'
            f'<span data-estado="pronto"{" hidden" if en_curso else ""}>{ui(l, "pronto")}</span>: '
            f'<b>{loc(it["t"], l)}</b>, {fechas}</span>')


# ---------- datos estructurados ----------

def persona(l):
    retrato = M["retrato"]["ramon-haiti-filiu"]
    return {
        "@type": "Person",
        "@id": f"{DOMINIO}/#persona",
        "name": NOMBRE,
        "alternateName": ["Ramon Eduardo Haiti Filiu", "Ramón Haití Filiu", "Ramon Haiti Filiu", "Ramón E. Haití Filiu"],
        "jobTitle": ui(l, "oficio").split(" · ")[0],
        "description": pag("portada", l)["desc"],
        "birthDate": "1971",
        "birthPlace": {"@type": "Place", "name": "Havana, Cuba"},
        "homeLocation": {"@type": "Place", "name": "Bergen, Norway"},
        "nationality": [{"@type": "Country", "name": "Cuba"}, {"@type": "Country", "name": "Norway"}],
        "url": DOMINIO + url("portada", l),
        "image": f"{DOMINIO}/img/retrato/ramon-haiti-filiu-{retrato['anchos'][-1]}.webp",
        "email": f"mailto:{CORREO}",
        "alumniOf": {"@type": "EducationalOrganization", "name": "Academia de Bellas Artes San Alejandro", "address": "Havana, Cuba"},
        "knowsAbout": ["Painting", "Collage", "Mixed media", "Murals"],
        "parent": {"@type": "Person", "name": "Ramón Haití Eduardo", "sameAs": PADRE_WIKIDATA,
                   "description": "Cuban sculptor and painter (b. 1932), member of the Grupo Antillano"},
        "knows": {"@type": "Person", "name": "Antonio López Sánchez", "url": TONY},
        "sameAs": [FACEBOOK, AMARE],
        "subjectOf": [{"@type": "Article", "url": u, "inLanguage": cod(li), "datePublished": "2020",
                        "author": {"@type": "Person", "name": "Wenche Holmedal"},
                        "publisher": {"@type": "Organization", "name": "Samtidskunst"}}
                       for li, u in SAMTIDSKUNST.items()],
    }


def sitio_web():
    return {"@type": "WebSite", "@id": f"{DOMINIO}/#web", "url": DOMINIO + "/", "name": NOMBRE,
            "inLanguage": [cod(l) for l in IDIOMAS], "about": {"@id": f"{DOMINIO}/#persona"}}


def migas(l, pasos):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMINIO + u} for i, (n, u) in enumerate(pasos)]}


def ld(objetos):
    datos = {"@context": "https://schema.org", "@graph": objetos}
    return f'<script type="application/ld+json">{json.dumps(datos, ensure_ascii=False, separators=(",", ":"))}</script>'


# ---------- esqueleto ----------

FLECHA_ABAJO = '<svg class="chevron" viewBox="0 0 12 8" width="12" height="8" aria-hidden="true"><path d="M1 1.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>'
FLECHA_DERECHA = '<svg class="flecha" viewBox="0 0 26 12" width="26" height="12" aria-hidden="true"><path d="M0 6h24M19 1l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>'

MENU = [("obra", "menu_obra"), ("murales", "menu_murales"), ("relato", "menu_relato"), ("cv", "menu_cv"),
        ("prensa", "menu_prensa"), ("contacto", "menu_contacto")]


def cabecera(l, u, clave, slug, portada=False):
    items = "".join(
        f'<li><a href="{rel(u, url(c, l))}"{" aria-current=" + chr(34) + "page" + chr(34) if c == clave else ""}>{ui(l, k)}</a></li>'
        for c, k in MENU)
    idiomas = "".join(
        f'<a href="{rel(u, url(clave, li, slug))}" hreflang="{cod(li)}" lang="{cod(li)}"'
        f'{" aria-current=" + chr(34) + "true" + chr(34) if li == l else ""}>{T["idiomas"][li]["corto"]}</a>'
        for li in SELECTOR)
    nombre = (f'<a class="nombre" href="{rel(u, url("portada", l))}">{NOMBRE_CORTO}'
              f'<small>{ui(l, "oficio")}</small></a>')
    if portada:
        nombre = f'<h1 class="h-nombre">{nombre}</h1>'
    return (f'<header class="cab">{nombre}'
            f'<nav class="menu" aria-label="{ui(l, "nav")}"><ul>{items}</ul>'
            f'<details class="idioma-sel"><summary aria-label="{ui(l, "idioma_actual")}">{T["idiomas"][l]["corto"]}{FLECHA_ABAJO}</summary>'
            f'<div class="idiomas" role="group" aria-label="{ui(l, "idiomas")}">{idiomas}</div></details></nav>'
            f'<details class="menu-movil"><summary>{ui(l, "menu")}</summary><div class="panel">'
            f'<ul>{items}</ul><div class="idiomas" role="group" aria-label="{ui(l, "idiomas")}">{idiomas}</div></div></details>'
            f'</header>')


def pie(l, u, clave, slug):
    idiomas = " · ".join(
        f'<a href="{rel(u, url(clave, li, slug))}" hreflang="{cod(li)}" lang="{cod(li)}">{T["idiomas"][li]["nombre"]}</a>'
        for li in SELECTOR)
    return (f'<footer class="pie"><div class="fila"><span class="luz">{ui(l, "luz")}</span>'
            f'<a href="mailto:{CORREO}">{CORREO}</a><span>{idiomas}</span>'
            f'<span>© {datetime.date.today().year} {NOMBRE} · <a href="https://index01.net">{ui(l, "credito")}</a></span></div></footer>')


def documento(l, u, clave, slug, titulo, desc, cuerpo, objetos, og_img, portada=False):
    alternos = "".join(f'<link rel="alternate" hreflang="{cod(li)}" href="{DOMINIO}{url(clave, li, slug)}">' for li in IDIOMAS)
    alternos += f'<link rel="alternate" hreflang="x-default" href="{DOMINIO}{url(clave, "en", slug)}">'
    robots = "" if LANZADO else '<meta name="robots" content="noindex">'
    ogs = "".join(f'<meta property="og:locale:alternate" content="{T["idiomas"][li]["og"]}">' for li in IDIOMAS if li != l)
    v = f"?v={VERSION}"
    cab = cabecera(l, u, clave, slug, portada)
    if portada:
        cuerpo = cuerpo.replace("{{CABECERA}}", cab)
        cab = ""
    return f"""<!doctype html>
<html lang="{cod(l)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{DOMINIO}{u}">
{alternos}
<meta name="theme-color" content="#E9EAE3">
<meta name="google-site-verification" content="{GSC}">
<meta property="og:type" content="{"profile" if portada else "website"}">
<meta property="og:site_name" content="{NOMBRE}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{DOMINIO}{u}">
<meta property="og:image" content="{DOMINIO}{og_img}">
<meta property="og:locale" content="{T["idiomas"][l]["og"]}">{ogs}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel(u, "/favicon.ico")}" sizes="48x48">
<link rel="icon" href="{rel(u, "/icon-192.png")}" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{rel(u, "/apple-touch-icon.png")}">
<link rel="preload" href="{rel(u, "/fonts/jost-latin.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel(u, "/css/sitio.css")}{v}">
<script src="{rel(u, "/js/luz.js")}{v}"></script>
<script src="{rel(u, "/js/sitio.js")}{v}" defer></script>
{ld(objetos)}
</head>
<body class="pag-{"portada" if portada else clave}">
<a class="salto" href="#contenido">{ui(l, "saltar")}</a>
{cab}{cuerpo}
{pie(l, u, clave, slug)}
</body>
</html>
"""


# ---------- páginas ----------

def tarjeta(l, u, o, sizes):
    return (f'<a href="{rel(u, url("obra", l, o["slug"]))}"><figure>'
            f'{picture(u, "obra", o["slug"], V[o["slug"]][l], sizes)}'
            f'<figcaption><i>{esc(o["titulo"])}</i> {o["anio"] or ""}</figcaption></figure></a>')


SIZES_REJILLA = "(max-width: 700px) 92vw, (max-width: 1100px) 45vw, 400px"


def portada(l):
    u = url("portada", l)
    p = pag("portada", l)
    hero = next(o for o in OBRAS if o.get("portada"))
    resto = [o for o in OBRAS if o is not hero][:6]
    diptico = hero.get("formato") == "diptico"
    ficha_obra = f'{hero["titulo"]}, {hero["anio"]}' if hero.get("anio") else hero["titulo"]
    formato = (ui(l, "diptico") + ", " if diptico else "") + (medidas(hero, l) or "")
    enlace = rel(u, url("obra", l, hero["slug"]))
    # Obra a pantalla completa con los bordes oscurecidos; encima, la cabecera en blanco y los textos del artista
    cuerpo = f"""<div class="escena">
{picture(u, "obra", hero["slug"], V[hero["slug"]][l], "100vw", "eager", True, movil=True)}
<div class="velo" aria-hidden="true"></div>
{{{{CABECERA}}}}
<div class="escena-texto">
<p class="lema">{p["lema"]}</p>
<a class="boton" href="{enlace}">{ui(l, "ver_obra")}{FLECHA_DERECHA}</a>
</div>
<div class="escena-pie">{aviso_html(l)}<p class="escena-ficha"><a href="{enlace}">{esc(ficha_obra)}</a><br>{ui(l, "tecnica_mixta")}<br>{formato}</p></div>
</div>
<main id="contenido">
<section class="declaracion"><p class="disciplinas">{p["disciplinas"]}</p>
<h2>{p["dialogo"]}</h2>
<p class="voz">{p["declaracion"]}</p></section>
<section class="bloque"><div class="intro"><p>{p["intro"]}</p>
<div class="mas"><a class="vermas" href="{rel(u, url("relato", l))}">{pag("relato", l)["h1"]}</a><a href="{rel(u, url("cv", l))}">CV</a><a href="{rel(u, url("contacto", l))}">{ui(l, "menu_contacto")}</a></div></div></section>
<section class="bloque"><div class="cabeza"><h2>{ui(l, "obra_reciente")}</h2></div>
<div class="obras">{"".join(tarjeta(l, u, o, SIZES_REJILLA) for o in resto)}</div>
<p><a class="vermas" href="{rel(u, url("obra", l))}">{ui(l, "toda_obra")}</a></p></section>
</main>"""
    objetos = [sitio_web(), persona(l),
               {"@type": "WebPage", "@id": DOMINIO + u, "url": DOMINIO + u, "name": p["titulo"], "inLanguage": cod(l),
                "isPartOf": {"@id": f"{DOMINIO}/#web"}, "about": {"@id": f"{DOMINIO}/#persona"},
                "primaryImageOfPage": f"{DOMINIO}/img/og/{hero['slug']}.jpg"}]
    escribir(u, documento(l, u, "portada", None, p["titulo"], p["desc"], cuerpo, objetos, f"/img/og/{hero['slug']}.jpg", portada=True))


def indice_obra(l):
    u = url("obra", l)
    p = pag("obra", l)
    cuerpo = f"""<main id="contenido" class="bloque">
<div class="cabeza"><h1>{p["h1"]}</h1><p>{p["lead"]}</p></div>
<div class="obras">{"".join(tarjeta(l, u, o, SIZES_REJILLA) for o in OBRAS)}</div>
</main>"""
    objetos = [{"@type": "CollectionPage", "@id": DOMINIO + u, "url": DOMINIO + u, "name": p["titulo"], "inLanguage": cod(l),
                "isPartOf": {"@id": f"{DOMINIO}/#web"}, "about": {"@id": f"{DOMINIO}/#persona"},
                "mainEntity": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "url": DOMINIO + url("obra", l, o["slug"]), "name": o["titulo"]}
                    for i, o in enumerate(OBRAS)]}},
               migas(l, [(NOMBRE, url("portada", l)), (p["h1"], u)])]
    escribir(u, documento(l, u, "obra", None, p["titulo"], p["desc"], cuerpo, objetos, f"/img/og/{OBRAS[0]['slug']}.jpg"))


def ficha(l, i, o):
    u = url("obra", l, o["slug"])
    s = o["slug"]
    dd = [f'<dt>{ui(l, "anio")}</dt><dd>{o["anio"]}</dd>'] if o.get("anio") else []
    if o.get("tecnica") == "mixta":
        tec = ui(l, "tecnica_mixta")
        if o.get("formato") == "diptico":
            tec = f'{ui(l, "diptico")}, {tec[0].lower() + tec[1:]}'
        dd.append(f'<dt>{ui(l, "tecnica")}</dt><dd>{tec}</dd>')
    elif o.get("tecnica") == "pintura":
        dd.append(f'<dt>{ui(l, "tecnica")}</dt><dd>{ui(l, "tecnica_pintura")}</dd>')
    med = medidas(o, l)
    if med:
        dd.append(f'<dt>{ui(l, "medidas")}</dt><dd>{med}</dd>')
    alt_t = f'<span class="alt"><i>{esc(o["alternativo"])}</i></span>' if o.get("alternativo") else ""
    asunto = urllib.parse.quote(ui(l, "asunto").format(titulo=o["titulo"]))
    texto = frase(o, l)
    detalle = ""
    if M["obra"][s]["detalle"]:
        detalle = (f'<section class="detalle"><p><b>{ui(l, "detalle")}</b>{ui(l, "detalle_nota")}</p>'
                   f'{picture_detalle(u, s, ui(l, "detalle") + ": " + o["titulo"])}</section>')
    vecinas = []
    if i > 0:
        a = OBRAS[i - 1]
        vecinas.append(f'<a rel="prev" href="{rel(u, url("obra", l, a["slug"]))}">{ui(l, "anterior")}: <i>{esc(a["titulo"])}</i></a>')
    else:
        vecinas.append("<span></span>")
    if i < len(OBRAS) - 1:
        b = OBRAS[i + 1]
        vecinas.append(f'<a rel="next" href="{rel(u, url("obra", l, b["slug"]))}">{ui(l, "siguiente")}: <i>{esc(b["titulo"])}</i></a>')
    cuerpo = f"""<main id="contenido" class="bloque">
<p class="miga"><a href="{rel(u, url("obra", l))}">{pag("obra", l)["h1"]}</a></p>
<article class="ficha">
<div class="lienzo">{picture(u, "obra", s, V[s][l], "(max-width: 860px) 92vw, 62vw", "eager", True)}</div>
<div class="cartela"><h1>{esc(o["titulo"])}</h1>{alt_t}
<dl>{"".join(dd)}</dl>
<p>{esc(texto)}</p>
{f'<a class="accion" href="mailto:{CORREO}?subject={asunto}">{ui(l, "consultar")}</a>' if o.get("consultar", True) else ""}</div>
</article>
{detalle}
<nav class="vecinas">{"".join(vecinas)}</nav>
</main>"""
    img = M["obra"][s]
    obra = {"@type": "VisualArtwork", "@id": DOMINIO + url("obra", "en", s) + "#obra", "url": DOMINIO + u,
            "name": o["titulo"], "creator": {"@id": f"{DOMINIO}/#persona"},
            "artform": "Painting", "description": texto, "inLanguage": cod(l),
            "image": f"{DOMINIO}/img/obra/{s}-{img['anchos'][-1]}.webp"}
    if o.get("anio"):
        obra["dateCreated"] = str(o["anio"])
    if o.get("alternativo"):
        obra["alternateName"] = o["alternativo"]
    if o.get("tecnica") == "mixta":
        obra["artMedium"] = "Mixed media"
        obra["artworkSurface"] = "Canvas"
    if o.get("alto"):
        obra["height"] = {"@type": "QuantitativeValue", "value": o["alto"], "unitCode": "CMT"}
        obra["width"] = {"@type": "QuantitativeValue", "value": o["ancho"], "unitCode": "CMT"}
    objetos = [obra, migas(l, [(NOMBRE, url("portada", l)), (pag("obra", l)["h1"], url("obra", l)), (o["titulo"], u)])]
    cabeza = f'{o["titulo"]} ({o["anio"]})' if o.get("anio") else o["titulo"]
    titulo = f'{cabeza} · {ui(l, "obra_de")} {NOMBRE_CORTO}'
    escribir(u, documento(l, u, "obra", s, titulo, texto, cuerpo, objetos, f"/img/og/{s}.jpg"))


def lista_cv(l, u, items):
    filas = []
    for it in items:
        t = loc(it["t"], l)
        if it.get("enlace"):
            t = f'<a href="{it["enlace"]}" target="_blank" rel="noopener">{t}</a>'
        extra = f' <span class="solo">· {ui(l, "solo")}</span>' if it.get("solo") else ""
        if it.get("fechas"):
            extra += f' <span class="solo">· {loc(it["fechas"], l)}</span>'
        filas.append(f'<li><span class="anio">{it["anio"]}</span><span>{t}{extra}</span></li>')
    return f'<ol>{"".join(filas)}</ol>'


def murales(l):
    u = url("murales", l)
    p = pag("murales", l)
    m = O["murales"][0]
    encargos = next(s for s in CV["secciones"] if s["id"] == "encargos")
    libros = [("trovadoras", "Trovadoras", "trovadoras-cubierta.webp", 640, 935, "Editorial Oriente, 2008"),
              ("convertida-en-cancion", "Convertida en canción", "convertida-cubierta.webp", 640, 984, "Editorial Capiro, 2019")]
    cubiertas = "".join(
        f'<figure><a href="{ui(l, "tony_url")[k]}" target="_blank" rel="noopener"><img src="{rel(u, "/img/libros/" + f)}" width="{w}" height="{h}" '
        f'alt="{esc(ui(l, "cubierta_alt").format(libro=t))}" loading="lazy" decoding="async"></a>'
        f'<figcaption><i>{t}</i>{tony(l)} · {ed}</figcaption></figure>'
        for k, t, f, w, h, ed in libros)
    cuerpo = f"""<main id="contenido" class="bloque">
<div class="cabeza"><h1>{p["h1"]}</h1><p>{p["lead"].replace("{tony}", tony(l))}</p></div>
<div class="mural">{picture(u, "mural", m["slug"], V[m["slug"]][l], "(max-width: 860px) 92vw, 62vw", "eager", True)}
<p class="cartela-min"><i>{m["titulo"]}</i> {ui(l, "mural")}, {m["medidas_texto"]}</p></div>
<h2 style="margin-bottom:24px">{ui(l, "cubiertas")}</h2>
<div class="cubiertas">{cubiertas}</div>
<h2 style="margin-bottom:24px">{ui(l, "libro")}</h2>
<div class="libro"><p class="libro-titulo"><i>{LIBRO["titulo"]}</i><i lang="es">{LIBRO["titulo_es"]}</i></p>
<p>{ui(l, "libro_nota")}</p><p class="libro-ficha">{ui(l, "libro_ficha")} · ISBN {LIBRO["isbn"]}</p>
<p>{fuera(LIBRO["url"], ui(l, "libro_enlace"))}</p></div>
<h2 style="margin-bottom:24px">{ui(l, "cuencos")}</h2>
<div class="cuencos">{"".join(picture(u, "cuenco", c["slug"], V[c["slug"]][l], "(max-width: 700px) 92vw, 45vw") for c in O.get("cuencos", []))}</div>
<section class="cv"><div><h2>{ui(l, "cronologia")}</h2>{lista_cv(l, u, encargos["items"])}</div></section>
</main>"""
    objetos = [{"@type": "CollectionPage", "@id": DOMINIO + u, "url": DOMINIO + u, "name": p["titulo"], "inLanguage": cod(l),
                "isPartOf": {"@id": f"{DOMINIO}/#web"}, "about": {"@id": f"{DOMINIO}/#persona"}},
               {"@type": "Book", "@id": f"{DOMINIO}/#libro", "name": f'{LIBRO["titulo"]} & {LIBRO["titulo_es"]}',
                "author": {"@id": f"{DOMINIO}/#persona"}, "illustrator": {"@id": f"{DOMINIO}/#persona"},
                "isbn": LIBRO["isbn"].replace("-", ""), "numberOfPages": 72, "datePublished": "2023-08-21",
                "bookFormat": "https://schema.org/Paperback", "inLanguage": ["en", "es"],
                "url": LIBRO["url"], "sameAs": [LIBRO["kindle"]]},
               migas(l, [(NOMBRE, url("portada", l)), (p["h1"], u)])]
    escribir(u, documento(l, u, "murales", None, p["titulo"], p["desc"], cuerpo, objetos, f"/img/og/{OBRAS[0]['slug']}.jpg"))


def relato(l):
    u = url("relato", l)
    p = pag("relato", l)
    secciones = "".join(f'<h2>{s["h2"]}</h2>' + "".join(f"<p>{x}</p>" for x in s["p"]) for s in p["secciones"])
    cuerpo = f"""<main id="contenido" class="bloque">
<div class="relato">
<figure>{picture(u, "retrato", "ramon-haiti-filiu", V["ramon-haiti-filiu"][l], "(max-width: 860px) 80vw, 36vw", "eager")}<figcaption>{ui(l, "retrato_pie")}</figcaption></figure>
<div class="texto"><h1>{p["h1"]}</h1>{secciones}</div>
</div>
</main>"""
    objetos = [{"@type": "ProfilePage", "@id": DOMINIO + u, "url": DOMINIO + u, "name": p["titulo"], "inLanguage": cod(l),
                "isPartOf": {"@id": f"{DOMINIO}/#web"}, "mainEntity": persona(l)},
               migas(l, [(NOMBRE, url("portada", l)), (p["h1"], u)])]
    escribir(u, documento(l, u, "relato", None, p["titulo"], p["desc"], cuerpo, objetos, "/img/og/ramon-haiti-filiu.jpg"))


def cv(l):
    u = url("cv", l)
    p = pag("cv", l)
    bloques = "".join(f'<div><h2>{s["titulo"][l]}</h2>{lista_cv(l, u, s["items"])}</div>' for s in CV["secciones"])
    cuerpo = f"""<main id="contenido" class="bloque">
<div class="cabeza"><h1>{p["h1"]}</h1><p>{p["lead"]}</p></div>
<div class="cv">{bloques}</div>
</main>"""
    objetos = [{"@type": "ProfilePage", "@id": DOMINIO + u, "url": DOMINIO + u, "name": p["titulo"], "inLanguage": cod(l),
                "isPartOf": {"@id": f"{DOMINIO}/#web"}, "mainEntity": {"@id": f"{DOMINIO}/#persona"}},
               migas(l, [(NOMBRE, url("portada", l)), (p["h1"], u)])]
    escribir(u, documento(l, u, "cv", None, p["titulo"], p["desc"], cuerpo, objetos, "/img/og/ramon-haiti-filiu.jpg"))


MESES = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
         "no": ["jan.", "feb.", "mars", "apr.", "mai", "juni", "juli", "aug.", "sep.", "okt.", "nov.", "des."],
         "es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]}


def fecha_txt(f, l):
    if len(f) == 4:
        return f
    a, m, d = f.split("-")
    mes = MESES[l][int(m) - 1]
    return f"{int(d)}. {mes} {a}" if l == "no" else f"{int(d)} {mes} {a}"


def fuera(href, texto):
    """Enlace externo: siempre en otra pestaña."""
    return f'<a href="{href}" target="_blank" rel="noopener">{texto}</a>'


def prensa(l):
    u = url("prensa", l)
    p = pag("prensa", l)
    rotulo_acceso = {"abierto": p["abierto"], "restringido": p["restringido"], "pago": p["pago"]}
    arts = sorted(P["articulos"], key=lambda a: a["fecha"], reverse=True)
    anios = sorted({a["fecha"][:4] for a in arts}, reverse=True)
    bloques, noticias = [], []
    for anio in anios:
        filas = []
        for a in (x for x in arts if x["fecha"][:4] == anio):
            enlace = a.get("url") or f"https://www.nb.no/items/{a['urn']}"
            leer = p["leer_web"] if a.get("url") else p["leer"]
            titular = f'<i class="titular" lang="no">{esc(a["titular"])}</i>' if a.get("titular") else ""
            autor = f' · {esc(a["autor"])}' if a.get("autor") else ""
            filas.append(f'<li><span class="anio">{fecha_txt(a["fecha"], l)}</span><div>'
                         f'<p class="medio"><b>{esc(a["medio"])}</b>{autor}</p>{titular}<p>{a["resumen"][l]}</p>'
                         f'<p class="fuente">{fuera(enlace, leer)}<span class="acceso">{rotulo_acceso[a["acceso"]]}</span></p></div></li>')
            n = {"@type": "Book" if a.get("libro") else "NewsArticle",
                 "headline": a.get("titular") or f'{a["medio"]}, {a["fecha"]}', "url": enlace,
                 "datePublished": a["fecha"], "inLanguage": "no", "about": {"@id": f"{DOMINIO}/#persona"},
                 "publisher": {"@type": "Organization", "name": a["medio"]}}
            if a.get("autor"):
                n["author"] = {"@type": "Person", "name": a["autor"]}
            noticias.append(n)
        bloques.append(f'<section><h2>{anio}</h2><ol>{"".join(filas)}</ol></section>')
    otros = []
    for t in P["textos"]:
        titulo = f'<i class="titular">{esc(t["titulo"][l])}</i>' if t.get("titulo") else ""
        autor = f' · {esc(t["autor"])}' if t.get("autor") else ""
        enlaces = " · ".join(fuera(loc(e["url"], l), e["rotulo"][l]) for e in t["enlaces"])
        otros.append(f'<li><span class="anio">{t["anio"]}</span><div><p class="medio"><b>{esc(t["medio"])}</b>{autor}</p>'
                     f'{titulo}<p>{t["resumen"][l]}</p><p class="fuente">{enlaces}</p></div></li>')
    trad = f'<p class="trad">{p["cita_trad"]}</p>' if p["cita_trad"] else ""
    cuerpo = f"""<main id="contenido" class="bloque">
<div class="cabeza"><h1>{p["h1"]}</h1><p>{p["lead"]}</p></div>
<blockquote class="cita"><p lang="nn">{esc(P["cita"]["texto"])}</p>{trad}<footer>{p["cita_fuente"]}</footer></blockquote>
<div class="prensa">{"".join(bloques)}
<section><h2>{p["otros"]}</h2><ol>{"".join(otros)}</ol></section></div>
<p class="nota-prensa">{p["leyenda"]} {p["derechos"]}</p>
</main>"""
    objetos = [{"@type": "CollectionPage", "@id": DOMINIO + u, "url": DOMINIO + u, "name": p["titulo"], "inLanguage": cod(l),
                "isPartOf": {"@id": f"{DOMINIO}/#web"}, "about": {"@id": f"{DOMINIO}/#persona"},
                "mainEntity": {"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "item": n} for i, n in enumerate(noticias)]}},
               migas(l, [(NOMBRE, url("portada", l)), (p["h1"], u)])]
    escribir(u, documento(l, u, "prensa", None, p["titulo"], p["desc"], cuerpo, objetos, "/img/og/ramon-haiti-filiu.jpg"))


def contacto(l):
    u = url("contacto", l)
    p = pag("contacto", l)
    cuerpo = f"""<main id="contenido" class="bloque">
<div class="cabeza"><h1>{p["h1"]}</h1><p>{p["lead"]}</p></div>
<div class="contacto">
<a class="correo" href="mailto:{CORREO}">{CORREO}</a>
<dl>
<div><dt>{p["taller"]}</dt><dd>{p["taller_txt"]}</dd></div>
<div><dt>{p["galeria"]}</dt><dd><a href="{AMARE}">Galleri Amare, Stavanger</a></dd></div>
<div><dt>{p["redes"]}</dt><dd><a href="{FACEBOOK}">Facebook</a></dd></div>
</dl>
</div>
</main>"""
    objetos = [{"@type": "ContactPage", "@id": DOMINIO + u, "url": DOMINIO + u, "name": p["titulo"], "inLanguage": cod(l),
                "isPartOf": {"@id": f"{DOMINIO}/#web"}, "about": {"@id": f"{DOMINIO}/#persona"}},
               migas(l, [(NOMBRE, url("portada", l)), (p["h1"], u)])]
    escribir(u, documento(l, u, "contacto", None, p["titulo"], p["desc"], cuerpo, objetos, "/img/og/ramon-haiti-filiu.jpg"))


def pagina_404():
    bloques = "".join(
        f'<section lang="{cod(l)}"><h1>{pag("404", l)["h1"]}</h1><p>{pag("404", l)["p"]} '
        f'<a data-ruta="{url("portada", l)}" href="{url("portada", l)}">{NOMBRE_CORTO}</a></p></section>'
        for l in IDIOMAS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>404 · {NOMBRE_CORTO}</title>
<style>
body {{ margin: 0; background: #E9EAE3; color: #0B0D12; font-family: "Helvetica Neue", Arial, system-ui, sans-serif; line-height: 1.55; }}
main {{ max-width: 640px; margin: 0 auto; padding-block: 16vh 64px; padding-inline: 20px; display: grid; gap: 36px; }}
h1 {{ font-size: 24px; margin: 0 0 6px; }} p {{ margin: 0; }} a {{ color: inherit; }}
</style>
</head>
<body>
<main>{bloques}</main>
<script>
/* En GitHub Pages el sitio vive en /haiti-web/; en el dominio propio, en la raíz */
var base = location.pathname.indexOf("/haiti-web/") === 0 ? "/haiti-web" : "";
document.querySelectorAll("[data-ruta]").forEach(function (a) {{ a.href = base + a.getAttribute("data-ruta"); }});
</script>
</body>
</html>
"""


# ---------- archivos de raíz ----------

def todas_las_rutas():
    rutas = [("portada", None), ("obra", None)] + [("obra", o["slug"]) for o in OBRAS]
    rutas += [("murales", None), ("relato", None), ("cv", None), ("prensa", None), ("contacto", None)]
    return rutas


def sitemap():
    filas = []
    for clave, slug in todas_las_rutas():
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{cod(li)}" href="{DOMINIO}{url(clave, li, slug)}"/>' for li in IDIOMAS)
        alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{DOMINIO}{url(clave, "en", slug)}"/>'
        for l in IDIOMAS:
            filas.append(f"<url><loc>{DOMINIO}{url(clave, l, slug)}</loc><lastmod>{HOY}</lastmod>{alt}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(filas) + "\n</urlset>\n")


def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    return ("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
            + f"Sitemap: {DOMINIO}/sitemap.xml\n")


def llms():
    obras = "\n".join(f"- [{o['titulo']}]({DOMINIO}{url('obra', 'en', o['slug'])}): {frase(o, 'en')}" for o in OBRAS)
    return f"""# {NOMBRE}

> Cuban-Norwegian painter, born in Havana in 1971 and based in Bergen, Norway, since 2009. Works in mixed media on canvas: oil and acrylic with collage of printed fabric, jute and corrugated cardboard.

Key facts:
- Education: Paulita Concepción art school, Havana (1984); San Alejandro Academy of Fine Arts, Havana (1992–1996); bronze casting course (1997).
- Taught sculpture at the José Antonio Díaz Peláez art school in Havana.
- Exhibited at the 10th (2012) and 15th (2024–2025) Havana Biennial, at Kunsthuset Wendelboe (Bergen), Galleri Amare (Stavanger) and Hardanger Kulturgalleri.
- Murals and the 2017 festival poster for Nattjazz, Bergen. Cover illustrations for the Cuban writer Antonio López Sánchez.
- Author and illustrator of the bilingual illustrated book "{LIBRO['titulo']} & {LIBRO['titulo_es']}" (2023, ISBN {LIBRO['isbn']}): {LIBRO['url']}
- Work in the collections of the Grieg Foundation (Bergen), Universitetet i Nordland and Nordland psykiatriske sykehus (Bodø).
- Not to be confused with his father, the Cuban sculptor Ramón Haití Eduardo (b. 1932), member of the Grupo Antillano ({PADRE_WIKIDATA}). Awards and 1960s studies attributed online to "Ramón Haití" belong to the father.
- Contact: {CORREO}

## Sources
- Wenche Holmedal, "Become better acquainted with the exciting artist Ramon Eduardo Haiti Filiu", Samtidskunst, 2020: the longest published profile, with his technique, themes and background. English: {SAMTIDSKUNST['en']} · Norwegian: {SAMTIDSKUNST['no']} · Spanish: {SAMTIDSKUNST['es']}
- Galleri Amare (Stavanger), CV and exhibition pages: {AMARE}
- Kunsthuset Wendelboe (Bergen), 2019 catalogue and exhibition text.
- National Library of Norway: 32 press pieces from 2006 onwards, listed at {DOMINIO}{url('prensa', 'en')}

## Pages
- [Home]({DOMINIO}/)
- [Works]({DOMINIO}{url('obra', 'en')})
- [Other work: murals, posters, book covers and his illustrated book]({DOMINIO}{url('murales', 'en')})
- [From Havana to Bergen]({DOMINIO}{url('relato', 'en')}): biography
- [CV]({DOMINIO}{url('cv', 'en')})
- [Press]({DOMINIO}{url('prensa', 'en')}): {len(P['articulos'])} pieces in the Norwegian press since 2006 (Avisa Nordland, Bergensavisen, Bergens Tidende, Klassekampen, Firda and others), with links to the National Library of Norway
- [Contact]({DOMINIO}{url('contacto', 'en')})
- Norwegian: {DOMINIO}/no/ · Spanish: {DOMINIO}/es/

## Works
{obras}
"""


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs><linearGradient id="c" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0B1735"/><stop offset=".55" stop-color="#8C7BA8"/><stop offset="1" stop-color="#F5D494"/>
</linearGradient></defs>
<rect width="64" height="64" rx="12" fill="url(#c)"/>
<circle cx="32" cy="45" r="7" fill="#F6F4ED"/>
</svg>
"""


def favicons():
    (RAIZ / "favicon.svg").write_text(FAVICON_SVG, encoding="utf-8")
    from PIL import Image, ImageDraw
    def icono(n):
        im = Image.new("RGB", (n, n))
        d = ImageDraw.Draw(im)
        paradas = [(0, (11, 23, 53)), (0.55, (140, 123, 168)), (1, (245, 212, 148))]
        for y in range(n):
            t = y / (n - 1)
            for (t0, c0), (t1, c1) in zip(paradas, paradas[1:]):
                if t0 <= t <= t1:
                    k = (t - t0) / (t1 - t0)
                    d.line([(0, y), (n, y)], fill=tuple(round(a + (b - a) * k) for a, b in zip(c0, c1)))
                    break
        r = n * 7 / 64
        cx, cy = n / 2, n * 45 / 64
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(246, 244, 237))
        return im
    icono(180).save(RAIZ / "apple-touch-icon.png")
    icono(48).save(RAIZ / "favicon.ico", sizes=[(48, 48), (32, 32), (16, 16)])


def main():
    for l in IDIOMAS:
        portada(l)
        indice_obra(l)
        for i, o in enumerate(OBRAS):
            ficha(l, i, o)
        murales(l)
        relato(l)
        cv(l)
        prensa(l)
        contacto(l)
    (RAIZ / "404.html").write_text(pagina_404(), encoding="utf-8")
    (RAIZ / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (RAIZ / "robots.txt").write_text(robots(), encoding="utf-8")
    (RAIZ / "llms.txt").write_text(llms(), encoding="utf-8")
    (RAIZ / ".nojekyll").write_text("", encoding="utf-8")
    # Los iconos (favicon.ico, icon-192/512, apple-touch-icon) salen de herramientas/favicon.py
    total = len(todas_las_rutas()) * len(IDIOMAS)
    print(f"{total} páginas en {len(IDIOMAS)} idiomas · LANZADO={LANZADO}")


if __name__ == "__main__":
    main()
