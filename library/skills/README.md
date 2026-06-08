# Librería personal de skills — Foxio

Tus skills evolucionadas, versionadas en git. Cada skill es una **carpeta**
`<nombre>/SKILL.md` (+ archivos auxiliares si los tiene) — el mismo formato que
usa Claude Code y `npx skills`, así que son skills reales y cargables, no docs sueltos.

```
library/skills/
  README.md
  ux-designer/
    SKILL.md
  firmware-stm32/
    SKILL.md
    checklists/...
```

## Cómo funciona

Cuando el foxio_orchestrator necesita una capacidad, **mira acá primero**. Si
encuentra tu versión, copia la carpeta al proyecto (`cp -R "$LIBRARY/<nombre>"
.claude/skills/`) y la usa. Si no existe, la busca en skills.sh y te ofrece
guardarla acá. Con el tiempo, estas skills acumulan tus decisiones de diseño,
restricciones de plataforma y contexto Foxio — cosas que skills.sh no sabe.

## Setup (una vez por máquina)

Agregá a tu `.zshrc` / `.bashrc`:
```sh
export FOXIO_SKILLS_LIBRARY="$HOME/Development/foxio-orchestrator/library/skills"
```
Si no la definís, se usa ese path por default. **Si el path no existe, el
orquestador y los comandos avisan en vez de seguir en silencio** (así no creés que
"no hay skill" cuando en realidad no la estás viendo).

## Comandos

| Comando | Qué hace |
|---------|----------|
| `/skill-list` | Lista las skills de la librería con descripción y origen |
| `/skill-save <nombre>` | Guarda/actualiza una skill del proyecto actual acá |

## Respaldar (es un repo git)

```sh
cd ~/Development/foxio-orchestrator
git add library/skills/
git commit -m "skill: actualizo <nombre>"
git push
```
