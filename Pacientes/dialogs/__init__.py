"""
Módulo de Gestión de Pacientes
Implementa todos los casos de uso del diagrama UML para el manejo de pacientes.
"""

from .paciente import Paciente
from .paciente_controller import PacienteController
from .paciente_view import PacienteView
from .registrar_paciente_dialog import RegistrarPacienteDialog
from .actualizar_datos_dialog import ActualizarDatosDialog
from .consultar_paciente_dialog import ConsultarPacienteDialog

__all__ = [
    'Paciente',
    'PacienteController',
    'PacienteView',
    'RegistrarPacienteDialog',
    'ActualizarDatosDialog',
    'ConsultarPacienteDialog'
]

__version__ = '1.0.0'
__author__ = 'Tu Nombre'