from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Habitacion:
    numero: str
    estado: str = "disponible"  # disponible | ocupada | mantenimiento
    ubicacion: str = "Planta Baja"  # Planta Baja | Piso 1 | Piso 2 | ...

@dataclass
class Cama:
    id_cama: str
    num_habitacion: str
    estado: str = "disponible"  # disponible | ocupada | reservada | mantenimiento
    higiene_ok: bool = True

@dataclass
class Sala:
    nombre: str
    activa: bool = True
    ubicacion: str = "Planta Baja"

@dataclass
class Infraestructura:
    nombre: str
    tipo: str  # sala | habitacion | cama
    capacidad: int
    ubicacion: str

@dataclass
class Paciente:
    id_paciente: str
    nombre: str
    estado: str = "en_observacion"  # hospitalizado | alta | en_observacion | pedido_registrado
    cama_asignada: Optional[str] = None

@dataclass
class PedidoHospitalizacion:
    id_paciente: str
    motivo: str
    estado: str = "pendiente"  # pendiente | autorizado | rechazado

@dataclass
class Historial:
    eventos: List[str] = field(default_factory=list)
    def registrar(self, evento: str):
        self.eventos.append(evento)
