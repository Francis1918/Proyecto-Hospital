from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional


@dataclass
class CitaMedica:
    codigo: str
    cc_paciente: str
    nombre_paciente: str
    especialidad: str
    medico: str
    fecha: date
    hora: time
    consultorio: str = ""
    estado: str = "Confirmada"  # Confirmada | Cancelada | Reprogramada | Asistió | Ausente | Tardanza
    creada_en: datetime = field(default_factory=datetime.now)
    actualizada_en: datetime = field(default_factory=datetime.now)
    comentario: str = ""
    hora_llegada: Optional[time] = None
    id_medico: int = 0

    def fecha_hora(self) -> datetime:
        return datetime.combine(self.fecha, self.hora)


@dataclass
class Notificacion:
    destinatario: str  # cc_paciente o medico
    canal: str         # email | sms | app | interno
    mensaje: str
    enviada_en: datetime = field(default_factory=datetime.now)
    estado: str = "Enviada"     # Enviada | Fallida
    detalle_error: str = ""
