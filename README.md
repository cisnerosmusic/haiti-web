# Ramón Haití Filiu · web de artista

Sitio del pintor y escultor cubano **Ramón Eduardo Haití Filiu** (La Habana, 1971), que vive y trabaja en Bergen, Noruega. Dominio previsto: ramonhaitifiliu.com.

## Estado

**Fase de diseño.** Lo publicado aquí son maquetas de trabajo, marcadas `noindex`; no son la web final.

| Ruta | Qué es |
|------|--------|
| `/` | Índice de maquetas |
| `/maquetas/luz.html` | Parte 2, mundo visual: tres luces para la casa y la ficha de una obra |

## Decisiones tomadas

- **Propósito:** presentación profesional (portafolio, CV y dossier para galerías, curadores, bienales y encargos). Las compras se atienden por consulta; no hay tienda.
- **Idiomas:** inglés en la raíz (`x-default`), noruego bokmål en `/no/` y español en `/es/`, con rutas traducidas y `hreflang` recíproco. Los títulos de obra se publican como los escribió el artista.
- **Mundo visual:** "Luz del norte". Marco claro y frío, sin color propio: el único color es la obra.
- **Salas:** Portada, Obra (una página por cuadro), Murales y encargos, De La Habana a Bergen, CV con dossier en PDF, Contacto. Escultura entra cuando haya material fotográfico.
- **Técnica:** sitio estático en HTML, CSS y JS propios, sin dependencias; fichas de obra generadas desde manifiestos JSON; JSON-LD `Person` y `VisualArtwork`, sitemap, `llms.txt`.

## Derechos

Obras e imágenes de obra: © Ramón Eduardo Haití Filiu. Las imágenes de este repositorio son reducciones para maquetas y no se pueden reutilizar sin su permiso.

Desarrollo: [Index01](https://index01.net), Miami.
