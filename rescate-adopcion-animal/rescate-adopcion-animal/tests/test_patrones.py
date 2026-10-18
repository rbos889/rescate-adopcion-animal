import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rescate_adopcion.animal import EstadoAnimal, Gato, Perro  # noqa: E402
from rescate_adopcion.factory import obtener_factory  # noqa: E402
from rescate_adopcion.notificacion import (ApiSmsExterna, Notificador,  # noqa: E402
                                           NotificadorEmailAdapter, NotificadorSmsAdapter)
from rescate_adopcion.observadores import (ActualizadorEstadoAnimal,  # noqa: E402
                                           RegistroAuditoria)
from rescate_adopcion.solicitud import Adoptante, EstadoSolicitud, SolicitudAdopcion  # noqa: E402


def _animal_disponible():
    a = obtener_factory("gato").registrar_animal({"nombre": "Luna", "edad_aprox": 2, "sexo": "H"})
    a.cambiar_estado(EstadoAnimal.DISPONIBLE)
    return a


class TestFactory(unittest.TestCase):
    def test_crea_subclase_correcta(self):
        self.assertIsInstance(obtener_factory("perro").registrar_animal(
            {"nombre": "Max", "edad_aprox": 3, "sexo": "M"}), Perro)
        self.assertIsInstance(obtener_factory("Gato").registrar_animal(
            {"nombre": "Luna", "edad_aprox": 2, "sexo": "H"}), Gato)

    def test_estado_inicial_en_rescate(self):
        a = obtener_factory("perro").registrar_animal({"nombre": "Max", "edad_aprox": 3, "sexo": "M"})
        self.assertEqual(a.estado, EstadoAnimal.EN_RESCATE)

    def test_validacion_y_especie_invalida(self):
        with self.assertRaises(ValueError):
            obtener_factory("perro").registrar_animal({"nombre": "Max"})
        with self.assertRaises(ValueError):
            obtener_factory("dragon")


class TestObserver(unittest.TestCase):
    def setUp(self):
        self.animal = _animal_disponible()
        self.sol = SolicitudAdopcion(self.animal, Adoptante("Ana", "ana@x.com"), "Quiero adoptar")
        self.auditoria = RegistroAuditoria()
        self.sol.suscribir(ActualizadorEstadoAnimal())
        self.sol.suscribir(self.auditoria)

    def test_aprobar_actualiza_animal_y_auditoria(self):
        self.sol.aprobar()
        self.assertEqual(self.sol.estado, EstadoSolicitud.APROBADA)
        self.assertEqual(self.animal.estado, EstadoAnimal.EN_PROCESO_ADOPCION)
        self.assertEqual(len(self.auditoria.eventos), 1)

    def test_rechazar_deja_animal_disponible(self):
        self.sol.rechazar("Sin visita previa")
        self.assertEqual(self.animal.estado, EstadoAnimal.DISPONIBLE)

    def test_no_se_resuelve_dos_veces(self):
        self.sol.aprobar()
        with self.assertRaises(ValueError):
            self.sol.rechazar()

    def test_solo_animales_disponibles(self):
        en_rescate = obtener_factory("perro").registrar_animal({"nombre": "Max", "edad_aprox": 3, "sexo": "M"})
        with self.assertRaises(ValueError):
            SolicitudAdopcion(en_rescate, Adoptante("Ana", "ana@x.com"), "Quiero adoptar")


class TestAdapter(unittest.TestCase):
    def test_ambos_adaptadores_cumplen_la_interfaz(self):
        for adaptador in (NotificadorEmailAdapter(), NotificadorSmsAdapter()):
            self.assertIsInstance(adaptador, Notificador)
            self.assertTrue(adaptador.enviar("destino", "Asunto", "Mensaje"))

    def test_sms_concatena_asunto(self):
        class ApiFalsa(ApiSmsExterna):
            def enviarSms(self, numero, texto):
                self.ultimo = (numero, texto)
                return "OK"
        api = ApiFalsa()
        NotificadorSmsAdapter(api).enviar("099", "Hola", "Mundo")
        self.assertEqual(api.ultimo, ("099", "Hola: Mundo"))


if __name__ == "__main__":
    unittest.main()
