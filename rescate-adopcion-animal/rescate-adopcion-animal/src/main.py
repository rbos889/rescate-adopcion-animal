"""Demo del flujo completo: rescate -> disponible -> solicitud -> aprobación."""
from rescate_adopcion.animal import EstadoAnimal
from rescate_adopcion.factory import obtener_factory
from rescate_adopcion.notificacion import NotificadorEmailAdapter
from rescate_adopcion.observadores import (ActualizadorEstadoAnimal, NotificadorAdoptante,
                                           RegistroAuditoria)
from rescate_adopcion.solicitud import Adoptante, SolicitudAdopcion


def main() -> None:
    # 1) Factory Method: registrar un animal rescatado
    perro = obtener_factory("perro").registrar_animal(
        {"nombre": "Max", "edad_aprox": 3, "sexo": "M", "tamano": "grande", "nivel_energia": 5})
    print(perro.ficha())
    perro.cambiar_estado(EstadoAnimal.EN_TRATAMIENTO)
    perro.cambiar_estado(EstadoAnimal.DISPONIBLE)

    # 2) Observer + Adapter: solicitud de adopción con notificaciones
    adoptante = Adoptante("Ana Pérez", "ana@correo.com")
    solicitud = SolicitudAdopcion(perro, adoptante, "Tengo patio y tiempo para él")
    auditoria = RegistroAuditoria()
    solicitud.suscribir(ActualizadorEstadoAnimal())
    solicitud.suscribir(NotificadorAdoptante(NotificadorEmailAdapter()))
    solicitud.suscribir(auditoria)

    solicitud.aprobar()
    print(perro.ficha())
    print(*auditoria.eventos, sep="\n")


if __name__ == "__main__":
    main()
