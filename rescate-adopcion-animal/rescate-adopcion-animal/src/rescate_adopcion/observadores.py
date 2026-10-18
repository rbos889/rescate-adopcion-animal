"""Observadores concretos de una solicitud de adopción."""
from .animal import EstadoAnimal
from .notificacion import Notificador
from .solicitud import EstadoSolicitud, EventoAdopcion, ObservadorAdopcion


class ActualizadorEstadoAnimal(ObservadorAdopcion):
    """Mantiene coherente el estado del animal con el de la solicitud."""

    def actualizar(self, evento: EventoAdopcion) -> None:
        animal = evento.solicitud.animal
        if evento.estado_nuevo == EstadoSolicitud.APROBADA:
            animal.cambiar_estado(EstadoAnimal.EN_PROCESO_ADOPCION)
        elif evento.estado_nuevo == EstadoSolicitud.RECHAZADA:
            animal.cambiar_estado(EstadoAnimal.DISPONIBLE)


class NotificadorAdoptante(ObservadorAdopcion):
    """Avisa al adoptante usando cualquier `Notificador` (email, SMS...)."""

    def __init__(self, notificador: Notificador):
        self._notificador = notificador

    def actualizar(self, evento: EventoAdopcion) -> None:
        s = evento.solicitud
        self._notificador.enviar(
            s.adoptante.correo,
            "Solicitud de adopción",
            f"Tu solicitud por {s.animal.nombre} fue {evento.estado_nuevo.value.lower()}.",
        )


class RegistroAuditoria(ObservadorAdopcion):
    """Deja constancia de cada cambio de estado."""

    def __init__(self):
        self.eventos: list[str] = []

    def actualizar(self, evento: EventoAdopcion) -> None:
        self.eventos.append(
            f"Solicitud de {evento.solicitud.adoptante.nombre} por "
            f"{evento.solicitud.animal.nombre}: "
            f"{evento.estado_anterior.value} -> {evento.estado_nuevo.value}"
        )
