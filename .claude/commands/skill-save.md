---
description: Guarda o actualiza una skill del proyecto actual en la librería personal de Foxio.
---

Guardá la skill indicada en la librería personal para que esté disponible en
todos los proyectos futuros.

Argumentos: $ARGUMENTS  (nombre de la skill, ej: `ux-designer`)

## Pasos

1. **Resolvé el path de la skill en el proyecto actual.**
   Buscá en `.claude/skills/$ARGUMENTS.md`. Si no existe, informá al PO y terminá.

2. **Resolvé el path de la librería.**
   ```bash
   LIBRARY="${FOXIO_SKILLS_LIBRARY:-$HOME/Development/foxio-orchestrator/library/skills}"
   echo "$LIBRARY"
   ```

3. **Verificá si ya existe en la librería.**
   - Si NO existe → guardala directamente (paso 4).
   - Si SÍ existe → mostrá un diff breve entre la versión del proyecto y la
     guardada con `diff "$LIBRARY/$ARGUMENTS.md" .claude/skills/$ARGUMENTS.md`.
     Pedí confirmación al PO antes de sobrescribir.

4. **Guardá el archivo.**
   Copiá `.claude/skills/$ARGUMENTS.md` a `$LIBRARY/$ARGUMENTS.md`.

5. **Registrá el origen** en las primeras líneas del archivo guardado.
   Agregá (o actualizá) un bloque de comentario al inicio del SKILL.md:
   ```
   <!-- foxio-library
   saved: <fecha ISO hoy>
   from:  <path absoluto del proyecto actual>
   -->
   ```
   Si el bloque ya existe, actualizá los valores.

6. **Confirmá al PO:**
   - Path donde quedó guardada
   - Si es nueva o actualizó una existente
   - Recordale que puede hacer `git commit + push` en el repo foxio-orchestrator
     para respaldarla en GitHub (`cd ~/Development/foxio-orchestrator && git add
     library/skills/$ARGUMENTS.md && git commit -m "skill: guardo $ARGUMENTS"
     && git push`)
