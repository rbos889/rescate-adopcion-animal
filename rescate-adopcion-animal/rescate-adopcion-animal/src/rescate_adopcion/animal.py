"""Dominio: animales rescatados y su ciclo de vida."""
from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


class EstadoAnimal(Enum):
    EN_RESCATE = "En rescate"
    EN_TRATAMIENTO = "En tratamiento"
    DISPONIBLE = "Disponible"
    EN_PROCESO_ADOPCION = "En proceso de adopción"
    ADOPTADO = "Adoptado"


class Animal(ABC):
    """Producto abstracto del patrón Factory Method."""

    _siguiente_id = 1

    def __init__(self, nombre: str, edad_aprox: int, sexo: str, raza: str = "Mestizo"):
        self.id = Animal._siguiente_id
        Animal._siguiente_id += 1
        self.nombre = nombre
        self.edad_aprox = edad_aprox
        self.sexo = sexo
        self.raza = raza
        self.estado = EstadoAnimal.EN_RESCATE
        self.fecha_ingreso = date.today()

    def cambiar_estado(self, nuevo: EstadoAnimal) -> None:
        self.estado = nuevo

    @property
    @abstractmethod
    def especie(self) -> str: ...

    def ficha(self) -> str:
        return (f"[{self.id}] {self.nombre} ({self.especie}, {self.raza}, "
                f"{self.edad_aprox} años) - {self.estado.value}")


class Perro(Animal):
    def __init__(self, nombre, edad_aprox, sexo, raza="Mestizo", tamano="mediano", nivel_energia=3):
        super().__init__(nombre, edad_aprox, sexo, raza)
        self.tamano = tamano
        self.nivel_energia = nivel_energia

    @property
    def especie(self) -> str:
        return "Perro"

    def requiere_ejercicio(self) -> bool:
        return self.nivel_energia >= 4


class Gato(Animal):
    def __init__(self, nombre, edad_aprox, sexo, raza="Mestizo", esterilizado=False, convive_con_otros=True):
        super().__init__(nombre, edad_aprox, sexo, raza)
        self.esterilizado = esterilizado
        self.convive_con_otros = convive_con_otros

    @property
    def especie(self) -> str:
        return "Gato"
