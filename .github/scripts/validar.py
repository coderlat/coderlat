"""Valida frontmatter de artículos de coderLAT. Uso: validar.py archivo.md ..."""
import re, sys, datetime, pathlib
import yaml

REQUIRED = ["title", "date", "author"]
TAXONOMIAS = ["tool", "resource", "country"]
SLUG = re.compile(r"^[a-z0-9][a-z0-9\-]*$")
MAX_IMG = 1024 * 1024
errores = []

def err(f, m): errores.append(f"{f}: {m}")

for f in sys.argv[1:]:
    p = pathlib.Path(f)
    txt = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        err(f, "falta el encabezado (frontmatter) entre '---'"); continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        err(f, f"YAML inválido: {e}"); continue
    for k in REQUIRED:
        if not fm.get(k): err(f, f"falta '{k}'")
    d = fm.get("date")
    if d and not isinstance(d, datetime.datetime):
        try: datetime.datetime.strptime(str(d), "%d-%m-%Y %H:%M")
        except ValueError: err(f, "'date' debe tener formato dd-mm-aaaa hh:mm")
    tax = fm.get("taxonomy") or {}
    for t in TAXONOMIAS:
        vals = tax.get(t)
        if not vals: err(f, f"falta taxonomy.{t}"); continue
        for v in (vals if isinstance(vals, list) else [vals]):
            if not SLUG.match(str(v)):
                err(f, f"taxonomy.{t}: '{v}' debe ir en minúsculas, sin tildes ni espacios")
    desc = ((fm.get("metadata") or {}).get("description") or "").strip()
    if not desc: err(f, "falta metadata.description (70-160 caracteres)")
    elif not 70 <= len(desc) <= 165: err(f, f"metadata.description mide {len(desc)} caracteres; debe tener entre 70 y 160")
    if not (0 < len(str(fm.get("title", ""))) <= 70): err(f, "el título debe tener entre 1 y 70 caracteres")
    faq = fm.get("faq")
    if faq:
        if not isinstance(faq, list) or any(not isinstance(i, dict) or not i.get("q") or not i.get("a") for i in faq):
            err(f, "faq debe ser una lista de pares q/a completos")
    body = txt.split("---", 2)[-1]
    if re.search(r"^# [^#]", body, re.M): err(f, "no uses '# ' (H1) en el texto: el título ya es el H1; empieza en '## '")
    if not re.search(r"^## ", body, re.M): err(f, "usa al menos un encabezado '## ' para estructurar el artículo")
    if re.search(r"!\[\s*\]\(", body): err(f, "hay imágenes sin texto alternativo: usa ![descripción](archivo.png)")
    # Seguridad: el sitio renderiza HTML del artículo tal cual (no se escapa); se rechaza lo ejecutable
    PELIGROSO = re.compile(r"<\s*(script|iframe|object|embed|form|style|link|meta|base)\b|javascript\s*:|\son[a-z]+\s*=|\{\{|\{%", re.I)
    for n, linea in enumerate(txt.splitlines(), 1):
        if PELIGROSO.search(linea):
            err(f, f"línea {n}: contenido no permitido (script, iframe, form, style, eventos on*=, javascript: o Twig): {linea.strip()[:60]}")
    if not p.parent.name or not SLUG.match(p.parent.name):
        err(f, f"la carpeta '{p.parent.name}' debe ser un slug en minúsculas con guiones")
    if len(txt.split("---", 2)[-1].strip()) < 200:
        err(f, "el artículo es demasiado corto (mínimo ~200 caracteres)")
    for img in p.parent.glob("*"):
        if img.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"} and img.stat().st_size > MAX_IMG:
            err(str(img), "imagen mayor a 1 MB")

if errores:
    print("\n".join(errores)); sys.exit(1)
print("OK: contenido válido")
