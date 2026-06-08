#!/usr/bin/env python3
"""
Validador estático del toolkit foxio_orchestrator.

No corre ningún LLM: valida la ESTRUCTURA y las INVARIANTES de las que depende la
lógica del agente. Si esto pasa, el toolkit está internamente consistente y
cargable. Para validar el COMPORTAMIENTO del agente, ver tests/scenarios/.

Uso:
    python3 tests/validate.py          # valida todo, exit 1 si algo falla
    python3 tests/validate.py -v       # además lista los checks que pasaron

Sin dependencias externas (solo stdlib). Requiere Python 3.8+.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv

# --- salida -----------------------------------------------------------------
_C = sys.stdout.isatty()
GREEN = "\033[32m" if _C else ""
RED = "\033[31m" if _C else ""
YELLOW = "\033[33m" if _C else ""
DIM = "\033[2m" if _C else ""
RESET = "\033[0m" if _C else ""

_failures: list[str] = []
_passes = 0
_skips = 0


def ok(msg: str) -> None:
    global _passes
    _passes += 1
    if VERBOSE:
        print(f"{GREEN}  PASS{RESET} {msg}")


def fail(msg: str) -> None:
    _failures.append(msg)
    print(f"{RED}  FAIL{RESET} {msg}")


def skip(msg: str) -> None:
    global _skips
    _skips += 1
    print(f"{YELLOW}  SKIP{RESET} {msg}")


def section(name: str) -> None:
    print(f"\n{DIM}== {name} =={RESET}")


# --- helpers ----------------------------------------------------------------
ALLOWED_TOOLS = {
    "Read", "Write", "Edit", "MultiEdit", "NotebookEdit", "Glob", "Grep",
    "Bash", "Task", "TodoWrite", "WebFetch", "WebSearch",
}
ALLOWED_MODELS = {"opus", "sonnet", "haiku", "inherit"}


def parse_frontmatter(text: str) -> dict | None:
    """Devuelve dict de keys top-level del frontmatter YAML, o None si no hay."""
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    fm: dict[str, str] = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if key not in fm:  # primera aparición gana (ignora sub-keys/listas)
                fm[key] = val
    return fm


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


# --- A. Frontmatter de agentes ---------------------------------------------
def check_agents() -> None:
    section("Agentes (.claude/agents/*.md)")
    agents_dir = ROOT / ".claude" / "agents"
    if not agents_dir.is_dir():
        fail(".claude/agents/ no existe")
        return
    files = sorted(agents_dir.glob("*.md"))
    if not files:
        fail("no hay agentes en .claude/agents/")
        return
    for f in files:
        fm = parse_frontmatter(read(f))
        if fm is None:
            fail(f"{rel(f)}: sin frontmatter válido")
            continue
        for key in ("name", "description", "tools", "model"):
            if key not in fm or not fm[key]:
                fail(f"{rel(f)}: falta '{key}' en frontmatter")
            else:
                ok(f"{rel(f)}: tiene '{key}'")
        if fm.get("name") and fm["name"] != f.stem:
            fail(f"{rel(f)}: name '{fm['name']}' != filename '{f.stem}'")
        else:
            ok(f"{rel(f)}: name coincide con filename")
        model = fm.get("model", "")
        if model and model not in ALLOWED_MODELS:
            fail(f"{rel(f)}: model '{model}' no está en {sorted(ALLOWED_MODELS)}")
        else:
            ok(f"{rel(f)}: model válido")
        tools_raw = fm.get("tools", "")
        if tools_raw:
            tools = [t.strip() for t in tools_raw.split(",") if t.strip()]
            bad = [t for t in tools if t not in ALLOWED_TOOLS]
            if bad:
                fail(f"{rel(f)}: tools desconocidas {bad}")
            else:
                ok(f"{rel(f)}: tools válidas ({len(tools)})")


# --- B. Frontmatter de comandos --------------------------------------------
def check_commands() -> None:
    section("Comandos (.claude/commands/*.md)")
    cmd_dir = ROOT / ".claude" / "commands"
    if not cmd_dir.is_dir():
        fail(".claude/commands/ no existe")
        return
    for f in sorted(cmd_dir.glob("*.md")):
        fm = parse_frontmatter(read(f))
        if fm is None:
            fail(f"{rel(f)}: sin frontmatter válido")
            continue
        if not fm.get("description"):
            fail(f"{rel(f)}: falta 'description'")
        else:
            ok(f"{rel(f)}: tiene description")


# --- C. Integridad referencial ---------------------------------------------
def check_references() -> None:
    section("Integridad referencial")
    # Los 3 comandos propios deben existir.
    for name in ("spec", "skill-save", "skill-list"):
        p = ROOT / ".claude" / "commands" / f"{name}.md"
        if p.exists():
            ok(f"comando /{name} existe")
        else:
            fail(f"comando /{name} referenciado pero falta {rel(p)}")

    # El orquestador NO debe referenciar specs/spec.md (legacy eliminado).
    orch = ROOT / ".claude" / "agents" / "foxio_orchestrator.md"
    if orch.exists():
        if "specs/spec.md" in read(orch):
            fail("foxio_orchestrator.md referencia 'specs/spec.md' (legacy eliminado)")
        else:
            ok("foxio_orchestrator.md no referencia el legacy specs/spec.md")

    # Links markdown relativos en README y GUIDE deben resolver.
    for doc in ("README.md", "GUIDE.md"):
        p = ROOT / doc
        if not p.exists():
            fail(f"{doc} no existe")
            continue
        for target in re.findall(r"\]\(([^)]+)\)", read(p)):
            t = target.strip()
            if t.startswith(("http://", "https://", "#", "mailto:")):
                continue
            t = t.split("#", 1)[0]
            if not t:
                continue
            resolved = (p.parent / t).resolve()
            if resolved.exists():
                ok(f"{doc} → {t} existe")
            else:
                fail(f"{doc} → link roto: {t}")


# --- D. Librería de skills --------------------------------------------------
def check_skill_library() -> None:
    section("Librería personal (library/skills/)")
    lib = ROOT / "library" / "skills"
    if not lib.is_dir():
        fail("library/skills/ no existe")
        return
    skill_dirs = [d for d in lib.iterdir() if d.is_dir()]
    if not skill_dirs:
        skip("librería vacía (todavía sin skills guardadas) — OK")
    for d in sorted(skill_dirs):
        sk = d / "SKILL.md"
        if not sk.exists():
            fail(f"library/skills/{d.name}/ sin SKILL.md")
            continue
        fm = parse_frontmatter(read(sk))
        if fm is None or not fm.get("name") or not fm.get("description"):
            fail(f"library/skills/{d.name}/SKILL.md: frontmatter incompleto (name/description)")
        else:
            ok(f"library/skills/{d.name}/SKILL.md válido")
    # Archivos sueltos .md (que no sean README) = modelo viejo de archivo plano.
    for f in lib.glob("*.md"):
        if f.name != "README.md":
            fail(f"library/skills/{f.name}: skill como archivo plano; debe ser carpeta {f.stem}/SKILL.md")


# --- E. Portabilidad / paths personales ------------------------------------
ALL_TEXT_GLOBS = ("*.md", "*.py", "*.yml", "*.yaml", "*.sh", "*.toml")


def iter_text_files():
    for pat in ALL_TEXT_GLOBS:
        for f in ROOT.rglob(pat):
            if ".git/" in str(f.relative_to(ROOT)):
                continue
            yield f


def check_portability() -> None:
    section("Portabilidad (sin paths personales hardcodeados)")
    leak = re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+")
    found = False
    for f in iter_text_files():
        for n, line in enumerate(read(f).splitlines(), 1):
            for m in leak.finditer(line):
                found = True
                fail(f"{rel(f)}:{n}: path personal '{m.group(0)}' (usá $HOME)")
    if not found:
        ok("ningún path /Users/<x> o /home/<x> hardcodeado")

    # Consistencia del default de FOXIO_SKILLS_LIBRARY.
    canonical = "$HOME/Development/foxio-orchestrator/library/skills"
    defaults = set()
    for f in iter_text_files():
        for m in re.finditer(r"\$\{FOXIO_SKILLS_LIBRARY:-([^}]+)\}", read(f)):
            defaults.add(m.group(1).strip())
    if not defaults:
        skip("no se usa el default :- de FOXIO_SKILLS_LIBRARY")
    elif defaults == {canonical}:
        ok(f"default de FOXIO_SKILLS_LIBRARY consistente ({canonical})")
    else:
        fail(f"defaults inconsistentes de FOXIO_SKILLS_LIBRARY: {sorted(defaults)}")


# --- F. Invariantes de la lógica del orquestador ---------------------------
def check_orchestrator_invariants() -> None:
    section("Invariantes del orquestador (lógica clave presente)")
    orch = ROOT / ".claude" / "agents" / "foxio_orchestrator.md"
    if not orch.exists():
        fail("falta foxio_orchestrator.md")
        return
    text = read(orch)
    invariants = {
        "topología Subagents por default": "Subagents por DEFAULT",
        "gate de OK antes de instalar": "Esperá OK explícito antes de instalar",
        "librería personal primero": "librería primero",
        "registro en SKILL_LOG": "SKILL_LOG.md",
        "no invoca slash commands": "No podés invocar slash commands",
        "integra OpenSpec": "openspec",
        "regla inviolable de skills": "REGLA INVIOLABLE",
    }
    for label, needle in invariants.items():
        if needle.lower() in text.lower():
            ok(f"invariante presente: {label}")
        else:
            fail(f"invariante AUSENTE: {label} (esperaba '{needle}')")


# --- G. OpenSpec (si aplica) ------------------------------------------------
def check_openspec() -> None:
    section("OpenSpec (si el proyecto lo usa)")
    if not (ROOT / "openspec").is_dir():
        skip("este repo es el toolkit, no tiene openspec/ — OK")
        return
    if not shutil.which("openspec"):
        skip("openspec/ existe pero el CLI no está instalado")
        return
    try:
        r = subprocess.run(
            ["openspec", "validate", "--all"],
            cwd=ROOT, capture_output=True, text=True, timeout=60,
        )
        if r.returncode == 0:
            ok("openspec validate --all pasó")
        else:
            fail(f"openspec validate falló:\n{r.stdout}\n{r.stderr}")
    except Exception as e:  # noqa: BLE001
        fail(f"no se pudo correr openspec validate: {e}")


def main() -> int:
    print(f"{DIM}foxio_orchestrator — validación estática del toolkit{RESET}")
    print(f"{DIM}root: {ROOT}{RESET}")
    check_agents()
    check_commands()
    check_references()
    check_skill_library()
    check_portability()
    check_orchestrator_invariants()
    check_openspec()

    print()
    if _failures:
        print(f"{RED}✗ {len(_failures)} fallo(s){RESET}, "
              f"{GREEN}{_passes} ok{RESET}, {YELLOW}{_skips} skip{RESET}")
        return 1
    print(f"{GREEN}✓ todo OK{RESET} — {_passes} checks, {YELLOW}{_skips} skip{RESET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
