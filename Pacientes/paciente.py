from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class Paciente:
    """
    Clase modelo que representa un Paciente según el diagrama de base de datos.
    """
    cc: str
    #num_unic: str
    nombre: str
    apellido: str
    direccion: str
    telefono: str
    email: str
    fecha_nacimiento: Optional[date] = None
    telefono_referencia: Optional[str] = None
    #id_fac: Optional[int] = None
    fecha_registro: Optional[datetime] = None

    def __post_init__(self):
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now()

    def validar_datos(self) -> tuple[bool, str]:
        """
        Valida los datos del paciente según reglas de negocio estrictas.
        Retorna: (es_valido, mensaje_error)
        """
        import re
        from datetime import date

        # 1. Validar Cédula 
        # (Solo dígitos y longitud entre 6 y 15)
        if not self.cc or not self.cc.isdigit() or not (6 <= len(self.cc) <= 15):
             return False, "La cédula debe contener solo números y tener entre 6 y 15 dígitos."

        # 2. Validar Nombres y Apellidos
        # (Solo letras y espacios, incluye tildes y ñ)
        patron_nombre = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$'
        
        if not self.nombre or len(self.nombre) < 2 or not re.match(patron_nombre, self.nombre):
            return False, "El nombre no es válido (mín. 2 letras, solo letras y espacios)."
        
        if not self.apellido or len(self.apellido) < 2 or not re.match(patron_nombre, self.apellido):
            return False, "El apellido no es válido (mín. 2 letras, solo letras y espacios)."

        # 3. Validar Dirección (longitud mínima 5)
        if not self.direccion or len(self.direccion) < 5:
            return False, "La dirección debe tener al menos 5 caracteres."

        # 4. Validar Teléfonos (longitud 7-15)
        if not self.telefono or not (7 <= len(self.telefono) <= 15):
            return False, "El teléfono principal debe tener entre 7 y 15 caracteres."

        if self.telefono_referencia and not (7 <= len(self.telefono_referencia) <= 15):
            return False, "El teléfono de referencia debe tener entre 7 y 15 caracteres."

        # 5. Validar Email (RFC Standard-ish)
        if self.email:
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_email, self.email):
                 return False, "El formato del correo electrónico no es válido."

        # 6. Validar Fechas (Nacimiento)
        if self.fecha_nacimiento:
            hoy = date.today()
            
            # No permitir fechas futuras
            if self.fecha_nacimiento >= hoy:
                return False, "La fecha de nacimiento no puede ser hoy ni futura."
            
            # Calcular edad
            edad = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            
            if edad > 150:
                 return False, f"La edad ({edad} años) no es válida (máximo 150)."
            # (Opcional) Validar edad mínima si fuera necesario, pero 0 es válido para recién nacidos.

        return True, ""

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para la base de datos."""
        return {
            'cc': self.cc,
            #'num_unic': self.num_unic,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'fecha_nacimiento': self.fecha_nacimiento,
            'telefono_referencia': self.telefono_referencia,
            #'id_fac': self.id_fac,
            'fecha_registro': self.fecha_registro
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Paciente':
        """Crea un objeto Paciente desde un diccionario."""
        return cls(**data)