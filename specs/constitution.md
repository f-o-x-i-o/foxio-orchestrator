# Constitution — [NOMBRE DEL PROYECTO]

> Principios y restricciones inviolables. El foxio_orchestrator y todos los subagentes
> los respetan sin excepción. Si algo acá entra en conflicto con una tarea, gana
> la constitution y se escala al PO.

## Propósito
[Una o dos frases: qué es y para qué.]

## Restricciones duras
- Plataforma / target: [ej. STM32H723, Daisy Seed, ESP32, web]
- Tiempo real / latencia: [ej. buffer de audio < 1ms, ODR 32kHz]
- Recursos: [presupuesto de CPU, RAM, flash]
- Certificación / seguridad: [ej. IEC 61010, UL/CE, o N/A]
- Licencia: [ej. MIT/Apache 2.0, propietario]

## Principios de diseño
- [ej. HAL separada de la lógica para testear en host]
- [ej. todo acceptance criterion debe ser medible numéricamente]

## Fuera de scope (explícito)
- [Lo que NO vamos a hacer en esta fase.]
