# Escenario 01 — La librería personal gana sobre skills.sh

Valida que el orquestador use TU versión de una skill cuando existe, sin ir al
catálogo externo.

## Setup
- `FOXIO_SKILLS_LIBRARY` apunta a una librería que contiene `ux-designer/SKILL.md`.
- Un cambio OpenSpec activo que necesita, entre otras, una capacidad de diseño UX.

## Entrada (mensaje del PO)
> "foxio_orchestrator, leé el cambio y armá el equipo."

## Comportamiento esperado (asserts)
- ✓ Resuelve `FOXIO_SKILLS_LIBRARY` y lista las carpetas de la librería ANTES de
  llamar a `npx skills find`.
- ✓ Para la capacidad de diseño UX, detecta `ux-designer` en la librería y la
  marca como "📚 de tu librería".
- ✓ Copia la carpeta al proyecto con `cp -R "$LIBRARY/ux-designer" .claude/skills/`.
- ✓ NO ejecuta `npx skills find` ni `add` para esa capacidad.
- ✓ Para las capacidades que NO están en la librería, sí va a skills.sh y pide OK.

## Anti-patrones (deben NO ocurrir)
- ✗ Ir directo a skills.sh ignorando la librería.
- ✗ Instalar `ux-designer` desde el catálogo pisando tu versión.
- ✗ Seguir en silencio si la librería no existe (debe AVISAR al PO).
