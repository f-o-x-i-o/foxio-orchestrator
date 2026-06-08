# foxio_orchestrator — orquestador con skill set evolutivo + librería personal

Orquestación multi-agente con humano en el loop. El equipo NO está hardcodeado y
el skill set del orquestador TAMPOCO: arranca de una base mínima de sabiduría,
crece/poda con el tiempo, y **recuerda tus versiones mejoradas de cada skill
entre proyectos**.

Vos sos el **Product Owner**. Hablás con el **foxio_orchestrator**.

## Modelo mental
- **Subagentes** = ejecutores aislados. Hay dos: `foxio_orchestrator` (orquesta)
  y `specialist` (ejecuta, genérico — se despacha N veces).
- **Skills (skills.sh)** = conocimiento procedural (`SKILL.md`) que un specialist
  o el orquestador carga para saber CÓMO hacer algo. NO son agentes corriendo.
- **Librería personal** (`library/skills/`) = TUS versiones de esas skills,
  evolucionadas con contexto Foxio. El orquestador siempre las prefiere.
- El equipo y el skill set se construyen en runtime, siempre con tu aprobación.

## Librería personal de skills

La clave del sistema: cada skill que usás se puede guardar en `library/skills/`.
Con el tiempo acumulan tus decisiones de diseño, restricciones de plataforma y
contexto Foxio — cosas que skills.sh no sabe.

```
library/skills/
  ux-designer.md       ← tu versión, ya con tus ajustes
  firmware-stm32.md    ← descargada, le agregaste la HAL de Foxio
  qa-audio-dsp.md      ← creada desde cero con skill-creator
```

**Flujo de una skill:**
1. El orquestador busca en `library/skills/` → si está, la usa directo (📚 tuya).
2. Si no está, la trae de skills.sh → te pregunta si la guardás en la librería.
3. La mejorás en el proyecto → `/skill-save {nombre}` la promueve a la librería.
4. Próximo proyecto → el orquestador ya arranca con tu versión mejorada.

**Comandos:**
- `/skill-list` → tus skills con descripción y fecha de guardado
- `/skill-save [nombre]` → guardar/actualizar desde el proyecto actual

**Setup (una vez por máquina):** agregá a tu `.zshrc` / `.bashrc`:
```sh
export FOXIO_SKILLS_LIBRARY="$HOME/Development/foxio-orchestrator/library/skills"
```

## Decisiones de diseño (tus defaults)
- **Skill set base = mínimo:** arranca solo con `find-skills` + `skill-creator`.
  Todo lo demás se trae bajo demanda, con tu aprobación.
- **Topología = Subagents por default** (Anthropic: más confiable para calidad de
  output). Pasa a Agent Teams / paralelo SOLO si vos lo pedís explícitamente.
- **Skill set evolutivo:** en los milestones hace retrospectiva y propone APRENDER
  (traer/crear/guardar en librería) o PODAR (remover del proyecto). **Nunca toca
  skills sin tu sí explícito.** Todo queda registrado en `SKILL_LOG.md`.
- **Librería personal primero:** antes de ir a skills.sh siempre chequea tu
  librería. Tu versión evolucionada de una skill siempre gana.

## Estructura
```
.claude/
  agents/
    foxio_orchestrator.md   # orquestador — tu punto de entrada
    specialist.md           # ejecutor genérico
  commands/
    spec.md                 # /spec — genera el spec-kit con vos
    skill-save.md           # /skill-save — guarda una skill a la librería
    skill-list.md           # /skill-list — muestra tu librería
  skills/
    SKILL_LOG.md            # registro de altas/bajas (trazabilidad)
    (skills instaladas — gitignored, son cache del proyecto)
library/
  skills/                   # TUS skills evolucionadas (versionadas en git)
    README.md
    {nombre}.md             # una skill por archivo
specs/
  constitution.md           # restricciones inviolables (plantilla)
  spec.md                   # requerimientos + acceptance (plantilla)
```

## Instalación
1. Copiá `.claude/` (y `specs/`) a la raíz de tu repo.
2. Instalá la base mínima (una vez):
   ```
   npx skills add https://github.com/vercel-labs/skills --skill find-skills
   npx skills add anthropics/skills --skill skill-creator
   ```
3. Agregá el env var a tu shell (ver arriba).
4. `claude` en el repo, `/agents` para verificar `foxio_orchestrator` y `specialist`.

## Flujo de uso
1. `/spec [descripción]` → escribe `constitution.md` + `spec.md`. Aprobás.
2. "usá el foxio_orchestrator, leé el spec y armá el equipo".
3. Te muestra: capacidades → 📚 de tu librería (directo) + 🌐 candidatas de
   skills.sh con reputación (esperá tu OK para instalar).
4. Instala las aprobadas, propone plan + orden. Aprobás. Despacha, integra, resume.
5. En cada milestone: retrospectiva → propone aprender/podar/guardar en librería
   → **te pregunta** → registra en `SKILL_LOG.md`.
6. Al cierre: `/skill-save [nombre]` para promover las skills mejoradas a tu
   librería. `git commit + push` para respaldarlas.

## Catálogo de "sabiduría" relevante en skills.sh (para traer bajo demanda)
- `brainstorming` — descomposición/ideación (rol "system architect")
- `writing-plans` + `executing-plans` — el par "project manager"
- `subagent-driven-development` — patrón Subagents (calidad)
- `dispatching-parallel-agents` — patrón Teams/paralelo (velocidad) — solo si pedís Teams
- `verification-before-completion` — pase de verificación antes de cerrar
- `systematic-debugging`, `test-driven-development` — según necesite el proyecto
- `find-skills` (vercel-labs), `skill-creator` (anthropics) — ya en la base

## Notas honestas
- "Conectarse a skills.sh" = el orquestador corre `npx skills find/add/remove` en
  Bash y lee los SKILL.md. No es magia; es el package manager del ecosistema.
- Seguridad: traés conocimiento de terceros. El gate antes de instalar es a
  propósito. Preferí skills oficiales/auditadas (skills.sh tiene sección audits).
- Tu dominio (firmware/DSP/STM32) está poco cubierto en el catálogo. Esperá que el
  orquestador proponga seguido CREAR skills con skill-creator en vez de traerlas.
  Eso, de paso, te posiciona publicando skills propias bajo Foxio.
- Sin estado persistente entre sesiones: cada sesión relee el spec y el SKILL_LOG.
  La "memoria" del sistema vive en el spec-kit, el código, el log y tu librería
  personal — no en agentes prendidos.
