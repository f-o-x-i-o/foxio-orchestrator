# SKILL_LOG — registro de altas/bajas de skills

> El foxio_orchestrator registra acá cada skill que instala, crea o elimina.
> Toda entrada requiere aprobación explícita del PO antes de ejecutarse.
> Formato: fecha | acción (ADD/CREATE/REMOVE) | skill | motivo | aprobó
>
> Nota: descubrir/instalar/remover NO requiere instalar ninguna skill — el CLI
> `skills` (skills.sh) ya trae `npx skills find/add/remove`. La única base
> recomendada es `skill-creator` para autoría de skills propias.

| Fecha | Acción | Skill | Motivo | Aprobó |
|-------|--------|-------|--------|--------|
| init | ADD | anthropics/skills:skill-creator | base: crear/testear skills propias | — |
