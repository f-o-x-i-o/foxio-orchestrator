# foxio_orchestrator

Orquestación multi-agente con humano en el loop para Claude Code. El equipo NO
está hardcodeado y el skill set del orquestador TAMPOCO: arranca de una base
mínima, trae skills bajo demanda desde [skills.sh](https://skills.sh), y
**recuerda tus versiones mejoradas de cada skill entre proyectos**. La
especificación de cada proyecto la maneja [OpenSpec](https://github.com/Fission-AI/OpenSpec).

Vos sos el **Product Owner (PO)**. Hablás con el **foxio_orchestrator**.

> ¿Primera vez? Leé **[GUIDE.md](GUIDE.md)** — el paso a paso para dummies.

## Este repo es dos cosas

1. **Un toolkit que copiás a tus proyectos**: los agentes (`.claude/agents/`),
   los comandos (`.claude/commands/`) y la plantilla `specs/constitution.md`.
2. **El hogar git-backed de tu librería personal de skills** (`library/skills/`),
   que vive SOLO acá y se referencia desde cualquier proyecto vía la variable de
   entorno `FOXIO_SKILLS_LIBRARY`.

## Modelo mental
- **Subagentes** = ejecutores aislados. Hay dos: `foxio_orchestrator` (orquesta)
  y `specialist` (ejecuta, genérico — se despacha N veces).
- **Skills** = conocimiento procedural (carpeta `<nombre>/SKILL.md`) que un
  specialist carga para saber CÓMO hacer algo. NO son agentes corriendo.
- **Librería personal** = TUS versiones de esas skills, evolucionadas con contexto
  Foxio. El orquestador siempre las prefiere.
- **OpenSpec** = el spec-kit: `proposal` + delta-specs + `design` + `tasks` por
  cada cambio, con un *source of truth* que se actualiza al archivar.

## Decisiones de diseño (tus defaults)
- **Spec-kit = OpenSpec real** (`@fission-ai/openspec`), no una imitación. Flujo
  nativo `/opsx:propose → apply → sync → archive`, con `openspec validate`.
- **Base de skills = mínima:** el CLI `skills` ya da `find/add/remove`; solo se
  suma `skill-creator` para autoría. Todo lo demás se trae bajo demanda, con tu OK.
- **Topología = Subagents por default** (Anthropic: más confiable para calidad).
  Pasa a Agent Teams / paralelo SOLO si vos lo pedís.
- **Skill set evolutivo:** en los milestones propone APRENDER (traer/crear/guardar)
  o PODAR (remover). **Nunca toca skills sin tu sí.** Todo va a `SKILL_LOG.md`.
- **Librería personal primero:** antes de skills.sh chequea tu librería; si el
  path no existe, **avisa en vez de seguir en silencio**.

## Estructura
```
.claude/
  agents/
    foxio_orchestrator.md   # orquestador — tu punto de entrada
    specialist.md           # ejecutor genérico
  commands/
    spec.md                 # /spec — bootstrapea OpenSpec (init + constitution)
    skill-save.md           # /skill-save — guarda una skill a la librería
    skill-list.md           # /skill-list — muestra tu librería
  skills/
    SKILL_LOG.md            # registro de altas/bajas (trazabilidad)
    (skills del proyecto — gitignored, son cache local)
library/
  skills/                   # TU librería personal (versionada en git)
    README.md
    <nombre>/SKILL.md       # una carpeta por skill
specs/
  constitution.md           # restricciones inviolables (única fuente)
tests/
  validate.py               # validación estática del toolkit (sin LLM)
  scenarios/                # evals de comportamiento del agente
GUIDE.md                    # manual para dummies
```
En un PROYECTO real se suma `openspec/` (lo crea `openspec init`): `openspec/specs/`
(source of truth) y `openspec/changes/<slug>/` (proposal, delta-specs, design, tasks).

## Instalación (en tu proyecto)
1. **Node ≥ 20.19** y el CLI de OpenSpec:
   ```bash
   npm install -g @fission-ai/openspec@latest
   ```
2. Copiá `.claude/` y `specs/constitution.md` de este toolkit a la raíz de tu repo.
3. (Opcional) skill de autoría:
   ```bash
   npx skills add anthropics/skills --skill skill-creator -a claude-code --copy -y
   ```
4. Apuntá tu librería personal (en tu shell, una vez por máquina):
   ```bash
   export FOXIO_SKILLS_LIBRARY="$HOME/Development/foxio-orchestrator/library/skills"
   ```
5. Abrí `claude`, corré `/agents` y verificá `foxio_orchestrator` y `specialist`.

## Flujo de uso
1. **`/spec [descripción]`** → bootstrapea OpenSpec (`openspec init`) y la
   constitution; te dice que corras `/opsx:propose`.
2. **`/opsx:propose <descripción>`** (OpenSpec) → crea `openspec/changes/<slug>/`
   con proposal + delta-specs + design + tasks. Validás con `openspec validate`. Aprobás.
3. *"foxio_orchestrator, leé el cambio y armá el equipo"* → lee los artefactos,
   toma los criterios de éxito como done, precarga `tasks.md` en su tablero.
4. Te muestra capacidades → 📚 de tu librería (directo) + 🌐 candidatas de skills.sh
   con la reputación que haya. **Aprobás qué instalar.**
5. Despacha specialists, integra contra los escenarios de los delta-specs, te resume.
6. En cada milestone: retrospectiva → aprender/podar/guardar → **te pregunta** →
   registra en `SKILL_LOG.md`.
7. Al cierre: `tasks.md` con checkboxes, y corrés **`/opsx:archive`** (mergea los
   delta-specs al source of truth). `/skill-save <nombre>` + `git push` para
   respaldar las skills mejoradas.

## El CLI `skills` (lo que usa el orquestador)
| Comando | Uso |
|---------|-----|
| `npx skills find "<cap>"` | Buscar en el catálogo |
| `npx skills add <owner/repo> --skill <n> -a claude-code --copy -y` | Instalar (copia editable) |
| `npx skills list` | Listar instaladas |
| `npx skills remove <n>` | Remover del proyecto |
| `npx skills update <n>` | Actualizar a la última |

> Distinción: `vercel-labs/skills` es el **CLI** (`npx skills`); el **contenido**
> de skills está en repos como `vercel-labs/agent-skills`, `anthropics/skills`, etc.

## Validar el toolkit
```bash
python3 tests/validate.py
```
Chequea frontmatter de agentes/comandos, integridad referencial (sin paths
colgados), formato de la librería, paths personales filtrados e invariantes de la
lógica del orquestador. Corre en CI (`.github/workflows/validate.yml`). Detalle y
los evals de comportamiento: ver [`tests/README.md`](tests/README.md).

## Notas honestas
- "Conectarse a skills.sh" = el orquestador corre `npx skills …` en Bash y lee los
  `SKILL.md`. No es magia; es el package manager del ecosistema.
- Seguridad: traés conocimiento de terceros. El gate antes de instalar es a
  propósito. Preferí skills oficiales/auditadas (skills.sh tiene sección audits).
- Tu dominio (firmware/DSP/STM32) está poco cubierto: esperá que el orquestador
  proponga CREAR skills con `skill-creator` seguido. Eso te posiciona publicando
  skills propias bajo Foxio.
- Sin estado persistente entre sesiones: cada sesión relee el spec, el `SKILL_LOG`
  y tu librería. La "memoria" vive en el spec-kit, el código, el log y la librería
  — no en agentes prendidos.

## Licencia
MIT — ver [LICENSE](LICENSE).
