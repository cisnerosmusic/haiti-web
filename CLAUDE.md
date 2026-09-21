# Ramón Haití Filiu · contexto para IA

Sitio de artista generado desde datos y **publicado en https://ramonhaitifiliu.com**: lo que se empuja se ve. Lee [README.md](README.md) antes de tocar nada y [PENDIENTES.md](PENDIENTES.md) para lo que falta.

- Nunca editar HTML a mano: se cambia `datos/` o `herramientas/` y se regenera con `python herramientas/sitio.py`.
- Nunca editar texto con Get-Content/Set-Content de PowerShell (rompe el UTF-8): usar herramientas de edición de archivos.
- Sin raya larga en textos públicos. Títulos de obra sin traducir.
- No publicar datos sin fuente: si algo no está verificado, va a PENDIENTES.md.
- **El artista vive y trabaja en Bergen, y así se cuenta siempre.** Ningún texto, dato ni metadato lo sitúa en otra ciudad o país; ante la duda, se consulta a Ernesto antes de publicar.
- Tras publicar páginas nuevas: `python herramientas/indexnow.py`.
- El artista no es su padre, el escultor Ramón Haití Eduardo (Wikidata Q131699504). No mezclar premios ni fechas.
- Antes de publicar: `grep` de raya larga, regenerar, revisar en el navegador (servidor local: `python -m http.server 8420`).
