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

## Workflow de trabajo

Un loop con vos (el PO) adentro y **gates** ⛔ donde el agente para y espera tu OK.
Nada irreversible pasa sin tu aprobación.

```
  /spec  ──►  /opsx:propose  ──►  foxio_orchestrator  ──►  specialists  ──►  /opsx:archive
(bootstrap)   (spec-kit)         (planifica + skills)      (ejecutan)        (mergea al
                                        │   ▲                   │             source of truth)
                                        │   └──── resúmenes ◄────┘
                                        ▼
                                 vos aprobás en
                                  cada GATE ⛔
```

| # | Fase | Quién | Qué pasa | Gate |
|---|------|-------|----------|------|
| 0 | Setup | vos | `npm i -g @fission-ai/openspec`, copiás `.claude/`, `export FOXIO_SKILLS_LIBRARY` | — |
| 1 | Especificar | vos + OpenSpec | `/spec` bootstrapea; `/opsx:propose` crea el spec-kit; `openspec validate` | aprobás el spec |
| 2 | Planificar | orquestador | lee el cambio, deriva **capacidades**, propone skills (📚 librería / 🌐 skills.sh) | ⛔ OK para instalar |
| 3 | Despachar | orquestador | propone plan de equipo + orden (Subagents por default) | ⛔ OK para despachar |
| 4 | Ejecutar | specialists | cada uno carga su skill, hace UNA tarea, devuelve un resumen | ⛔ OK tras cada tanda |
| 5 | Integrar | orquestador | verifica contra los escenarios GIVEN/WHEN/THEN + criterios de éxito | — |
| 6 | Retrospectiva | orquestador + vos | aprender / podar / guardar skills; registra en `SKILL_LOG.md` | ⛔ OK para tocar skills |
| 7 | Cerrar | vos | `/opsx:archive` mergea los delta-specs; `/skill-save` + `git push` respalda | — |

## Ejemplo completo: un acortador de URLs

Proyecto de juguete, estándar y con mil referencias online para contrastar: una
API REST que acorta URLs (`POST /shorten` → código; `GET /:code` → redirect 301).

**1. El spec** (lo genera `/opsx:propose`, lo aprobás vos). Criterios de éxito en
`proposal.md`:

| ID | Criterio | Corte medible |
|----|----------|---------------|
| AC-1 | `POST /shorten` devuelve un código base62 de 7 chars | `^[0-9A-Za-z]{7}$` |
| AC-2 | `GET /:code` redirige a la URL original | HTTP 301 + `Location` |
| AC-3 | URL inválida → error | HTTP 400 |
| AC-4 | código inexistente → no encontrado | HTTP 404 |
| AC-5 | la misma URL pedida 2 veces → el mismo código | idempotente |

**2. El orquestador deriva capacidades y arma el equipo.** Tres capacidades → tres
specialists, cada uno con su skill real de skills.sh (la primera vez la librería
está vacía, así que las trae del catálogo y te pide OK):

| Rol (specialist) | Capacidad | Skill (skills.sh) | Installs |
|------------------|-----------|-------------------|----------|
| **Backend dev** | API REST + persistencia | `mrgoonie/claudekit-skills@backend-development` | 1.4K |
| **QA engineer** | tests de los 5 escenarios | `addyosmani/agent-skills@test-driven-development` | 4.6K |
| **CI/CD engineer** | pipeline GitHub Actions | `ruvnet/ruflo@agent-ops-cicd-github` | 654 |

**3. Cómo se ve en la práctica** (transcript abreviado):

```
vos:          /spec una API REST que acorta URLs
/spec:        OpenSpec listo. Corré  /opsx:propose acortador de URLs

vos:          /opsx:propose acortador de URLs
              → revisás los artefactos, corrés  openspec validate , aprobás

vos:          foxio_orchestrator, leé el cambio y armá el equipo
orquestador:  Leí el cambio add-url-shortener. Capacidades:
                1) API REST + persistencia   2) suite de tests   3) CI/CD
              Tu librería está vacía → busqué en skills.sh (ordenado por installs):
                backend  → backend-development           (1.4K)
                QA       → test-driven-development        (4.6K)
                CI/CD    → agent-ops-cicd-github          (654)
              ¿Instalo estas tres?                                      ⛔ GATE
vos:          dale
orquestador:  Instaladas (anotadas en SKILL_LOG). Plan — Subagents secuencial:
                #1 backend → endpoints + storage
                #2 QA      → tests contra AC-1..AC-5
                #3 CI/CD   → Actions (install→lint→test) en cada push
              ¿Despacho?                                                ⛔ GATE
vos:          sí
orquestador:  #1 ✓ POST /shorten, GET /:code, store SQLite, base62(id++)
              #2 ✓ 11 tests; AC-5 (idempotencia) destapó un bug → lo reporté
              #3 ✓ .github/workflows/ci.yml (install→lint→test)
              Conflicto: el design no definía URLs duplicadas bajo carga.
              ¿Lo cierro idempotente antes de archivar?                 ⛔ GATE
vos:          sí, cerralo
orquestador:  Hecho. tasks.md con todos los checkboxes. Retrospectiva:
              adapté backend-development a tu estilo (storage detrás de interfaz,
              tests en host). ¿Lo guardás como tu foxio-backend?  → /skill-save
              Cuando quieras, corré  /opsx:archive  para mergear los specs.
```

**4. La próxima vez** que arranques una API REST, el orquestador ya encuentra tu
`foxio-backend` en la librería (📚) y la usa directo, sin volver al catálogo.

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
