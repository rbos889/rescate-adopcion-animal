# Análisis del escenario

## Actores

| Actor | Rol |
|---|---|
| Rescatista | Reporta y registra animales rescatados en la calle |
| Voluntario | Apoya el registro de fichas y el seguimiento post-adopción |
| Veterinario | Evalúa, trata y vacuna a los animales |
| Adoptante | Consulta animales disponibles y solicita adopciones |
| Administrador del refugio | Gestiona estados, aprueba adopciones, usuarios y reportes |
| Servicio de correo/SMS (secundario) | Sistema externo que envía las notificaciones |

## Requerimientos funcionales

| ID | Requerimiento |
|---|---|
| RF01 | Registrar un rescate (fecha, ubicación, condición) |
| RF02 | Registrar la ficha de cada animal rescatado |
| RF03 | Registrar evaluaciones veterinarias, tratamientos y vacunas |
| RF04 | Controlar el estado del animal: en rescate, en tratamiento, disponible, en proceso de adopción, adoptado |
| RF05 | Consultar y filtrar animales disponibles para adopción |
| RF06 | Registrar adoptantes y recibir solicitudes de adopción |
| RF07 | Evaluar (aprobar o rechazar) solicitudes de adopción |
| RF08 | Formalizar la adopción y generar el contrato |
| RF09 | Registrar el seguimiento post-adopción |
| RF10 | Notificar a los involucrados por correo o SMS |
| RF11 | Generar reportes (rescates, adopciones, animales por estado) |
| RF12 | Autenticar usuarios y gestionar roles y permisos |

## Requerimientos no funcionales

| ID | Atributo | Descripción |
|---|---|---|
| RNF01 | Seguridad | Acceso por roles; datos personales protegidos |
| RNF02 | Usabilidad | Interfaz simple para voluntarios sin formación técnica |
| RNF03 | Escalabilidad | Nuevas especies y canales de notificación sin modificar el núcleo |
| RNF04 | Mantenibilidad | Bajo acoplamiento, patrones de diseño, pruebas unitarias |
| RNF05 | Disponibilidad | Operación continua en horario de atención del refugio |
| RNF06 | Trazabilidad | Auditoría de los cambios de estado |

## Reglas de negocio

- Solo los animales en estado *Disponible* pueden recibir solicitudes de adopción.
- Una solicitud se resuelve una sola vez (aprobada o rechazada).
- Al aprobarse una solicitud, el animal pasa a *En proceso de adopción*; si se rechaza, vuelve a *Disponible*.
- Todo animal tiene una única ficha médica con cero o más tratamientos.
