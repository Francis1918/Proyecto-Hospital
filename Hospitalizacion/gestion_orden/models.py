from dataclasses import dataclass
from datetime import datetime

@dataclass
class OrdenMedica:
    id_orden: str
    id_paciente: str
    descripcion: str
    fecha: datetime
    medico: str
