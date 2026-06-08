---
description: Bootstrapea OpenSpec en el proyecto (instala el CLI + init) y arranca el flujo de spec con /opsx:propose.
---

Preparás el proyecto para spec-driven development con OpenSpec real
(`@fission-ai/openspec`). NO generás los specs a mano: OpenSpec tiene su propio
flujo (`/opsx:propose → apply → sync → archive`) y su validador. Tu trabajo es
dejar todo instalado y manejar la constitution de Foxio, que OpenSpec no cubre.

Argumentos del usuario: $ARGUMENTS

## Paso 1 — ¿Está el CLI de OpenSpec?
```bash
openspec --version 2>/dev/null || echo "NO_INSTALADO"
```
Si dice `NO_INSTALADO`, mostrale al PO cómo instalarlo y esperá:
```bash
npm install -g @fission-ai/openspec@latest   # requiere Node ≥ 20.19
```

## Paso 2 — ¿Está inicializado en el proyecto?
```bash
test -d openspec && echo "YA_INIT" || echo "FALTA_INIT"
```
Si falta, corré `openspec init` (genera `openspec/`, `config.yaml` y los comandos
nativos `/opsx:*` para Claude Code). Mostrale el output al PO.

## Paso 3 — Constitution de Foxio (capa propia, encima de OpenSpec)
OpenSpec maneja proposals/specs/tasks, pero NO tiene el concepto de "restricciones
inviolables" de Foxio. Asegurá que exista `specs/constitution.md`:
```bash
test -f specs/constitution.md && echo "OK" || echo "FALTA"
```
- Si falta, copiá la plantilla desde este toolkit y entrevistá al PO SOLO para las
  restricciones duras (plataforma/target, latencia, CPU/RAM/flash, certificación,
  licencia). `specs/constitution.md` es la ÚNICA fuente de la constitution —
  no la dupliques en otro lado.
- Si querés, sembrá el contexto en `openspec/config.yaml` (sección `context`/`rules`)
  a partir de la constitution, para que OpenSpec lo tenga presente.

## Paso 4 — Arrancá el spec con el comando nativo
Decile al PO que corra el flujo de OpenSpec (vos no podés invocar slash commands
por él):

> "Todo listo. Para especificar el cambio, corré:
> **`/opsx:propose <descripción-corta>`**
> OpenSpec va a crear `openspec/changes/<slug>/` con `proposal.md`, `specs/`
> (delta-specs ADDED/MODIFIED/REMOVED), `design.md` y `tasks.md`.
> Después validá con `openspec validate` y, cuando lo apruebes, decime
> *'leé el cambio y armá el equipo'* para que el foxio_orchestrator lo ejecute."

Si OpenSpec no estuviera disponible por algún motivo, avisá al PO y ofrecé el
fallback mínimo (generar a mano `openspec/changes/<slug>/{proposal,design,tasks}.md`
+ `specs/<dominio>/spec.md` en formato delta), aclarando que `openspec validate`
no estará disponible hasta instalar el CLI.
