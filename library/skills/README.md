# Librería personal de skills — Foxio

Skills descargadas de skills.sh y evolucionadas con conocimiento Foxio.
Cada una es un `{nombre}.md` en este directorio.

## Cómo funciona

Cada vez que el foxio_orchestrator necesita una capacidad, **mira acá primero**.
Si encontrá tu versión, la usa directamente (sin ir a skills.sh).
Si no existe todavía, la busca en el catálogo externo y te ofrece guardarla acá.

Con el tiempo estas skills acumulan tus decisiones de diseño, restricciones
de plataforma, nomenclatura interna y contexto Foxio — cosas que skills.sh
no puede saber.

## Setup (una vez por máquina)

Agregá esto a tu `.zshrc` / `.bashrc`:

```sh
export FOXIO_SKILLS_LIBRARY="$HOME/Development/foxio-orchestrator/library/skills"
```

Si no definís la var, el foxio_orchestrator busca en ese mismo path por defecto.

## Comandos útiles

| Comando | Qué hace |
|---------|----------|
| `/skill-list` | Muestra todas las skills de la librería con descripción |
| `/skill-save [nombre]` | Guarda/actualiza una skill del proyecto actual a la librería |

## Respaldar

Esta carpeta está versionada en git. Para respaldar tus skills evolucionadas:

```sh
cd ~/Development/foxio-orchestrator
git add library/skills/
git commit -m "skill: actualizo [nombre]"
git push
```
