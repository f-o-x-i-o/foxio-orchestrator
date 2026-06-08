---
description: Guarda o actualiza una skill del proyecto actual en la librería personal de Foxio (formato carpeta SKILL.md).
---

Promové la skill indicada del proyecto actual a tu librería personal, para
tenerla en proyectos futuros. Las skills son CARPETAS (`<nombre>/SKILL.md`), no
archivos sueltos — así son skills reales de Claude Code y round-trippean con
`npx skills`.

Argumentos: $ARGUMENTS  (nombre de la skill, ej: `ux-designer`)

## Pasos

1. **Resolvé y validá la librería (fallá ruidoso).**
   ```bash
   LIBRARY="${FOXIO_SKILLS_LIBRARY:-$HOME/Development/foxio-orchestrator/library/skills}"
   if [ ! -d "$LIBRARY" ]; then
     echo "ERROR: no encuentro la librería en '$LIBRARY'."
     echo "Definí FOXIO_SKILLS_LIBRARY o cloná foxio-orchestrator ahí. Abortando."
   else
     echo "Librería: $LIBRARY"
   fi
   ```
   Si dio ERROR, no sigas: informá al PO y terminá.

2. **Encontrá la skill en el proyecto.**
   ```bash
   test -f ".claude/skills/$ARGUMENTS/SKILL.md" && echo "OK" || echo "NO_EXISTE"
   ```
   Si `NO_EXISTE`, decíselo al PO (quizá el nombre está mal o la skill no se
   instaló con `--copy`) y terminá.

3. **¿Ya está en la librería? Mostrá el diff antes de pisar.**
   ```bash
   if [ -d "$LIBRARY/$ARGUMENTS" ]; then
     diff -ru "$LIBRARY/$ARGUMENTS" ".claude/skills/$ARGUMENTS" || true
   fi
   ```
   Si existía, pedí confirmación explícita al PO antes de sobrescribir.

4. **Guardá la carpeta completa.**
   ```bash
   rm -rf "$LIBRARY/$ARGUMENTS" && cp -R ".claude/skills/$ARGUMENTS" "$LIBRARY/$ARGUMENTS"
   ```

5. **Registrá el origen** al inicio de `$LIBRARY/$ARGUMENTS/SKILL.md`, justo
   después del frontmatter, como bloque HTML-comment (no rompe el frontmatter):
   ```
   <!-- foxio-library
   saved: <fecha ISO de hoy>
   from:  <path absoluto del proyecto actual>
   -->
   ```
   Si el bloque ya existe, actualizá los valores.

6. **Confirmá al PO** y recordale respaldar (la librería es un repo git aparte):
   ```bash
   cd "$LIBRARY/../.." && git add library/skills/$ARGUMENTS && \
   git commit -m "skill: guardo/actualizo $ARGUMENTS" && git push
   ```
   Aclarale que ese commit es en el repo `foxio-orchestrator`, no en el proyecto
   donde está trabajando.
