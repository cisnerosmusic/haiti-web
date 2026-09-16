"""Avisa a IndexNow (Bing, Yandex, Naver y otros) de que el sitio cambió.

Lee sitemap.xml, manda todas las direcciones de una vez y muestra la respuesta.
La clave vive en INDEXNOW dentro de sitio.py y en el archivo <clave>.txt de la raíz.
Uso:  python herramientas/indexnow.py
"""
import json
import re
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sitio = (RAIZ / "herramientas" / "sitio.py").read_text(encoding="utf-8")
clave = re.search(r'INDEXNOW = "([^"]+)"', sitio).group(1)
urls = re.findall(r"<loc>([^<]+)</loc>", (RAIZ / "sitemap.xml").read_text(encoding="utf-8"))
datos = {"host": "ramonhaitifiliu.com", "key": clave,
         "keyLocation": f"https://ramonhaitifiliu.com/{clave}.txt", "urlList": urls}
pet = urllib.request.Request("https://api.indexnow.org/indexnow",
                             data=json.dumps(datos).encode("utf-8"),
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(pet) as r:
    print(f"{len(urls)} direcciones enviadas · respuesta {r.status}")
