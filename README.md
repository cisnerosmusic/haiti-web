# Ramón Eduardo Haití Filiu · sitio oficial

Web del pintor y escultor cubano-noruego **Ramón Eduardo Haití Filiu** (La Habana, 1971), que vive y trabaja en Bergen. Dominio: **ramonhaitifiliu.com** (pendiente de apuntar; mientras tanto se ve en [cisnerosmusic.github.io/haiti-web](https://cisnerosmusic.github.io/haiti-web/)).

## La idea

**Luz del norte.** El marco calla para que hable el cuadro: tipografía sobria, cartelas de museo, ningún color propio. El color de fondo lo pone la luz real de Bergen: `js/luz.js` calcula la altura del sol sobre la ciudad y pinta la página, del azul casi negro de la noche al alba y al amarillo verdeazulado de la hora más clara. En la portada la luz es un cielo en degradado, con una aurora casi imperceptible en noche cerrada; en las demás páginas conserva la hora pero pierde el color, para que el único color siga siendo la obra. El texto elige solo la tinta clara u oscura, y ningún fondo con texto cae en la franja de luminancia donde el contraste no alcanza.

Vista previa de cualquier hora: añade `?luz=HH:MM` a una dirección (hora de Bergen, día de hoy).

## Idiomas

Inglés en la raíz (`x-default`), noruego bokmål en `/no/` y español en `/es/`, con rutas traducidas y `hreflang` recíproco. **Los títulos de obra no se traducen**: se publican como los escribió el artista.

## Cómo está hecho

HTML, CSS y JS propios, sin frameworks ni peticiones a terceros (fuentes autohospedadas: Schibsted Grotesk y Newsreader cursiva). Todo el HTML sale de un generador; no se edita a mano.

| Carpeta | Contenido |
|---|---|
| `datos/textos.json` | Todo el texto del sitio en los tres idiomas |
| `datos/obras.json` | Catálogo: título, año, técnica, medidas, original y centro del recorte de detalle |
| `datos/cv.json` | CV por secciones; `desde`/`hasta` activan el aviso de exposición en la portada |
| `datos/vistas.json` | Texto alternativo de cada imagen |
| `herramientas/imagenes.py` | Originales → AVIF y WebP en 640/1200/1800, recortes de detalle, imágenes para redes |
| `herramientas/sitio.py` | Escribe las 51 páginas, `sitemap.xml`, `robots.txt`, `llms.txt`, `404.html` y favicons |
| `css/`, `js/`, `fonts/`, `img/` | Recursos publicados |

Al cambiar algo:

```bash
python herramientas/imagenes.py     # solo si hay obra o imagen nueva (--forzar para rehacer todo)
python herramientas/sitio.py        # siempre
```

Si cambia `css/` o `js/`, sube `VERSION` en `herramientas/sitio.py`. Los originales de alta resolución no están en git: viven en OneDrive y en `originales/` (ignorada).

**Añadir una obra:** una entrada en `datos/obras.json`, su texto alternativo en `datos/vistas.json`, y los dos comandos.

## Lanzamiento

Hoy las páginas llevan `noindex` porque el dominio aún apunta a otro servidor. El día del cambio:

1. Apuntar el DNS de ramonhaitifiliu.com a GitHub Pages.
2. `LANZADO = True` en `herramientas/sitio.py`, crear el archivo `CNAME` y regenerar.
3. Search Console y Bing Webmaster Tools, enviar el sitemap.

## Reglas de contenido

- Solo datos verificados: cada línea del CV sale del CV del artista o de fuentes publicadas. Lo dudoso está en [PENDIENTES.md](PENDIENTES.md) hasta que el artista lo confirme.
- Sin raya larga en ningún texto público.
- Se distingue siempre al artista de su padre, el escultor Ramón Haití Eduardo (Grupo Antillano).

## Derechos

Obras e imágenes de obra: © Ramón Eduardo Haití Filiu. No se pueden reutilizar sin su permiso. Cubiertas de *Trovadoras* y *Convertida en canción*: ilustraciones del artista para los libros de Antonio López Sánchez.

Desarrollo: [Index01](https://index01.net), Miami.
