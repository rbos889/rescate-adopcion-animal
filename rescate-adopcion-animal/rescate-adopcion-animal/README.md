# Sistema de Control de Rescate y Adopción Animal

Diseño de la arquitectura lógica de un sistema para registrar rescates, seguir el
estado de los animales y gestionar solicitudes de adopción.

Actividad #1 - Unidad 1: Desarrollo de software, introducción y paradigmas de diseño.

## Contenido

| Carpeta | Descripción |
|---|---|
| `docs/analisis.md` | Actores, requerimientos funcionales y no funcionales |
| `docs/diagrams/` | Diagramas UML (casos de uso, clases) y de patrones (fuentes `.dot` + `.png`) |
| `src/rescate_adopcion/` | Implementación de referencia de los patrones de diseño |
| `tests/` | Pruebas unitarias de los patrones |
| `scripts/` | Script que reproduce el historial Gitflow |

## Patrones de diseño aplicados

| Patrón | Tipo | Dónde |
|---|---|---|
| Factory Method | Creacional | `factory.py` - registro de animales por especie |
| Adapter | Estructural | `notificacion.py` - correo y SMS externos |
| Observer | Comportamiento | `solicitud.py`, `observadores.py` - cambios de estado de una solicitud |

## Ejecución

```bash
python src/main.py
```

## Flujo de trabajo (Gitflow)

- `main`: versiones estables, etiquetadas (`v1.0.0`, `v1.0.1`).
- `develop`: integración continua del diseño.
- `feature/*`: una rama por entregable (análisis, diagramas, cada patrón).
- `release/*`: preparación de versión.
- `hotfix/*`: correcciones urgentes sobre `main`.

Mensajes de commit siguen *Conventional Commits* (`docs:`, `feat:`, `fix:`, `test:`, `chore:`).
