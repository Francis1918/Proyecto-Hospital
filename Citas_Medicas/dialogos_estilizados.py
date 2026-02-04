"""
Diálogos estilizados para el módulo de Citas Médicas.
Proporciona mensajes de error, advertencia e información con estilo UI consistente.
"""

from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from core.theme import get_sheet, AppPalette, STYLES
from core.utils import get_icon


class DialogoEstilizado(QMessageBox):
    """Diálogo base con estilo consistente con la aplicación."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(get_sheet())
        fuente = self.font()
        fuente.setPointSize(10)
        self.setFont(fuente)
        
        try:
            icon = get_icon("info.svg")
            if not icon.isNull(): self.setWindowIcon(icon)
        except: pass


class DialogoError(DialogoEstilizado):
    """Diálogo de error con icono y colores de error."""
    
    def __init__(self, titulo: str, mensaje: str, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(titulo)
        self.setText(mensaje)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)

    @staticmethod
    def mostrar_lista(titulo: str, errores: list, parent=None):
        """Método estático limpio para mostrar errores sin duplicados."""
        if not errores: return
        mensaje = "Se encontraron los siguientes errores:\n\n"
        for error in errores:
            mensaje += f"• {str(error).strip()}\n"
        
        dlg = DialogoError(titulo, mensaje, parent)
        return dlg.exec()


class DialogoAdvertencia(DialogoEstilizado):
    """Diálogo de advertencia con icono de precaución."""
    
    def __init__(self, titulo: str, mensaje: str, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowTitle(titulo)
        self.setText(mensaje)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)


class DialogoInfo(DialogoEstilizado):
    """Diálogo de información."""
    
    def __init__(self, titulo: str, mensaje: str, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle(titulo)
        self.setText(mensaje)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)


class DialogoConfirmacion(DialogoEstilizado):
    """Diálogo de confirmación con opciones Sí/No."""
    
    def __init__(self, titulo: str, mensaje: str, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle(titulo)
        self.setText(mensaje)
        self.setStandardButtons(
            QMessageBox.StandardButton.Yes | 
            QMessageBox.StandardButton.No
        )
        self.setDefaultButton(QMessageBox.StandardButton.No)


class DialogoExito(DialogoEstilizado):
    """Diálogo de éxito con icono de verificación."""
    
    def __init__(self, titulo: str, mensaje: str, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle(titulo)
        self.setText(mensaje)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        # Cambiar color del ícono a verde
        self.setStyleSheet(get_sheet())


# ========================================================
# FUNCIONES AUXILIARES PARA MENSAJES COMUNES
# ========================================================

def mostrar_error_cedula_invalida(cc: str, razon: str, parent=None) -> None:
    """
    Muestra error cuando la cédula es inválida.
    
    :param cc: Cédula ingresada
    :param razon: Razón por la que es inválida
    :param parent: Widget padre
    """
    dlg = DialogoError(
        "❌ Cédula Inválida",
        f"La cédula '{cc}' no es válida:\n\n{razon}",
        parent
    )
    dlg.exec()


def mostrar_error_paciente_no_encontrado(cc: str, parent=None) -> int:
    """
    Muestra error cuando el paciente no existe en el sistema.
    Pregunta si desea registrarlo.
    
    :param cc: Cédula del paciente
    :param parent: Widget padre
    :return: QMessageBox.Yes o QMessageBox.No
    """
    dlg = DialogoConfirmacion(
        "👤 Paciente No Registrado",
        f"La cédula {cc} no existe en el sistema.\n\n"
        "¿Desea registrar al paciente ahora?",
        parent
    )
    return dlg.exec()


def mostrar_error_sin_horarios(especialidad: str, medico: str, fecha: str, parent=None) -> None:
    """
    Muestra error cuando no hay horarios disponibles.
    
    :param especialidad: Especialidad
    :param medico: Nombre del médico
    :param fecha: Fecha solicitada
    :param parent: Widget padre
    """
    dlg = DialogoAdvertencia(
        "⏰ Sin Horarios Disponibles",
        f"No hay horarios disponibles para:\n\n"
        f"• Especialidad: {especialidad}\n"
        f"• Médico: {medico}\n"
        f"• Fecha: {fecha}\n\n"
        "Intente con otro médico o fecha.",
        parent
    )
    dlg.exec()


def mostrar_error_horario_ocupado(hora: str, medico: str, parent=None) -> None:
    """
    Muestra error cuando el horario está ocupado.
    
    :param hora: Hora solicitada
    :param medico: Nombre del médico
    :param parent: Widget padre
    """
    dlg = DialogoAdvertencia(
        "⏰ Horario Ocupado",
        f"El horario {hora} ya fue ocupado por {medico}.\n\n"
        "Seleccione otro horario disponible.",
        parent
    )
    dlg.exec()


def mostrar_error_fecha_invalida(razon: str, parent=None) -> None:
    """
    Muestra error cuando la fecha es inválida.
    
    :param razon: Razón por la que es inválida
    :param parent: Widget padre
    """
    dlg = DialogoError(
        "📅 Fecha Inválida",
        f"La fecha ingresada no es válida:\n\n{razon}",
        parent
    )
    dlg.exec()


def mostrar_exito_cita_registrada(codigo: str, paciente: str, medico: str, fecha: str, hora: str, parent=None) -> None:
    """
    Muestra confirmación de cita registrada exitosamente.
    
    :param codigo: Código de la cita
    :param paciente: Nombre del paciente
    :param medico: Nombre del médico
    :param fecha: Fecha de la cita
    :param hora: Hora de la cita
    :param parent: Widget padre
    """
    mensaje = (
        f"✅ ¡CITA AGENDADA EXITOSAMENTE!\n"
        f"{'═' * 30}\n\n"
        f"📋 Código: {codigo}\n"
        f"👤 Paciente: {paciente}\n"
        f"👨‍⚕️ Médico: {medico}\n"
        f"📅 Fecha: {fecha}\n"
        f"⏰ Hora: {hora}\n\n"
        f"{'═' * 30}\n"
        "Se ha enviado una notificación al paciente y médico."
    )
    dlg = DialogoExito("¡Éxito!", mensaje, parent)
    dlg.exec()


def mostrar_exito_cita_modificada(codigo: str, nueva_fecha: str, nueva_hora: str, parent=None) -> None:
    """
    Muestra confirmación de cita modificada exitosamente.
    
    :param codigo: Código de la cita
    :param nueva_fecha: Nueva fecha
    :param nueva_hora: Nueva hora
    :param parent: Widget padre
    """
    mensaje = (
        f"✅ ¡CITA MODIFICADA EXITOSAMENTE!\n"
        f"{'═' * 30}\n\n"
        f"📋 Código: {codigo}\n"
        f"📅 Nueva Fecha: {nueva_fecha}\n"
        f"⏰ Nueva Hora: {nueva_hora}\n"
    )
    dlg = QMessageBox(parent)
    dlg.setStyleSheet(get_sheet())
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.setWindowTitle("¡Actualizado!")
    dlg.setText(mensaje)
    dlg.exec()


def mostrar_exito_cita_cancelada(codigo: str, paciente: str, parent=None) -> None:
    """
    Muestra confirmación de cita cancelada.
    
    :param codigo: Código de la cita
    :param paciente: Nombre del paciente
    :param parent: Widget padre
    """
    mensaje = (
        f"✅ ¡CITA CANCELADA!\n"
        f"{'═' * 30}\n\n"
        f"📋 Código: {codigo}\n"
        f"👤 Paciente: {paciente}\n\n"
        f"{'═' * 30}\n"
        "Se ha notificado la cancelación al paciente."
    )
    dlg = DialogoExito("¡Cancelada!", mensaje, parent)
    dlg.exec()


def mostrar_confirmacion_eliminar_cita(codigo: str, paciente: str, fecha: str, hora: str, parent=None) -> int:
    """
    Solicita confirmación antes de eliminar una cita.
    
    :param codigo: Código de la cita
    :param paciente: Nombre del paciente
    :param fecha: Fecha de la cita
    :param hora: Hora de la cita
    :param parent: Widget padre
    :return: QMessageBox.Yes o QMessageBox.No
    """
    mensaje = (
        "⚠️ ¿Está seguro de que desea CANCELAR esta cita?\n\n"
        f"📋 Código: {codigo}\n"
        f"👤 Paciente: {paciente}\n"
        f"📅 Fecha: {fecha}\n"
        f"⏰ Hora: {hora}\n\n"
        "Esta acción no se puede deshacer."
    )
    dlg = DialogoConfirmacion("Cancelar Cita", mensaje, parent)
    return dlg.exec()


def mostrar_confirmacion_modificar_cita(codigo: str, paciente: str, nueva_fecha: str, nueva_hora: str, parent=None) -> int:
    """
    Solicita confirmación antes de modificar una cita.
    
    :param codigo: Código de la cita
    :param paciente: Nombre del paciente
    :param nueva_fecha: Nueva fecha
    :param nueva_hora: Nueva hora
    :param parent: Widget padre
    :return: QMessageBox.Yes o QMessageBox.No
    """
    mensaje = (
        "✏️ ¿Está seguro de que desea MODIFICAR esta cita?\n\n"
        f"📋 Código: {codigo}\n"
        f"👤 Paciente: {paciente}\n"
        f"📅 Nueva Fecha: {nueva_fecha}\n"
        f"⏰ Nueva Hora: {nueva_hora}\n\n"
        "Se notificará al paciente los cambios."
    )
    dlg = DialogoConfirmacion("Modificar Cita", mensaje, parent)
    return dlg.exec()


def mostrar_error_lista_validacion(titulo: str, errores: list, parent=None) -> None:
    """
    Muestra una lista de errores de validación formateados.
    
    :param titulo: Título del diálogo
    :param errores: Lista de mensajes de error
    :param parent: Widget padre
    """
    if not errores: return
    mensaje = "Se encontraron los siguientes errores:\n\n"
    for error in errores:
        mensaje += f"❌ {str(error).strip()}\n"
    
    # Creamos una instancia limpia y la ejecutamos una sola vez
    dlg = DialogoError(titulo, mensaje, parent)
    dlg.exec()


def mostrar_error_codigo_no_encontrado(codigo: str, parent=None) -> None:
    """
    Muestra error cuando el código de cita no se encuentra.
    
    :param codigo: Código buscado
    :param parent: Widget padre
    """
    dlg = DialogoError(
        "❌ Cita No Encontrada",
        f"No se encontró ninguna cita con el código: {codigo}\n\n"
        "Verifique que el código sea correcto.",
        parent
    )
    dlg.exec()


def mostrar_error_fecha_invalida_dialog(razon: str, parent=None) -> None:
    """
    Muestra error cuando la fecha es inválida.
    
    :param razon: Razón por la que es inválida
    :param parent: Widget padre
    """
    dlg = DialogoError(
        "📅 Fecha Inválida",
        f"La fecha ingresada no es válida:\n\n{razon}",
        parent
    )
    dlg.exec()
