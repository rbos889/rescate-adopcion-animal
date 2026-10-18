"""Patrón de COMPORTAMIENTO: Observer.

`SolicitudAdopcion` es el Subject: al cambiar de estado avisa a todos los
observadores suscritos sin conocer su implementación.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .animal import Animal, EstadoAnimal


class EstadoSolicitud(Enum):
    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"


@dataclass
class Adoptante:
    nombre: str
    correo: str
    telefono: str = ""


@dataclass
class EventoAdopcion:
    solicitud: "SolicitudAdopcion"
    estado_anterior: EstadoSolicitud
    estado_nuevo: EstadoSolicitud


class ObservadorAdopcion(ABC):
    """Observer."""

    @abstractmethod
    def actualizar(self, evento: EventoAdopcion) -> None: ...


class SolicitudAdopcion:
    """Subject."""

    def __init__(self, animal: Animal, adoptante: Adoptante, motivo: str):
        if animal.estado != EstadoAnimal.DISPONIBLE:
            raise ValueError("Solo se puede solicitar la adopción de animales disponibles")
        self.animal = animal
        self.adoptante = adoptante
        self.motivo = motivo
        self.estado = EstadoSolicitud.PENDIENTE
        self._observadores: list[ObservadorAdopcion] = []

    def suscribir(self, observador: ObservadorAdopcion) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador: ObservadorAdopcion) -> None:
        self._observadores.remove(observador)

    def aprobar(self) -> None:
        self._cambiar_estado(EstadoSolicitud.APROBADA)

    def rechazar(self, motivo: str = "") -> None:
        self.motivo_rechazo = motivo
        self._cambiar_estado(EstadoSolicitud.RECHAZADA)

    def _cambiar_estado(self, nuevo: EstadoSolicitud) -> None:
        if self.estado != EstadoSolicitud.PENDIENTE:
            raise ValueError("La solicitud ya fue resuelta")
        evento = EventoAdopcion(self, self.estado, nuevo)
        self.estado = nuevo
        self._notificar(evento)

    def _notificar(self, evento: EventoAdopcion) -> None:
        for obs in list(self._observadores):
            obs.actualizar(evento)
