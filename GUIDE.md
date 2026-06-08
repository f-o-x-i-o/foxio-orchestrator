# Guía para dummies — foxio_orchestrator

Esta guía explica TODO de cero, sin asumir que ya sabés cómo funciona. Si es tu
primera vez, leé esto antes que el README.

---

## 1. ¿Qué es esto, en una frase?

Un sistema para que **vos (el jefe del proyecto, el "Product Owner") le pidas a un
agente de IA que arme un equipo de IA a medida** para cada proyecto, en vez de
tener un equipo fijo. El agente jefe se llama **foxio_orchestrator**.

## 2. Las 4 piezas (analogía de un estudio)

| Pieza | Qué es | Analogía |
|-------|--------|----------|
| **foxio_orchestrator** | El agente que planifica y reparte el trabajo | El director del estudio |
| **specialist** | Un agente ejecutor genérico que se despacha N veces | Un freelance que viene por una tarea |
| **skill** | Un manual de "cómo hacer X" que un specialist lee | El manual de procedimiento |
| **OpenSpec** | El documento que dice QUÉ hay que construir | El brief del cliente |

Lo importante:
- El **specialist no sabe nada** por sí mismo. Se vuelve "experto en firmware"
  porque el orquestador le da el **manual (skill) de firmware** para esa tarea.
- Las **skills se bajan de internet** (un catálogo llamado **skills.sh**) cuando
  hacen falta. No vienen todas de fábrica.

## 3. La idea clave: tu librería personal de skills

Acá está la magia que hace esto tuyo y no genérico:

> Cuando bajás una skill (ej: "diseñador UX") y la usás en un proyecto, la podés
> **mejorar** con tus decisiones y tu contexto Foxio. Después la **guardás en tu
> librería personal**. La próxima vez que arranques un proyecto que necesita un
> diseñador UX, el orquestador usa **TU versión mejorada**, no la genérica de internet.

Tu librería vive en este repo (`library/skills/`), versionada en git. Es decir:
tus skills evolucionan, quedan guardadas, y las respaldás en GitHub.

```
Proyecto 1:  bajás "ux-designer" genérico → lo mejorás → lo guardás
Proyecto 2:  el orquestador ya arranca con TU "ux-designer"  ← evolución
Proyecto 3:  le agregás más cosas → lo volvés a guardar      ← sigue creciendo
```

## 4. Instalación paso a paso

### 4.1. Lo que necesitás una sola vez (por máquina)

1. **Node.js 20.19 o más nuevo.** Verificá:
   ```bash
   node --version
   ```
2. **El CLI de OpenSpec** (maneja los specs):
   ```bash
   npm install -g @fission-ai/openspec@latest
   ```
3. **Decirle al sistema dónde está tu librería personal.** Abrí `~/.zshrc`
   (o `~/.bashrc`) y agregá al final:
   ```bash
   export FOXIO_SKILLS_LIBRARY="$HOME/Development/foxio-orchestrator/library/skills"
   ```
   Cerrá y reabrí la terminal. (Ajustá el path si clonaste el repo en otro lado.)

### 4.2. En cada proyecto nuevo

1. Copiá la carpeta `.claude/` y el archivo `specs/constitution.md` de este
   toolkit a la raíz de tu proyecto.
2. (Opcional) Instalá la skill para crear skills propias:
   ```bash
   npx skills add anthropics/skills --skill skill-creator -a claude-code --copy -y
   ```
3. Abrí Claude Code en el proyecto (`claude`), escribí `/agents` y confirmá que
   aparecen `foxio_orchestrator` y `specialist`.

## 5. Tu primer proyecto, de punta a punta

> Ejemplo: un módulo de reloj para VCV Rack.

**Paso 1 — Especificá qué querés.** En Claude Code:
```
/spec un módulo de clock para VCV Rack 2 con swing y división configurable
```
Esto prepara OpenSpec y te pide correr el comando nativo:
```
/opsx:propose clock con swing y división
```
OpenSpec crea una carpeta `openspec/changes/clock-swing/` con 4 archivos:
- `proposal.md` — por qué y qué (con criterios de éxito)
- `specs/` — los requisitos en detalle (formato "delta": qué se AGREGA/MODIFICA/QUITA)
- `design.md` — cómo, técnicamente
- `tasks.md` — la lista de tareas

**Paso 2 — Revisá y validá.**
```bash
openspec validate
```
Leé los archivos. Si te gustan, aprobás.

**Paso 3 — Soltá al orquestador.** En el chat:
```
foxio_orchestrator, leé el cambio y armá el equipo
```
El orquestador va a:
1. Leer la constitution + el cambio.
2. Decir qué **capacidades** hacen falta (ej: "DSP de audio", "UI de VCV Rack").
3. Para cada una: ¿está en **tu librería**? la usa. ¿No? busca en skills.sh y
   **te muestra los candidatos**.
4. **Frená acá:** vos aprobás qué instalar. Nada se instala sin tu OK.

**Paso 4 — Ejecuta.** Despacha specialists (uno por tarea), cada uno con su skill.
Te va resumiendo. En los hitos importantes, **para y te pregunta** antes de seguir.

**Paso 5 — Cerrá.** Cuando está todo:
```
/opsx:archive
```
Esto "oficializa" los cambios (los mergea al source of truth).

**Paso 6 — Capitalizá lo aprendido.** Si una skill quedó mejor que la original:
```
/skill-save dsp-audio
```
La guarda en tu librería. Después respaldala:
```bash
cd ~/Development/foxio-orchestrator && git add library/skills/ && git commit -m "skill: dsp-audio" && git push
```

## 6. La constitution (importante)

`specs/constitution.md` son tus **reglas inviolables** del proyecto: plataforma,
límites de CPU/RAM, latencia, licencia, lo que NUNCA se hace. Si una skill o una
tarea las contradice, **gana la constitution** y el agente te escala el conflicto.
Llenala al principio de cada proyecto.

## 7. Reglas de oro que el orquestador SIEMPRE respeta

1. **Nunca instala, crea ni borra una skill sin tu sí explícito.**
2. **Nunca hace algo irreversible** (cambiar arquitectura, borrar trabajo) sin tu OK.
3. **Siempre mira tu librería personal antes** de bajar algo de internet.
4. **Te para en los hitos** para que apruebes antes de seguir gastando.
5. Todo alta/baja de skill queda anotada en `.claude/skills/SKILL_LOG.md`.

## 8. Preguntas frecuentes

**¿Por qué el equipo no es fijo?** Porque un proyecto de firmware no necesita lo
mismo que uno web. Armar el equipo a medida evita cargar contexto inútil.

**¿"skill" = "agente"?** No. Un agente (specialist) es un trabajador que corre.
Una skill es un manual que ese trabajador lee. Un specialist + una skill de
firmware = "un especialista en firmware" por esa tarea.

**¿Dónde viven mis skills mejoradas?** En `library/skills/<nombre>/SKILL.md`,
dentro de este repo, en git. Por eso las podés respaldar y versionar.

**¿Qué pasa si no encuentra una skill buena?** Te avisa y propone crearla con
`skill-creator`, o que el specialist la haga sin manual.

**¿El orquestador puede correr `/spec` o `/skill-save` solo?** No: los slash
commands son tuyos. El orquestador te pide que los corras, o hace los mismos pasos
manualmente en la terminal.

**¿Esto es magia?** No. El orquestador corre comandos reales (`npx skills`,
`openspec`) en una terminal y lee los archivos que generan. Funciona en la medida
en que esas herramientas y el catálogo de skills sean buenos para tu dominio.

## 9. Si algo no anda

| Síntoma | Probable causa |
|---------|----------------|
| "no encuentro la librería en…" | Falta `export FOXIO_SKILLS_LIBRARY` o el path está mal |
| `/agents` no muestra los agentes | No copiaste `.claude/` a la raíz del proyecto |
| `openspec: command not found` | Falta `npm install -g @fission-ai/openspec` |
| El orquestador "no ve" tu skill | La guardaste como archivo suelto en vez de carpeta `<nombre>/SKILL.md` |
| Querés chequear que el toolkit está sano | `python3 tests/validate.py` |
