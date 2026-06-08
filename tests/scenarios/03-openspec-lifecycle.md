# Escenario 03 — El orquestador respeta el ciclo de OpenSpec

Valida que el orquestador se inserte como el paso `apply` multi-agente y no se
salga de los rieles de OpenSpec.

## Setup
- OpenSpec inicializado, con `openspec/changes/clock-swing/` (proposal, delta-specs
  en `specs/`, design, tasks) y `openspec/specs/` como source of truth.

## Entrada (mensaje del PO)
> "foxio_orchestrator, leé el cambio clock-swing y armá el equipo."

## Comportamiento esperado (asserts)
- ✓ Lee `specs/constitution.md`, luego `openspec/specs/` (source of truth), luego
  `openspec/changes/clock-swing/`.
- ✓ Toma los criterios de éxito del `proposal.md` como definición de done.
- ✓ Precarga `tasks.md` en su TodoWrite.
- ✓ Si el CLI está, corre `openspec validate clock-swing` antes de ejecutar.
- ✓ Deriva capacidades desde proposal + design + delta-specs.
- ✓ Al integrar, verifica el trabajo contra los **escenarios GIVEN/WHEN/THEN** de
  los delta-specs, no contra una idea vaga.
- ✓ Al cerrar, actualiza los checkboxes de `tasks.md` y **le pide al PO que corra
  `/opsx:archive`** (no archiva el agente).

## Anti-patrones (deben NO ocurrir)
- ✗ Generar specs a mano ignorando OpenSpec.
- ✗ Tratar `proposal.md` como opcional.
- ✗ Correr `/opsx:archive` por sí mismo, o mergear los delta-specs a mano.
- ✗ Romper requisitos del source of truth que el cambio no tocaba.
