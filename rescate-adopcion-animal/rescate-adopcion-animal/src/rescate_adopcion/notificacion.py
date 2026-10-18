"""Patrón ESTRUCTURAL: Adapter.

El sistema trabaja con la interfaz `Notificador`. Los servicios externos de
correo y SMS tienen interfaces distintas e incompatibles; los adaptadores las
traducen sin modificar el código de los servicios.
"""
from abc import ABC, abstractmethod


class Notificador(ABC):
    """Target: interfaz que espera el sistema."""

    @abstractmethod
    def enviar(self, destino: str, asunto: str, mensaje: str) -> bool: ...


# ----- Adaptees (servicios externos simulados, interfaz incompatible) -----
class ServicioCorreoExterno:
    def sendMail(self, to: str, subject: str, body: str) -> int:
        print(f"  [correo] To: {to} | {subject} | {body}")
        return 200


class ApiSmsExterna:
    def enviarSms(self, numero: str, texto: str) -> str:
        print(f"  [sms] {numero}: {texto}")
        return "OK"


# ----- Adapters -----
class NotificadorEmailAdapter(Notificador):
    def __init__(self, servicio: ServicioCorreoExterno | None = None):
        self._servicio = servicio or ServicioCorreoExterno()

    def enviar(self, destino: str, asunto: str, mensaje: str) -> bool:
        return self._servicio.sendMail(destino, asunto, mensaje) == 200


class NotificadorSmsAdapter(Notificador):
    def __init__(self, api: ApiSmsExterna | None = None):
        self._api = api or ApiSmsExterna()

    def enviar(self, destino: str, asunto: str, mensaje: str) -> bool:
        # El SMS no tiene asunto: se antepone al texto.
        return self._api.enviarSms(destino, f"{asunto}: {mensaje}") == "OK"
