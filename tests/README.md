# Tests — cómo se valida el toolkit

Un sistema de agentes es mayormente *prompts*, así que no se puede unit-testear el
razonamiento del modelo de forma determinística. Pero sí se puede validar dos
capas concretas:

## Capa 1 — Validación estática (`validate.py`)

Determinística, sin LLM, corre en CI. Chequea:

- **Frontmatter** de agentes (`name`/`description`/`tools`/`model` válidos, `name`
  == filename, tools dentro del allowlist) y de comandos (`description`).
- **Integridad referencial**: los comandos `/spec`, `/skill-save`, `/skill-list`
  existen; el orquestador NO referencia el legacy `specs/spec.md`; los links
  markdown relativos de README/GUIDE resuelven.
- **Librería de skills**: cada skill es una carpeta `<nombre>/SKILL.md` con
  frontmatter (no archivos planos).
- **Portabilidad**: ningún path personal `/Users/<x>` ni `/home/<x>` hardcodeado;
  el default de `FOXIO_SKILLS_LIBRARY` es consistente en todo el repo.
- **Invariantes de la lógica del orquestador**: que el prompt siga conteniendo las
  reglas clave (Subagents por default, gate de OK antes de instalar, librería
  primero, registro en SKILL_LOG, no invocar slash commands, integración OpenSpec,
  regla inviolable de skills). Si alguien edita el agente y borra un gate, falla.
- **OpenSpec**: si hay `openspec/` y el CLI, corre `openspec validate --all`.

```bash
python3 tests/validate.py        # exit 1 si algo falla
python3 tests/validate.py -v     # lista también los PASS
```

Esto habría cazado varios bugs reales del repo: un `specs/spec.md` colgado, paths
personales filtrados, o un gate borrado del orquestador.

## Capa 2 — Evals de comportamiento (`scenarios/`)

Lo que `validate.py` NO puede hacer: confirmar que el agente *se comporta* bien
(que frena en los gates, que mira la librería primero, etc.). Eso se valida con
**escenarios**: cada `scenarios/*.md` describe una situación de entrada y el
comportamiento esperado, como checklist.

Se pueden correr de dos formas:
1. **A mano**: seguís el escenario en Claude Code y verificás los "✓ esperado".
2. **Como eval automatizado**: alimentás el escenario a un harness de evals (por
   ej. el `skill-creator` de skills.sh trae soporte de evals, o tu propio runner
   que invoque al agente y chequee asserts). El formato está pensado para eso:
   `## Entrada`, `## Comportamiento esperado` (asserts), `## Anti-patrones`.

Los escenarios son también **documentación viva** de la lógica del orquestador.
