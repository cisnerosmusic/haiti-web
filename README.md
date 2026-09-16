# Ramón Eduardo Haití Filiu · sitio oficial

Web del pintor cubano-noruego **Ramón Eduardo Haití Filiu** (La Habana, 1971), que vive y trabaja en Bergen. En línea en **https://ramonhaitifiliu.com**.

## La idea

**Luz del norte.** El marco calla para que hable el cuadro: tipografía sobria, cartelas de museo, ningún color propio. El color de fondo lo pone la luz real de Bergen: `js/luz.js` calcula la altura del sol sobre la ciudad y pinta la página, del azul casi negro de la noche al alba y al amarillo verdeazulado de la hora más clara. En la portada la luz es un cielo en degradado, con una aurora casi imperceptible en noche cerrada; en las demás páginas conserva la hora pero pierde el color, para que el único color siga siendo la obra. El texto elige solo la tinta clara u oscura, y ningún fondo con texto cae en la franja de luminancia donde el contraste no alcanza.

Vista previa de cualquier hora: añade `?luz=HH:MM` a una dirección (hora de Bergen, día de hoy).

## Salas

Portada · Obra (una página por cuadro) · Otros (murales, carteles, cubiertas y cuencos pintados) · De La Habana a Bergen · CV · Prensa · Contacto.

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
| `datos/prensa.json` | Prensa verificada y textos de galerías, con su tipo de acceso |
| `herramientas/imagenes.py` | Originales → AVIF y WebP en 640/1200/1800, recortes de detalle, imágenes para redes |
| `herramientas/sitio.py` | Escribe las 90 páginas, `sitemap.xml`, `robots.txt`, `llms.txt` y `404.html` |
| `herramientas/favicon.py` | Marca del artista limpia, favicon, iconos y apple-touch-icon |
| `herramientas/indexnow.py` | Avisa a IndexNow de que el sitio cambió |
| `css/`, `js/`, `fonts/`, `img/` | Recursos publicados |

Al cambiar algo:

```bash
python herramientas/imagenes.py     # solo si hay obra o imagen nueva (--forzar para rehacer todo)
python herramientas/sitio.py        # siempre
```

Si cambia `css/` o `js/`, sube `VERSION` en `herramientas/sitio.py`. Los originales de alta resolución no están en git: viven en OneDrive y en `originales/` (ignorada).

**Añadir una obra:** una entrada en `datos/obras.json`, su texto alternativo en `datos/vistas.json`, y los dos comandos.

## Publicado

En línea desde el 15 de septiembre de 2026 en https://ramonhaitifiliu.com, con certificado de Let's Encrypt y HTTPS forzado. El DNS vive en Hostinger (cuatro registros A a GitHub Pages y el `www` por CNAME al mismo destino) y el dominio está pagado hasta octubre de 2028. Verificado en Google Search Console por etiqueta HTML: **esa etiqueta no se quita nunca**, va en `herramientas/sitio.py`.

El WordPress anterior sigue en el hosting de Hostinger, cerrado con contraseña y sin conexión con el dominio. En su panel **no se debe pulsar "Conectar dominio"**: rehace el DNS y tumba esta web.

Al añadir o cambiar páginas, avisar a IndexNow (Bing, Yandex y otros):

```bash
python herramientas/indexnow.py
```

## Reglas de contenido

- Solo datos verificados: cada línea del CV sale del CV del artista o de fuentes publicadas. Lo dudoso está en [PENDIENTES.md](PENDIENTES.md) hasta que el artista lo confirme.
- Sin raya larga en ningún texto público.
- Se distingue siempre al artista de su padre, el escultor Ramón Haití Eduardo (Grupo Antillano).

## Derechos

Obras e imágenes de obra: © Ramón Eduardo Haití Filiu. No se pueden reutilizar sin su permiso. Cubiertas de *Trovadoras* y *Convertida en canción*: ilustraciones del artista para los libros de Antonio López Sánchez.

Desarrollo: [Index01](https://index01.net), Miami.
