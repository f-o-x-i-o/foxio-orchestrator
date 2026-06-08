# foxio_orchestrator — equipo de subagentes con librería personal + sourcing desde skills.sh

Orquestación multi-agente con humano en el loop, donde el equipo NO está
hardcodeado: el foxio_orchestrator arma el equipo en runtime trayendo las skills que
el proyecto necesita — **primero de tu librería personal, luego de skills.sh**.

Vos sos el **Product Owner**. Hablás con el **foxio_orchestrator**, que:
lee el spec-kit -> deriva qué capacidades hacen falta -> busca en tu librería
personal -> si no las tiene, las trae de skills.sh -> despacha `specialist`s
que cargan esas skills -> integra -> te consulta en los gates.

## Modelo mental (importante)

- **Subagentes** = los ejecutores aislados (contexto propio). Acá hay dos:
  `foxio_orchestrator` (orquesta) y `specialist` (ejecuta, genérico).
- **Skills (skills.sh)** = conocimiento procedural (`SKILL.md`) que un specialist
  carga para saber CÓMO hacer una disciplina. NO son agentes corriendo.
- **Librería personal** (`library/skills/`) = TUS versiones de esas skills,
  evolucionadas con contexto Foxio. El orquestador siempre las prefiere.
- El equipo se "arma" = el foxio_orchestrator elige qué skills traer (librería
  personal primero, skills.sh si falta) y se las asigna a specialists.

## Librería personal de skills

La clave del sistema: cada skill que usás se puede guardar en `library/skills/`
dentro de este repo. Con el tiempo esas skills acumulan tus decisiones de diseño,
restricciones de plataforma y contexto Foxio — cosas que skills.sh no sabe.

```
library/skills/
  ux-designer.md       ← tu versión, ya con tus ajustes
  firmware-stm32.md    ← la descargaste, le agregaste la HAL de Foxio
  qa-audio-dsp.md      ← creada desde cero con skill-creator
```

**Flujo de una skill nueva:**
1. El orquestador la busca en `library/skills/` → si está, la usa directo.
2. Si no está, la trae de skills.sh → te pregunta si la guardás en la librería.
3. La editás en el proyecto, mejorás → `/skill-save {nombre}` la promueve a la librería.
4. Próximo proyecto → el orquestador ya arranca con tu versión mejorada.

**Comandos de la librería:**
- `/skill-list` → ver todas tus skills con descripción y fecha de guardado
- `/skill-save [nombre]` → guardar/actualizar la skill del proyecto actual

**Setup (una vez por máquina):** agregá a tu `.zshrc`:
```sh
export FOXIO_SKILLS_LIBRARY="$HOME/Development/foxio-orchestrator/library/skills"
```

## Estructura
```
.claude/
  agents/
    foxio_orchestrator.md    # orquestador — tu punto de entrada
    specialist.md            # ejecutor genérico (se despacha N veces, una por tarea)
  commands/
    spec.md                  # /spec — genera el spec-kit con vos
    skill-save.md            # /skill-save — guarda una skill a la librería personal
    skill-list.md            # /skill-list — muestra tu librería
  skills/                    # cache de skills del proyecto actual (gitignored)
library/
  skills/                    # TUS skills evolucionadas (versionadas en git)
    README.md
    {nombre}.md              # una skill por archivo
specs/
  constitution.md            # restricciones inviolables (plantilla)
  spec.md                    # requerimientos + acceptance (plantilla)
```

## Instalación

1. Copiá la carpeta `.claude/` (y `specs/` por las plantillas) a la raíz de tu repo.

2. **Instalá `find-skills`** (es lo que le da al foxio_orchestrator la capacidad de
   descubrir/instalar skills):
   ```
   npx skills add https://github.com/vercel-labs/skills --skill find-skills
   ```
   Opcional pero recomendado para el spec-gen / crear skills propias:
   ```
   npx skills add anthropics/skills --skill skill-creator
   ```

3. Abrí Claude Code en el repo, corré `/agents` y verificá que estén
   `foxio_orchestrator` y `specialist`.

## Flujo de uso

1. Spec: `/spec [descripción]` → te entrevista y escribe `constitution.md` +
   `spec.md`. Aprobás.
2. "foxio_orchestrator, leé el spec y armá el equipo".
3. El foxio_orchestrator muestra: capacidades necesarias + origen de cada skill
   (📚 **de tu librería** vs 🌐 candidatas de skills.sh con reputación).
   **Vos aprobás qué instalar del catálogo externo.**
4. Instala las aprobadas, te propone plan de equipo + orden. Aprobás.
5. Despacha specialists (paralelo/secuencial), integra, te resume. Aprobás la
   siguiente tanda. Nada irreversible sin tu OK.
6. Después del proyecto: `/skill-save [nombre]` para guardar las skills
   evolucionadas a tu librería. `git push` para respaldarlas.

## Notas

- El CLI de skills.sh expone `npx skills find` (buscar) y `npx skills add`
  (instalar). No hay search nativo más allá de eso; `find-skills` le enseña al
  agente a usarlos y a rankear por reputación.
- **Seguridad:** estás trayendo conocimiento de terceros a tu repo. El gate de
  aprobación antes de instalar es a propósito. skills.sh tiene una sección de
  audits — preferí skills auditadas/oficiales. Revisá el SKILL.md antes de
  ejecutar si la fuente no es de confianza.
- `opus` en el foxio_orchestrator (razonamiento de orquestación), `sonnet` en
  specialist (costo/consistencia). Ajustable en el frontmatter.
- Si una capacidad no tiene buena skill en el catálogo: el foxio_orchestrator te avisa
  y o la creás con `skill-creator`, o el specialist la resuelve sin skill.

## Limitación honesta
Esto vive entero en Claude Code. La parte de "conectarse a skills.sh y traer lo
necesario" la hace el foxio_orchestrator vía el CLI `npx skills` corriendo en Bash —
no es una integración mágica, es el agente ejecutando el package manager del
ecosistema y leyendo los SKILL.md resultantes. Funciona, pero depende de que las
skills del catálogo sean buenas para tu dominio (firmware embebido / DSP es un
nicho menos cubierto que web; puede que tengas que crear las tuyas).
