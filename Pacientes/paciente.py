from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Paciente:
    """
    Clase modelo que representa un Paciente según el diagrama de base de datos.
    """
    cc: str
    num_unic: str
    nombre: str
    apellido: str
    direccion: str
    telefono: str
    email: str
    telefono_referencia: Optional[str] = None
    id_fac: Optional[int] = None
    fecha_registro: Optional[datetime] = None

    def __post_init__(self):
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now()

    def validar_datos(self) -> tuple[bool, str]:
        """
        Valida los datos del paciente.
        Retorna: (es_valido, mensaje_error)
        """
        if not self.cc or len(self.cc) < 6:
            return False, "La cédula debe tener al menos 6 caracteres"

        if not self.num_unic:
            return False, "El número único es requerido"

        if not self.nombre or not self.apellido:
            return False, "Nombre y apellido son requeridos"

        if not self.telefono or len(self.telefono) < 7:
            return False, "El teléfono debe tener al menos 7 dígitos"

        if self.email and '@' not in self.email:
            return False, "El email no es válido"

        return True, ""

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para la base de datos."""
        return {
            'cc': self.cc,
            'num_unic': self.num_unic,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'telefono_referencia': self.telefono_referencia,
            'id_fac': self.id_fac,
            'fecha_registro': self.fecha_registro
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Paciente':
        """Crea un objeto Paciente desde un diccionario."""
        return cls(**data)