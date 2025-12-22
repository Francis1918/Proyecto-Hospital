"""
Módulo de Citas Médicas.

Implementa casos de uso para:
- Solicitar/Agendar cita
- Consultar / Modificar / Cancelar cita
- Consultar agenda por médico y fecha
- Registrar estado de cita (recepción)
- Historial de notificaciones

Persistencia en memoria (temporal), consistente con el proyecto.
"""

from .citas_controller import CitasMedicasController
from .citas_view import CitasMedicasView

__all__ = ["CitasMedicasController", "CitasMedicasView"]
