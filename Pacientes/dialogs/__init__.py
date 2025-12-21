"""
Módulo de Diálogos para Gestión de Pacientes
"""

from .registrar_paciente_dialog import RegistrarPacienteDialog
from .actualizar_datos_dialog import ActualizarDatosDialog
from .consultar_paciente_dialog import ConsultarPacienteDialog

__all__ = [
    'RegistrarPacienteDialog',
    'ActualizarDatosDialog',
    'ConsultarPacienteDialog'
]

__version__ = '1.0.0'
__author__ = 'Tu Nombre'