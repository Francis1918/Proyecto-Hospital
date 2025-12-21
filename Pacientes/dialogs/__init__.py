"""
Módulo de diálogos para la gestión de pacientes.
"""

from .registrar_paciente_dialog import RegistrarPacienteDialog
from .consultar_paciente_dialog import ConsultarPacienteDialog
from .actualizar_datos_dialog import ActualizarDatosDialog
from .registrar_anamnesis_dialog import RegistrarAnamnesisDilaog
from .historia_clinica_dialog import HistoriaClinicaDialog
from .submenu_actualizar_dialog import SubmenuActualizarDialog

__all__ = [
    'RegistrarPacienteDialog',
    'ConsultarPacienteDialog',
    'ActualizarDatosDialog',
    'RegistrarAnamnesisDilaog',
    'HistoriaClinicaDialog',
    'SubmenuActualizarDialog'
]

__version__ = '1.0.0'
__author__ = 'Tu Nombre'