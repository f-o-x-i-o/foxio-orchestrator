---
description: Genera el spec-kit (constitution.md + spec.md) de un proyecto nuevo a partir de una conversación con el PO.
---

Vas a generar el spec-kit del proyecto. Hacelo en diálogo con el PO, no de una.

1. Preguntá lo mínimo indispensable para llenar la plantilla: objetivo, scope,
   restricciones duras (tiempo real, certificación, presupuesto de CPU/memoria),
   plataforma de hardware/target, y criterios de aceptación medibles.
2. Escribí `specs/constitution.md` (principios y restricciones inviolables del
   proyecto) y `specs/spec.md` (requerimientos concretos y acceptance criteria).
3. Mostrale al PO el resultado y pedí aprobación ANTES de pasarle el control al
   foxio_orchestrator para descomponer y despachar.

Argumentos del usuario: $ARGUMENTS
