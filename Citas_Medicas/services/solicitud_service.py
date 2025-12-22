import time
import random
from typing import List, Dict
from . import validaciones


class SolicitudService:
    def __init__(self):
        # Repositorio simple en memoria de pacientes
        self.pacientes = [
            {"cedula": "12345678", "nombre": "Juan Perez", "telefono": "099999999"},
            {"cedula": "87654321", "nombre": "Maria Gomez", "telefono": "098888888"}
        ]

        # Especialidades y médicos con horarios disponibles (slots como 'YYYY-MM-DD HH:MM')
        self.especialidades = {
            "Cardiología": [
                {"id": "med1", "nombre": "Dr. López", "slots": ["2025-12-22 09:00", "2025-12-22 10:00"]},
                {"id": "med2", "nombre": "Dra. Martínez", "slots": ["2025-12-22 11:00", "2025-12-23 09:00"]}
            ],
            "Pediatría": [
                {"id": "med3", "nombre": "Dr. Rivera", "slots": ["2025-12-22 09:30", "2025-12-22 10:30"]}
            ]
        }

        # Solicitudes provisionales y historial de notificaciones
        self.solicitudes = []  # cada item dict con datos y estado provisional/confirmada
        self.historial_notificaciones = []

    def buscar_paciente_por_cedula(self, cedula: str):
        for p in self.pacientes:
            if p["cedula"] == cedula:
                return p
        return None

    def listar_especialidades(self) -> List[str]:
        return list(self.especialidades.keys())

    def listar_medicos_por_especialidad(self, especialidad: str) -> List[Dict]:
        return self.especialidades.get(especialidad, [])

    def obtener_horarios_disponibles(self, medico_id: str) -> List[str]:
        for espec, medicos in self.especialidades.items():
            for m in medicos:
                if m["id"] == medico_id:
                    # devolver copia
                    return list(m.get("slots", []))
        return []

    def reservar_horario_provisional(self, medico_id: str, slot: str, paciente_cedula: str, especialidad: str) -> Dict:
        # comprobar existencia del slot y reservarlo (eliminar de lista pública)
        for medicos in self.especialidades.values():
            for m in medicos:
                if m["id"] == medico_id:
                    if slot in m.get("slots", []):
                        m["slots"].remove(slot)
                        codigo = self._generar_codigo_solicitud()
                        solicitud = {
                            "codigo": codigo,
                            "paciente_cedula": paciente_cedula,
                            "medico_id": medico_id,
                            "especialidad": especialidad,
                            "slot": slot,
                            "estado": "provisional",
                            "timestamp": time.time()
                        }
                        self.solicitudes.append(solicitud)
                        return solicitud
                    else:
                        raise ValueError("Horario no disponible")
        raise ValueError("Médico no encontrado")

    def confirmar_solicitud(self, codigo: str) -> Dict:
        for s in self.solicitudes:
            if s["codigo"] == codigo:
                s["estado"] = "enviado_a_medico"
                return s
        raise ValueError("Solicitud no encontrada")

    def generar_comprobante(self, solicitud: Dict) -> str:
        # comprobante simple textual
        texto = (
            f"Comprobante - Código: {solicitud['codigo']}\n"
            f"Especialidad: {solicitud['especialidad']}\n"
            f"Médico ID: {solicitud['medico_id']}\n"
            f"Fecha y Hora: {solicitud['slot']}\n"
            f"Estado: {solicitud['estado']}\n"
        )
        return texto

    def enviar_notificacion(self, paciente: Dict, solicitud: Dict) -> bool:
        mensaje = f"Solicitud {solicitud['codigo']} - {solicitud['especialidad']} {solicitud['slot']}"
        registro = {"cedula": paciente.get("cedula"), "mensaje": mensaje, "timestamp": time.time()}
        self.historial_notificaciones.append(registro)
        return True

    def registrar_historial_notificaciones(self, registro: Dict):
        self.historial_notificaciones.append(registro)

    def _generar_codigo_solicitud(self) -> str:
        return f"S-{int(time.time())}-{random.randint(100,999)}"
