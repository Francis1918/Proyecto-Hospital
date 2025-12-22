from __future__ import annotations

from datetime import datetime, date, time, timedelta
from typing import Dict, List, Optional, Tuple
import random
import string

from Pacientes import PacienteController
from .models import CitaMedica, Notificacion


class CitasMedicasController:
    """
    Controlador del módulo de Citas Médicas (persistencia en memoria).
    """

    def __init__(self, paciente_controller: Optional[PacienteController] = None):
        self.pacientes = paciente_controller or PacienteController()

        # Catálogo demo (puedes cambiarlo)
        self._especialidades: List[str] = [
            "Medicina General",
            "Pediatría",
            "Cardiología",
            "Ginecología",
            "Traumatología",
        ]

        # especialidad -> médicos
        self._medicos_por_especialidad: Dict[str, List[dict]] = {
            "Medicina General": [
                {"nombre": "Dr. Andrés Paredes", "consultorio": "101"},
                {"nombre": "Dra. Sofía Vega", "consultorio": "102"},
            ],
            "Pediatría": [
                {"nombre": "Dra. María Salazar", "consultorio": "201"},
            ],
            "Cardiología": [
                {"nombre": "Dr. Diego Herrera", "consultorio": "301"},
            ],
            "Ginecología": [
                {"nombre": "Dra. Valeria Luna", "consultorio": "401"},
            ],
            "Traumatología": [
                {"nombre": "Dr. Carlos Ríos", "consultorio": "501"},
            ],
        }

        # Agenda laboral por médico: (hora_inicio, hora_fin)
        self._agenda_medicos: Dict[str, Tuple[int, int]] = {
            m["nombre"]: (9, 17)
            for medicos in self._medicos_por_especialidad.values()
            for m in medicos
        }

        # Persistencia en memoria
        self._citas: Dict[str, CitaMedica] = {}           # codigo -> cita
        self._notificaciones: List[Notificacion] = []     # historial

        # Ejemplo
        self._cargar_datos_ejemplo()

    # ---------------------------
    # Validaciones
    # ---------------------------
    @staticmethod
    def validar_formato_cedula(cc: str) -> Tuple[bool, str]:
        cc = (cc or "").strip()
        if not cc:
            return False, "Debe ingresar la cédula."
        if not cc.isdigit():
            return False, "La cédula debe contener solo números."
        if len(cc) != 10:
            return False, "La cédula debe tener 10 dígitos."
        return True, "Formato de cédula válido."

    @staticmethod
    def _generar_codigo() -> str:
        cuerpo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"CM-{cuerpo}"

    def _cargar_datos_ejemplo(self):
        p = self.pacientes.consultar_paciente("1234567890")
        if not p:
            return

        codigo = "CM-DEMO1"
        self._citas[codigo] = CitaMedica(
            codigo=codigo,
            cc_paciente=p.cc,
            nombre_paciente=f"{p.nombre} {p.apellido}",
            especialidad="Medicina General",
            medico="Dr. Andrés Paredes",
            fecha=(date.today() + timedelta(days=1)),
            hora=time(10, 0),
            consultorio="101",
            estado="Confirmada",
        )

    # ---------------------------
    # Catálogo y agenda
    # ---------------------------
    def obtener_especialidades(self) -> List[str]:
        return list(self._especialidades)

    def obtener_medicos_por_especialidad(self, especialidad: str) -> List[str]:
        medicos = self._medicos_por_especialidad.get(especialidad, [])
        return [m["nombre"] for m in medicos]

    def obtener_todos_medicos(self) -> List[str]:
        return sorted(list(self._agenda_medicos.keys()))

    def obtener_consultorio_medico(self, medico: str) -> str:
        for medicos in self._medicos_por_especialidad.values():
            for m in medicos:
                if m["nombre"] == medico:
                    return m.get("consultorio", "")
        return ""

    def obtener_agenda_medico(self, medico: str) -> Tuple[int, int]:
        return self._agenda_medicos.get(medico, (9, 17))

    def registrar_agenda_medico(self, medico: str, hora_inicio: int, hora_fin: int) -> Tuple[bool, str]:
        if medico not in self._agenda_medicos:
            return False, "Médico no encontrado."
        if not (0 <= hora_inicio <= 23 and 1 <= hora_fin <= 24 and hora_inicio < hora_fin):
            return False, "Rango de horas inválido."
        self._agenda_medicos[medico] = (hora_inicio, hora_fin)
        return True, "Agenda registrada/actualizada correctamente."

    def obtener_horarios_disponibles(self, medico: str, fecha: date) -> List[time]:
        """
        Retorna horas disponibles (cada 60 min) según agenda y citas no canceladas.
        """
        if medico not in self._agenda_medicos:
            return []

        start, end = self._agenda_medicos[medico]
        horas = [time(h, 0) for h in range(start, end)]

        ocupadas = {
            c.hora
            for c in self._citas.values()
            if c.medico == medico and c.fecha == fecha and c.estado != "Cancelada"
        }
        return [h for h in horas if h not in ocupadas]

    def consultar_agenda(self, medico: str, fecha: date) -> List[CitaMedica]:
        citas = [c for c in self._citas.values() if c.medico == medico and c.fecha == fecha]
        return sorted(citas, key=lambda c: c.hora)

    # ---------------------------
    # CRUD Citas
    # ---------------------------
    def solicitar_cita(
        self,
        cc: str,
        especialidad: str,
        medico: str,
        fecha: date,
        hora: time
    ) -> Tuple[bool, str, Optional[CitaMedica]]:

        ok, msg = self.validar_formato_cedula(cc)
        if not ok:
            return False, msg, None

        paciente = self.pacientes.consultar_paciente(cc)
        if not paciente:
            return False, "Paciente no registrado en la base de datos.", None

        if especialidad not in self._especialidades:
            return False, "Especialidad no válida.", None

        if medico not in self.obtener_medicos_por_especialidad(especialidad):
            return False, "No existen médicos disponibles para esta especialidad.", None

        disponibles = self.obtener_horarios_disponibles(medico, fecha)
        if not disponibles:
            return False, "El médico seleccionado no tiene horarios disponibles.", None

        if hora not in disponibles:
            return False, "El horario seleccionado ya no está disponible.", None

        codigo = self._generar_codigo()
        while codigo in self._citas:
            codigo = self._generar_codigo()

        cita = CitaMedica(
            codigo=codigo,
            cc_paciente=cc,
            nombre_paciente=f"{paciente.nombre} {paciente.apellido}",
            especialidad=especialidad,
            medico=medico,
            fecha=fecha,
            hora=hora,
            consultorio=self.obtener_consultorio_medico(medico),
            estado="Confirmada"
        )
        self._citas[codigo] = cita

        # Notificación automática (simulada)
        self._notificar_cita_programada(cita)

        return True, "Cita registrada con éxito.", cita

    def consultar_cita_por_codigo(self, codigo: str) -> Optional[CitaMedica]:
        return self._citas.get((codigo or "").strip())

    def consultar_citas_por_paciente(self, cc: str) -> List[CitaMedica]:
        cc = (cc or "").strip()
        citas = [c for c in self._citas.values() if c.cc_paciente == cc]
        return sorted(citas, key=lambda c: (c.fecha, c.hora))

    def modificar_cita(self, codigo: str, nueva_fecha: date, nueva_hora: time) -> Tuple[bool, str, Optional[CitaMedica]]:
        cita = self.consultar_cita_por_codigo(codigo)
        if not cita:
            return False, "No se encontró la cita.", None

        if cita.estado == "Cancelada":
            return False, "No se puede modificar una cita cancelada.", None

        # Política 12h
        if datetime.now() > (cita.fecha_hora() - timedelta(hours=12)):
            return False, "No se puede modificar la cita por política de preaviso (12 horas).", None

        disponibles = self.obtener_horarios_disponibles(cita.medico, nueva_fecha)

        # permitir la misma hora si no cambió
        if not (nueva_fecha == cita.fecha and nueva_hora == cita.hora):
            if nueva_hora not in disponibles:
                return False, "El nuevo horario no está disponible.", None

        cita.fecha = nueva_fecha
        cita.hora = nueva_hora
        cita.estado = "Reprogramada"
        cita.actualizada_en = datetime.now()

        self._notificar(destinatario=cita.cc_paciente, canal="interno",
                        mensaje=f"Su cita {cita.codigo} fue reprogramada para {cita.fecha.isoformat()} {cita.hora.strftime('%H:%M')} con {cita.medico}.")
        self._notificar(destinatario=cita.medico, canal="interno",
                        mensaje=f"Cita reprogramada: {cita.codigo} - {cita.nombre_paciente} ({cita.fecha.isoformat()} {cita.hora.strftime('%H:%M')}).")

        return True, "Cita modificada correctamente.", cita

    def cancelar_cita(self, codigo: str) -> Tuple[bool, str]:
        cita = self.consultar_cita_por_codigo(codigo)
        if not cita:
            return False, "No se encontró la cita."

        if cita.estado == "Cancelada":
            return False, "La cita ya está cancelada."

        if datetime.now() > (cita.fecha_hora() - timedelta(hours=12)):
            return False, "No se puede cancelar la cita por política de preaviso (12 horas)."

        cita.estado = "Cancelada"
        cita.actualizada_en = datetime.now()

        self._notificar(destinatario=cita.cc_paciente, canal="interno",
                        mensaje=f"Su cita {cita.codigo} ha sido cancelada.")
        self._notificar(destinatario=cita.medico, canal="interno",
                        mensaje=f"La cita {cita.codigo} ha sido cancelada.")

        return True, "Cita cancelada correctamente."

    # ---------------------------
    # Recepción: registrar estado
    # ---------------------------
    def registrar_estado_cita(
        self,
        codigo: str,
        nuevo_estado: str,
        hora_llegada: Optional[time] = None,
        comentario: str = ""
    ) -> Tuple[bool, str, Optional[CitaMedica]]:
        cita = self.consultar_cita_por_codigo(codigo)
        if not cita:
            return False, "No se encontró la cita.", None

        if cita.estado == "Cancelada":
            return False, "No se puede actualizar una cita cancelada.", None

        estados_validos = {"Asistió", "Ausente", "Tardanza"}
        if nuevo_estado not in estados_validos:
            return False, "Estado inválido.", None

        cita.estado = nuevo_estado
        cita.hora_llegada = hora_llegada
        cita.comentario = comentario
        cita.actualizada_en = datetime.now()

        self._notificar(destinatario=cita.medico, canal="interno",
                        mensaje=f"Actualización recepción: {cita.nombre_paciente} - {cita.codigo} Estado: {nuevo_estado}.")

        return True, f"Estado de la cita actualizado: {nuevo_estado}.", cita

    # ---------------------------
    # Notificaciones
    # ---------------------------
    def obtener_historial_notificaciones(self) -> List[Notificacion]:
        return list(self._notificaciones)

    def _notificar(self, destinatario: str, canal: str, mensaje: str,
                   estado: str = "Enviada", detalle_error: str = ""):
        self._notificaciones.append(Notificacion(
            destinatario=destinatario,
            canal=canal,
            mensaje=mensaje,
            estado=estado,
            detalle_error=detalle_error
        ))

    def _notificar_cita_programada(self, cita: CitaMedica):
        paciente = self.pacientes.consultar_paciente(cita.cc_paciente)

        canal = "interno"
        if paciente:
            if getattr(paciente, "email", None):
                canal = "email"
            elif getattr(paciente, "telefono", None):
                canal = "sms"

        msg_paciente = (
            f"Cita programada: {cita.especialidad} con {cita.medico} "
            f"el {cita.fecha.isoformat()} a las {cita.hora.strftime('%H:%M')} "
            f"(Consultorio {cita.consultorio}). Código: {cita.codigo}."
        )
        msg_medico = (
            f"Nueva cita: {cita.nombre_paciente} - {cita.especialidad} "
            f"{cita.fecha.isoformat()} {cita.hora.strftime('%H:%M')} (Código {cita.codigo})."
        )

        self._notificar(destinatario=cita.cc_paciente, canal=canal, mensaje=msg_paciente)
        self._notificar(destinatario=cita.medico, canal="interno", mensaje=msg_medico)
