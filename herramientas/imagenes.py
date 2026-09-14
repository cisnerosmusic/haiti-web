"""Genera las imágenes publicables a partir de los originales.

Lee datos/obras.json y escribe en img/:
  obra/<slug>-<ancho>.avif|webp   (anchos 640, 1200, 1800; nunca amplía)
  obra/<slug>-detalle.avif|webp   (recorte 1:1 de 800 px alrededor de 'foco')
  mural/<slug>-<ancho>.avif|webp
  retrato/<slug>-<ancho>.avif|webp
  og/<slug>.jpg                   (1200 px, para compartir en redes)
y deja img/manifiesto.json con medidas reales, que lee el generador del sitio.

Los originales viven en OneDrive (no en git). Carpeta por defecto abajo;
se puede cambiar con la variable de entorno RH_ORIGINALES.
Uso:  python herramientas/imagenes.py [--forzar]
"""
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ORIGINALES = Path(os.environ.get("RH_ORIGINALES", r"C:\Users\Ernesto\OneDrive\Imágenes\Haití"))
SALIDA = RAIZ / "img"
ANCHOS_OBRA = [640, 1200, 1800]
ANCHOS_RETRATO = [480, 960]
DETALLE = 800
FORZAR = "--forzar" in sys.argv


def ruta_fuente(rel):
    if rel.startswith("@proyecto/"):
        return RAIZ / rel[len("@proyecto/"):]
    return ORIGINALES / rel


def abrir(ruta):
    im = Image.open(ruta)
    im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


def guardar(im, base):
    base.parent.mkdir(parents=True, exist_ok=True)
    avif, webp = base.with_suffix(".avif"), base.with_suffix(".webp")
    if FORZAR or not avif.exists():
        im.save(avif, quality=50, speed=6)
    if FORZAR or not webp.exists():
        im.save(webp, quality=72, method=6)


def escalas(im, carpeta, slug, anchos):
    ancho, alto = im.size
    hechos = []
    for a in anchos:
        if a > ancho and hechos:
            continue
        a = min(a, ancho)
        copia = im.resize((a, round(alto * a / ancho)), Image.LANCZOS)
        guardar(copia, SALIDA / carpeta / f"{slug}-{a}")
        hechos.append(a)
    return hechos


def og(im, slug):
    destino = SALIDA / "og" / f"{slug}.jpg"
    if destino.exists() and not FORZAR:
        return
    destino.parent.mkdir(parents=True, exist_ok=True)
    ancho, alto = im.size
    a = min(1200, ancho)
    im.resize((a, round(alto * a / ancho)), Image.LANCZOS).save(destino, quality=82, optimize=True, progressive=True)


def detalle(im, slug, foco):
    ancho, alto = im.size
    if not foco or min(ancho, alto) < 1600:
        return False
    cx, cy = foco[0] * ancho, foco[1] * alto
    x = int(min(max(cx - DETALLE / 2, 0), ancho - DETALLE))
    y = int(min(max(cy - DETALLE / 2, 0), alto - DETALLE))
    guardar(im.crop((x, y, x + DETALLE, y + DETALLE)), SALIDA / "obra" / f"{slug}-detalle")
    return True


def main():
    datos = json.loads((RAIZ / "datos" / "obras.json").read_text(encoding="utf-8"))
    manifiesto = {"obra": {}, "mural": {}, "retrato": {}, "cuenco": {}}

    for o in datos["obras"]:
        im = abrir(ruta_fuente(o["fuente"]))
        manifiesto["obra"][o["slug"]] = {
            "ancho": im.size[0], "alto": im.size[1],
            "anchos": escalas(im, "obra", o["slug"], ANCHOS_OBRA),
            "detalle": detalle(im, o["slug"], o.get("foco")),
        }
        og(im, o["slug"])
        print("obra", o["slug"], im.size)

    for m in datos["murales"]:
        im = abrir(ruta_fuente(m["fuente"]))
        manifiesto["mural"][m["slug"]] = {"ancho": im.size[0], "alto": im.size[1],
                                          "anchos": escalas(im, "mural", m["slug"], ANCHOS_OBRA)}
        print("mural", m["slug"], im.size)

    for c in datos.get("cuencos", []):
        im = abrir(ruta_fuente(c["fuente"]))
        if c.get("recorte"):
            im = im.crop(tuple(c["recorte"]))  # misma proporción (3:2) para toda la serie
        manifiesto["cuenco"][c["slug"]] = {"ancho": im.size[0], "alto": im.size[1],
                                           "anchos": escalas(im, "cuenco", c["slug"], [640, 1200])}
        print("cuenco", c["slug"], im.size)

    r = datos["retrato"]
    im = abrir(ruta_fuente(r["fuente"]))
    manifiesto["retrato"][r["slug"]] = {"ancho": im.size[0], "alto": im.size[1],
                                        "anchos": escalas(im, "retrato", r["slug"], ANCHOS_RETRATO)}
    og(im, r["slug"])
    print("retrato", im.size)

    (SALIDA / "manifiesto.json").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
