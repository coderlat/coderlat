"""Mueve los aportes aprobados (aportes/<slug>/) al repo de contenido (contenido/pages/02.blog/<slug>/).
Escribe en $RUNNER_TEMP: publicados.txt (para limpiar el buzón) y errores.txt.
Se ejecuta SOLO tras el merge en main (evento push), nunca sobre código de un PR."""
import os, re, shutil, subprocess, sys, pathlib
import yaml

OWNER = os.environ.get("OWNER", "")
BEFORE = os.environ.get("BEFORE", "")
TMP = pathlib.Path(os.environ.get("RUNNER_TEMP", "/tmp"))
DEST_BASE = pathlib.Path("contenido/pages/02.blog")
SLUG = re.compile(r"^[a-z0-9][a-z0-9\-]*$")

def sh(*a): return subprocess.run(a, capture_output=True, text=True)

def autor(item):
    txt = item.read_text(encoding="utf-8")
    fm = yaml.safe_load(txt.split("---")[1]) or {}
    return str(fm.get("author", "")).strip().lower()

def slugs_cambiados():
    if re.fullmatch(r"0*", BEFORE or "0"):
        base = [p.name for p in pathlib.Path("aportes").iterdir() if p.is_dir()]
        return sorted(base)
    r = sh("git", "diff", "--name-only", "--diff-filter=AM", BEFORE, "HEAD", "--", "aportes/")
    out = set()
    for f in r.stdout.splitlines():
        parts = f.split("/")
        if len(parts) >= 3: out.add(parts[1])
    return sorted(out)

publicados, errores = [], []
for slug in slugs_cambiados():
    src = pathlib.Path("aportes") / slug
    if not SLUG.match(slug) or not src.is_dir():
        errores.append(f"{slug}: slug inválido"); continue
    items = sorted(src.glob("item*.md"))
    if not items:
        errores.append(f"{slug}: no tiene item*.md"); continue
    v = sh(sys.executable, ".github/scripts/validar.py", *map(str, items))
    if v.returncode != 0:
        errores.append(f"{slug}: no pasa la validación\n{v.stdout}"); continue
    nuevo = autor(items[0])
    dest = DEST_BASE / slug
    existentes = sorted(dest.glob("item*.md")) if dest.is_dir() else []
    if existentes and autor(existentes[0]) not in (nuevo, OWNER.lower()) and nuevo != OWNER.lower():
        errores.append(f"{slug}: ya existe publicado por otro autor ({autor(existentes[0])}); revisar a mano"); continue
    if dest.exists(): shutil.rmtree(dest)
    shutil.copytree(src, dest)
    publicados.append(slug)
    print(f"publicado: {slug}")

(TMP / "publicados.txt").write_text("\n".join(publicados) + ("\n" if publicados else ""))
(TMP / "errores.txt").write_text("\n".join(errores) + ("\n" if errores else ""))
print(f"{len(publicados)} publicados, {len(errores)} con error")
