"""Favicon y marca a partir de la marca de agua del artista.

Fuente: originales/marca-de-agua06.jpg (la marca que usaba el WordPress
anterior, a 1600 px; tinta negra sobre blanco). Escribe:
  img/marca/marca.png      la marca limpia, negra sobre transparente
  favicon.ico              16, 32 y 48 px, loseta hueso con la marca
  icon-192.png, icon-512.png
  apple-touch-icon.png     180 px, loseta a sangre (iOS redondea por su cuenta)
Uso: python herramientas/favicon.py
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "originales" / "marca-de-agua06.jpg"
HUESO = (233, 234, 227)
TINTA = (11, 13, 18)


def marca_limpia():
    gris = Image.open(FUENTE).convert("L").filter(ImageFilter.MedianFilter(5))  # fuera motas de escaneo
    alfa = gris.point(lambda v: 255 if v < 128 else 0)
    alfa = alfa.crop(alfa.getbbox())
    tinta = Image.new("RGBA", alfa.size, TINTA + (0,))
    tinta.putalpha(alfa)
    return tinta


def loseta(marca, lado, redondeo=True, ancho_marca=0.84):
    escala = 4  # se dibuja grande y se reduce: bordes limpios
    L = lado * escala
    fondo = Image.new("RGBA", (L, L), (0, 0, 0, 0))
    d = ImageDraw.Draw(fondo)
    if redondeo:
        d.rounded_rectangle([0, 0, L - 1, L - 1], radius=int(L * 0.22), fill=HUESO + (255,))
    else:
        d.rectangle([0, 0, L, L], fill=HUESO + (255,))
    w = int(L * ancho_marca)
    h = round(marca.size[1] * w / marca.size[0])
    m = marca.resize((w, h), Image.LANCZOS)
    fondo.alpha_composite(m, ((L - w) // 2, (L - h) // 2))
    return fondo.resize((lado, lado), Image.LANCZOS)


def main():
    marca = marca_limpia()
    (RAIZ / "img" / "marca").mkdir(parents=True, exist_ok=True)
    ancho = 1200
    marca.resize((ancho, round(marca.size[1] * ancho / marca.size[0])), Image.LANCZOS).save(RAIZ / "img" / "marca" / "marca.png", optimize=True)
    grande = loseta(marca, 256)
    grande.save(RAIZ / "favicon.ico", sizes=[(48, 48), (32, 32), (16, 16)])
    loseta(marca, 192).save(RAIZ / "icon-192.png", optimize=True)
    loseta(marca, 512).save(RAIZ / "icon-512.png", optimize=True)
    loseta(marca, 180, redondeo=False, ancho_marca=0.78).convert("RGB").save(RAIZ / "apple-touch-icon.png", optimize=True)
    print("marca", marca.size, "· favicon.ico, icon-192/512, apple-touch-icon listos")


if __name__ == "__main__":
    main()
