"""Patrón CREACIONAL: Factory Method.

El registro de un animal rescatado no depende de su especie concreta:
cada fábrica decide qué subclase de Animal instanciar.
"""
from abc import ABC, abstractmethod

from .animal import Animal, Gato, Perro


class AnimalFactory(ABC):
    """Creator: define el método plantilla `registrar_animal`."""

    CAMPOS_OBLIGATORIOS = ("nombre", "edad_aprox", "sexo")

    def registrar_animal(self, datos: dict) -> Animal:
        self.validar(datos)
        return self.crear_animal(datos)

    def validar(self, datos: dict) -> None:
        faltantes = [c for c in self.CAMPOS_OBLIGATORIOS if c not in datos]
        if faltantes:
            raise ValueError(f"Faltan campos obligatorios: {', '.join(faltantes)}")

    @abstractmethod
    def crear_animal(self, datos: dict) -> Animal:
        """Factory Method: lo implementa cada fábrica concreta."""


class PerroFactory(AnimalFactory):
    def crear_animal(self, datos: dict) -> Perro:
        return Perro(datos["nombre"], datos["edad_aprox"], datos["sexo"],
                     raza=datos.get("raza", "Mestizo"),
                     tamano=datos.get("tamano", "mediano"),
                     nivel_energia=datos.get("nivel_energia", 3))


class GatoFactory(AnimalFactory):
    def crear_animal(self, datos: dict) -> Gato:
        return Gato(datos["nombre"], datos["edad_aprox"], datos["sexo"],
                    raza=datos.get("raza", "Mestizo"),
                    esterilizado=datos.get("esterilizado", False),
                    convive_con_otros=datos.get("convive_con_otros", True))


_FABRICAS = {"perro": PerroFactory, "gato": GatoFactory}


def obtener_factory(especie: str) -> AnimalFactory:
    """Devuelve la fábrica adecuada; agregar una especie solo requiere registrarla aquí."""
    try:
        return _FABRICAS[especie.lower()]()
    except KeyError:
        raise ValueError(f"Especie no soportada: {especie}") from None
