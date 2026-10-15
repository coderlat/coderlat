# Cómo publicar en Coderlat

1. Haz **fork** de este repositorio.
2. Copia `templates/articulo/` a `aportes/<slug-de-tu-articulo>/` (slug en minúsculas, sin tildes, con guiones).
3. Renombra el archivo a `item.es.md` y completa el encabezado (frontmatter) y el texto en Markdown. Imágenes: en la misma carpeta, referenciadas por nombre.
4. Abre un **Pull Request** hacia `main`. La validación automática te dirá si falta algo.
5. Revisamos, pedimos ajustes si hace falta y, al aprobar, **se publica en el sitio automáticamente** y tu carpeta sale de `aportes/` (este repositorio es solo un buzón, por eso es liviano).

> Tip: no necesitas clonar nada. En GitHub, entra a `aportes/` → **Add file → Create new file** y escribe `mi-articulo/item.es.md`; GitHub crea el fork y el PR por ti. Tu PR solo puede tocar archivos dentro de `aportes/`.

Archivos permitidos junto al artículo: `.md`, `.png`, `.jpg`, `.gif`, `.webp`, `.webm`, `.mp4` (máx. 1 MB por imagen, sin subcarpetas).

## Encabezado obligatorio

```yaml
---
title: 'Título claro y específico'
date: '31-12-2026 10:00'      # dd-mm-aaaa hh:mm
author: tu-usuario-github
taxonomy:
    tool: [n8n]               # herramienta principal, en minúsculas
    resource: [tutorial]      # skill, plantilla, tutorial, glosario, automatizacion, ...
    country: [mexico]         # país de origen, sin tildes, en minúsculas
metadata:
    description: 'Resumen de 70 a 160 caracteres'
---
```

Las etiquetas van en minúsculas y sin tildes para que los filtros del sitio no se dupliquen (`n8n` y `N8N` serían filtros distintos).

## Escribe para buscadores y para IA (SEO · AEO · GEO)

- **Título** claro, de hasta ~60 caracteres, con la palabra clave al inicio.
- **`metadata.description`**: 70–160 caracteres. Es lo que se ve en Google, en redes y en la discusión de comentarios.
- **Primer párrafo = respuesta.** Resuelve el problema en 2–3 frases antes de explicar el contexto.
- **Estructura:** empieza en `##` (el título ya es el H1), usa `###` para subtemas, listas y tablas cuando comparas cosas.
- **`faq`**: 2–4 preguntas reales con respuestas de 1–3 frases, que se entiendan sin leer el resto.
- **`sources`**: enlaza documentación oficial y datos que respalden lo que afirmas; las IA citan fuentes verificables.
- **Imágenes** con texto alternativo descriptivo (`![Qué muestra](archivo.png)`).
- **Experiencia propia:** cuenta qué probaste, en qué versión y qué resultado obtuviste. Eso diferencia tu artículo.
- Actualiza `updated: 'dd-mm-aaaa hh:mm'` cuando revises el contenido.

## Criterios editoriales

- Resuelve un problema real, con pasos que otra persona pueda reproducir.
- Es contenido propio o con permiso; cita fuentes y licencias.
- No incluyas credenciales, datos personales ni información de clientes.
- Sin publicidad ni autopromoción encubierta.

## Sin git

Abre un Issue con la plantilla **Proponer solución**; lo convertimos en artículo y te damos el crédito como autor.
