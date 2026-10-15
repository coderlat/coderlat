# Guía del mantenedor: buzón → publicación

```
Colaborador ──fork/PR──▶ coderlat (buzón, aportes/)
                              │  merge a main (tú apruebas)
                              ▼
                  Action "Publicar aporte"
                     │                │
        copia a coderlat-contenido   borra aportes/<slug> del buzón
                     │
                     ▼
        Servidor: git pull + rsync → user/pages/02.blog + clearcache
```

Los forks parten del buzón, que casi siempre está vacío: no arrastran los artículos publicados.
(El historial de git conserva las versiones antiguas de texto; es despreciable. Las imágenes se limitan a 1 MB.)

## Configuración única

1. **Crear el repo de contenido**: `porquero/coderlat-contenido` (puede ser privado). Estructura: `pages/02.blog/<slug>/item.es.md`.
   Mueve ahí tus artículos publicados actuales.
2. **Token (PAT)**: GitHub → Settings → Developer settings → Fine-grained tokens.
   Repositorios: `coderlat` y `coderlat-contenido`. Permiso: *Contents: Read and write*. Caducidad: 90 días o más.
3. **Secreto**: en el repo `coderlat` → Settings → Secrets and variables → Actions → New secret → `PUBLICAR_TOKEN` = el token.
4. **Protección de `main`** (Settings → Branches/Rulesets): exige PR, el check **Validar contenido** y la revisión de CODEOWNERS.
   Permite que los administradores salten la regla (*no marcar* "Do not allow bypassing"), porque la Action empuja con tu token para limpiar el buzón.
5. **Aprobación de workflows** (ver abajo).
6. **Mover tu artículo de prueba**: en tu rama, `git mv pages/02.blog/kanboard-gestion-de-proyectos-kanban-open-source aportes/` y borra `pages/`.

## ¿Se puede evitar aprobar el workflow en cada PR?

GitHub exige aprobación manual la **primera vez** que alguien envía un PR desde un fork. Ajuste: Settings → Actions → General → *Fork pull request workflows from outside collaborators*.
- *Require approval for first-time contributors who are new to GitHub*: pide aprobación solo a cuentas nuevas. Es la opción más cómoda.
- *Require approval for first-time contributors*: a quien nunca ha tenido un PR aceptado.
- *Require approval for all outside collaborators*: siempre (la más estricta).

Con cualquiera de las dos primeras, quien ya tiene un PR aprobado no vuelve a necesitar aprobación. Es seguro relajarlo porque el workflow de validación corre con `pull_request`, permisos de solo lectura y **sin secretos**. No uses `pull_request_target` para evitar la aprobación: ejecutaría código del fork con acceso a secretos.

## Publicar en el servidor

```bash
# Primera vez (repo privado: usa una deploy key de solo lectura)
git clone git@github.com:porquero/coderlat-contenido.git ~/coderlat-contenido

# Cada publicación
cd ~/coderlat-contenido && git pull origin main \
  && rsync -av pages/ /RUTA/AL/SITIO/user/pages/ \
  && cd /RUTA/AL/SITIO && bin/grav clearcache
```

## Qué pasa si algo falla
- **Check "Validar contenido" en rojo**: el detalle indica qué corregir.
- **"Publicar aporte" en rojo**: el aporte queda en `aportes/` (no se borra) y el error aparece en el log. Casos típicos: slug ya publicado por otro autor (se revisa a mano) o archivo no permitido.
- **Token vencido**: renueva el PAT y actualiza el secreto `PUBLICAR_TOKEN`.
