"""
Módulo de diálogos para la gestión de pacientes.
"""

from .registrar_paciente_dialog import RegistrarPacienteDialog
from .consultar_paciente_dialog import ConsultarPacienteDialog
from .actualizar_datos_dialog import ActualizarDatosDialog
from .registrar_anamnesis_dialog import RegistrarAnamnesisDilaog

__all__ = [
    'RegistrarPacienteDialog',
    'ConsultarPacienteDialog',
    'ActualizarDatosDialog',
    'RegistrarAnamnesisDilaog'
]

__version__ = '1.0.0'
__author__ = 'Tu Nombre'