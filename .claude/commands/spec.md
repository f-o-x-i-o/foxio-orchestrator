---
description: Genera el spec-kit en formato OpenSpec para un proyecto nuevo, a partir de una conversación con el PO.
---

Generá el spec-kit del proyecto en formato OpenSpec. Hacelo en diálogo con el PO,
no de una sola. El output son 5 artefactos: constitution + proposal + requirements
+ design + tasks.

Argumentos del usuario: $ARGUMENTS

## Paso 1 — Entrevistá al PO (una ronda, no más de 6 preguntas)

Cubrí lo mínimo indispensable:
- **Problema / por qué**: qué no funciona, qué falta, qué genera pain.
- **Solución propuesta / qué**: qué va a cambiar, a alto nivel.
- **Restricciones duras**: plataforma/target, latencia, CPU/RAM/flash, certificación, licencia.
- **Scope**: qué entra explícitamente y qué queda FUERA en esta iteración.
- **Criterios de aceptación medibles**: cómo sabemos que está hecho (con números).

Si $ARGUMENTS contiene suficiente contexto para varias respuestas, usálo y preguntá
solo lo que falte.

## Paso 2 — Derivá el slug

Del nombre del proyecto generá un slug en kebab-case.
Ejemplo: "Ψ-CLK para VCV Rack 2" → `psi-clk-vcv-rack2`

## Paso 3 — Creá los 5 artefactos

### `specs/constitution.md` — restricciones inviolables del proyecto
(Se crea una vez por proyecto. Si ya existe, actualizá solo las restricciones duras.)

```markdown
# Constitution — [Nombre del proyecto]

> Restricciones inviolables. El foxio_orchestrator y todos los specialists las
> respetan sin excepción. Si algo entra en conflicto con una tarea, gana la
> constitution y se escala al PO.

## Propósito
[Una o dos frases: qué es y para qué.]

## Restricciones duras
- Plataforma / target: [ej. STM32H723, VCV Rack 2 plugin, web]
- Tiempo real / latencia: [ej. buffer de audio < 1 ms, ODR 32 kHz — o N/A]
- Recursos: [CPU %, RAM, flash — con número — o N/A]
- Certificación / seguridad: [ej. IEC 61010 — o N/A]
- Licencia: [ej. GPL-3.0, MIT, propietario]

## Principios de diseño
- [ej. HAL separada de la lógica para testear en host]
- [ej. acceptance criteria siempre medibles con número]

## Fuera de scope (permanente)
- [Lo que nunca entra en este proyecto, en ninguna iteración.]
```

---

### `openspec/changes/{slug}/proposal.md` — el "por qué" y el "qué"

```markdown
# [Título del proyecto / cambio]

## Problema
[Por qué hacemos esto. Qué duele, qué falta, qué riesgo existe sin esto.]

## Solución propuesta
[Qué va a cambiar. Sin detalles de implementación todavía — eso va en design.md.]

## Experiencia esperada
[Qué puede hacer el usuario / sistema que antes no podía. Observable y concreto.]

## No-goals (fuera de scope en esta iteración)
- [Lo que explícitamente NO hacemos acá.]

## Criterios de éxito
| ID | Criterio | Métrica / corte |
|----|----------|-----------------|
| AC-1 | [...] | [ej. THD < 0.5 %] |
| AC-2 | [...] | [...] |
```

---

### `openspec/changes/{slug}/specs/requirements.md` — req + escenarios

```markdown
# Requerimientos — [título]

## Funcionales
- RF-1: [...]
- RF-2: [...]

## No funcionales
- RNF-1: [siempre con número: latencia < X ms, throughput > Y, etc.]
- RNF-2: [...]

## Escenarios
### Escenario A — [nombre descriptivo]
**Dado** [contexto inicial]
**Cuando** [acción / evento]
**Entonces** [resultado observable y verificable]

### Escenario B — [nombre]
[...]
```

---

### `openspec/changes/{slug}/design.md` — enfoque técnico

```markdown
# Diseño técnico — [título]

## Enfoque
[Decisión de arquitectura top-level. Por qué este approach y no otro.]

## Componentes / módulos
[Qué se crea, qué se modifica, interfaces clave entre módulos.]

## Consideraciones de plataforma
[HAL, restricciones de hardware, dependencias externas, ABI.]

## Riesgos y trade-offs
[Lo que podría salir mal o las tensiones entre objetivos. Honesto.]
```

---

### `openspec/changes/{slug}/tasks.md` — checklist de implementación

```markdown
# Tasks — [título]

- [ ] 1.1 [Primera tarea concreta y acotada]
- [ ] 1.2 [...]
- [ ] 2.1 [Segunda área de trabajo]
- [ ] 2.2 [...]
```

Los números agrupan por área (1.x = área 1, 2.x = área 2). Cada item debe ser
ejecutable por un specialist en una sola sesión.

---

## Paso 4 — Mostrá al PO y pedí aprobación

Resumí los artefactos generados (paths + un vistazo a los criterios de éxito y
las tareas). **No pasés el control al foxio_orchestrator hasta recibir OK
explícito del PO.**
