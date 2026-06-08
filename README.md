# foxio_orchestrator — equipo de subagentes con sourcing dinámico desde skills.sh

Orquestación multi-agente con humano en el loop, donde el equipo NO está
hardcodeado: el foxio_orchestrator arma el equipo en runtime trayendo las skills que
el proyecto necesita desde skills.sh.

Vos sos el **Product Owner**. Hablás con el **foxio_orchestrator**, que:
lee el spec-kit -> deriva qué capacidades hacen falta -> las busca/instala desde
skills.sh -> despacha `specialist`s que cargan esas skills -> integra -> te
consulta en los gates.

## Modelo mental (importante)

- **Subagentes** = los ejecutores aislados (contexto propio). Acá hay dos:
  `foxio_orchestrator` (orquesta) y `specialist` (ejecuta, genérico).
- **Skills (skills.sh)** = conocimiento procedural (`SKILL.md`) que un specialist
  carga para saber CÓMO hacer una disciplina. NO son agentes corriendo.
- El equipo se "arma" = el foxio_orchestrator elige qué skills traer y se las asigna a
  specialists. Proyecto puro firmware -> trae skills de firmware/embedded y no
  toca front-end.

## Estructura
```
.claude/
  agents/
    foxio_orchestrator.md    # orquestador — tu punto de entrada
    specialist.md      # ejecutor genérico (se despacha N veces, una por tarea)
  commands/
    spec.md            # /spec — genera el spec-kit con vos
  skills/              # acá caen las skills que el foxio_orchestrator instala (runtime)
specs/
  constitution.md      # restricciones inviolables (plantilla)
  spec.md              # requerimientos + acceptance (plantilla)
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

1. Spec: `/spec [descripción]` -> te entrevista y escribe `constitution.md` +
   `spec.md`. Aprobás.
2. "foxio_orchestrator, leé el spec y armá el equipo".
3. El foxio_orchestrator te muestra: capacidades necesarias + skills candidatas de
   skills.sh con su reputación (installs/stars/fuente). **Vos aprobás cuáles
   instalar.**
4. Instala las aprobadas, te propone plan de equipo + orden. Aprobás.
5. Despacha specialists (paralelo/secuencial), integra, te resume. Aprobás la
   siguiente tanda. Nada irreversible sin tu OK.

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
