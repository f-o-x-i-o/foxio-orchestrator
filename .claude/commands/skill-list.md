---
description: Lista las skills de la librería personal de Foxio (carpetas con SKILL.md) con descripción y origen.
---

Mostrá el estado de tu librería personal de skills.

## Pasos

1. **Resolvé y validá la librería (fallá ruidoso).**
   ```bash
   LIBRARY="${FOXIO_SKILLS_LIBRARY:-$HOME/Development/foxio-orchestrator/library/skills}"
   if [ ! -d "$LIBRARY" ]; then
     echo "ERROR: no encuentro la librería en '$LIBRARY'. Definí FOXIO_SKILLS_LIBRARY."
   else
     find "$LIBRARY" -mindepth 1 -maxdepth 1 -type d -exec test -f '{}/SKILL.md' ';' -print
   fi
   ```
   Si dio ERROR o no hay ninguna carpeta, informalo con el setup
   (ver `library/skills/README.md`) y terminá.

2. **Para cada carpeta encontrada**, leé `<carpeta>/SKILL.md`:
   - Frontmatter `name` + `description`.
   - Bloque `<!-- foxio-library ... -->` si existe (`saved`, `from`).

3. **Presentá una tabla al PO:**
   ```
   ## Tu librería personal de skills

   | Skill | Descripción | Guardada | Proyecto origen |
   |-------|-------------|----------|-----------------|
   | ux-designer | ... | 2026-06-08 | ~/Development/... |
   ```

4. **Al pie:** total de skills + recordatorio `/skill-save [nombre]` para agregar
   más, y que para usar una en un proyecto el foxio_orchestrator la copia con
   `cp -R "$LIBRARY/<nombre>" .claude/skills/`.
