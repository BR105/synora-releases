#!/usr/bin/env python3
"""Sube Zynora.exe a VirusTotal y actualiza los enlaces del sitio (gh-pages).

Uso (en Actions):
  VT_API_KEY=... python vt_upload_and_link.py --exe Zynora.exe --site-dir site

- Si el hash ya existe en VT, no vuelve a subir (ahorra cuota).
- Espera a que el análisis termine (o timeout) antes de tocar la web.
- Reemplaza cualquier /gui/file/<64 hex> en index.html y avisos.html.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
from pathlib import Path

import requests

VT = "https://www.virustotal.com/api/v3"
HASH_RE = re.compile(
    r"(https://www\.virustotal\.com/gui/file/)[a-fA-F0-9]{64}"
)


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def vt_get(session: requests.Session, path: str) -> requests.Response:
    return session.get(f"{VT}{path}", timeout=60)


def vt_post_file(session: requests.Session, exe: Path) -> str:
    """Devuelve analysis id."""
    with exe.open("rb") as f:
        r = session.post(
            f"{VT}/files",
            files={"file": (exe.name, f)},
            timeout=120,
        )
    if r.status_code == 429:
        die("Cuota VirusTotal agotada (429). Reintenta más tarde.")
    if r.status_code >= 400:
        die(f"Upload falló HTTP {r.status_code}: {r.text[:500]}")
    data = r.json()
    try:
        return data["data"]["id"]
    except (KeyError, TypeError):
        die(f"Respuesta de upload inesperada: {data}")


def wait_analysis(session: requests.Session, analysis_id: str, timeout_s: int = 600) -> None:
    deadline = time.time() + timeout_s
    # Free API: ~4 req/min → esperar ≥15 s entre polls
    while time.time() < deadline:
        r = vt_get(session, f"/analyses/{analysis_id}")
        if r.status_code == 429:
            print("Rate limit; esperando 20 s…")
            time.sleep(20)
            continue
        if r.status_code >= 400:
            die(f"Poll análisis HTTP {r.status_code}: {r.text[:400]}")
        status = r.json().get("data", {}).get("attributes", {}).get("status")
        print(f"  análisis: {status}")
        if status == "completed":
            return
        time.sleep(16)
    print("AVISO: timeout esperando análisis; igual se actualiza el enlace (el informe puede tardar un poco más).")


def file_known(session: requests.Session, sha: str) -> bool:
    r = vt_get(session, f"/files/{sha}")
    if r.status_code == 200:
        return True
    if r.status_code == 404:
        return False
    if r.status_code == 429:
        die("Cuota VirusTotal agotada al consultar el hash (429).")
    die(f"Consulta hash HTTP {r.status_code}: {r.text[:400]}")


def update_site(site_dir: Path, sha: str) -> list[Path]:
    changed: list[Path] = []
    for name in ("index.html", "avisos.html"):
        path = site_dir / name
        if not path.is_file():
            print(f"AVISO: no existe {path}, se omite")
            continue
        text = path.read_text(encoding="utf-8")
        new, n = HASH_RE.subn(rf"\g<1>{sha}", text)
        if n == 0:
            print(f"AVISO: {name} no tenía enlace VT con hash de 64 hex")
            continue
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed.append(path)
            print(f"  {name}: {n} enlace(s) → {sha}")
        else:
            print(f"  {name}: ya apuntaba a {sha}")
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", type=Path, required=True)
    ap.add_argument("--site-dir", type=Path, required=True)
    ap.add_argument("--skip-upload", action="store_true", help="Solo actualizar HTML con el hash local")
    args = ap.parse_args()

    api_key = os.environ.get("VT_API_KEY", "").strip()
    if not api_key and not args.skip_upload:
        die("Falta variable de entorno VT_API_KEY")

    exe = args.exe
    if not exe.is_file():
        die(f"No está el exe: {exe}")

    sha = sha256_file(exe)
    print(f"SHA256={sha}")
    print(f"URL=https://www.virustotal.com/gui/file/{sha}")

    if not args.skip_upload:
        session = requests.Session()
        session.headers.update({"x-apikey": api_key, "Accept": "application/json"})
        if file_known(session, sha):
            print("Ya existe en VirusTotal; no se vuelve a subir.")
        else:
            print("Subiendo a VirusTotal…")
            analysis_id = vt_post_file(session, exe)
            print(f"analysis_id={analysis_id}")
            wait_analysis(session, analysis_id)

    changed = update_site(args.site_dir, sha)
    # Para el step de commit
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"sha256={sha}\n")
            f.write(f"vt_url=https://www.virustotal.com/gui/file/{sha}\n")
            f.write(f"changed={'true' if changed else 'false'}\n")

    print("Listo.")


if __name__ == "__main__":
    main()
