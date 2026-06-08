---
description: Lista todas las skills en la librería personal de Foxio con descripción y origen.
---

Mostrá el estado actual de la librería personal de skills.

## Pasos

1. **Resolvé el path de la librería.**
   ```bash
   LIBRARY="${FOXIO_SKILLS_LIBRARY:-$HOME/Development/foxio-orchestrator/library/skills}"
   ls "$LIBRARY"/*.md 2>/dev/null | grep -v README.md
   ```
   Si la librería está vacía o no existe, informalo con instrucciones de setup
   (ver `library/skills/README.md`).

2. **Para cada `.md` encontrado (excluí `README.md`):**
   - Leé el bloque `<!-- foxio-library ... -->` si existe (saved, from).
   - Extraé las primeras líneas de descripción del SKILL.md (título y primer párrafo).

3. **Presentá una tabla al PO:**

   ```
   ## Tu librería personal de skills
   
   | Skill | Descripción breve | Guardada | Proyecto origen |
   |-------|------------------|----------|-----------------|
   | ux-designer | ... | 2026-06-08 | ~/Development/... |
   ```

4. **Al pie de la tabla**, mostrá también:
   - Total de skills en la librería.
   - Comando recordatorio: `/skill-save [nombre]` para agregar más.
