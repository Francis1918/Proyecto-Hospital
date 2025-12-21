from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QLabel,
    QFrame, QGridLayout
)
from PyQt6.QtCore import Qt
from .paciente_controller import PacienteController


class PacienteView(QMainWindow):
    """
    Vista principal del módulo Paciente con PyQt6.
    Implementa la interfaz gráfica para todos los casos de uso.
    """

    def __init__(self, controller: PacienteController = None):
        super().__init__()
        self.controller = controller or PacienteController()
        self.init_ui()

    def get_styles(self):
        """Retorna los estilos CSS para la vista de pacientes."""
        return """
            QMainWindow {
                background-color: #e8f4fc;
            }
            QWidget#central {
                background-color: #e8f4fc;
            }
            QLabel#titulo {
                color: #1a365d;
                font-size: 32px;
                font-weight: bold;
                padding: 20px;
            }
            QFrame#menu_container {
                background-color: #e8f4fc;
                padding: 20px;
            }
            QPushButton.menu_btn {
                background-color: #3182ce;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
                min-height: 70px;
                min-width: 200px;
            }
            QPushButton.menu_btn:hover {
                background-color: #2c5282;
            }
            QPushButton.menu_btn:pressed {
                background-color: #1a365d;
            }
            QPushButton#btn_salir {
                background-color: #3182ce;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
                min-height: 70px;
                min-width: 200px;
            }
            QPushButton#btn_salir:hover {
                background-color: #2c5282;
            }
            QPushButton#btn_salir:pressed {
                background-color: #1a365d;
            }
        """

    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle("Sistema de Gestión Clínica - Pacientes")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(self.get_styles())

        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 20, 40, 20)

        # Título
        titulo = QLabel("Sistema de Gestión Clínica")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(titulo)

        # Contenedor del menú de botones
        menu_container = self.crear_menu_botones()
        main_layout.addWidget(menu_container)

        main_layout.addStretch()

    def crear_menu_botones(self):
        """Crea el contenedor con los botones del menú estilo tarjeta."""
        container = QFrame()
        container.setObjectName("menu_container")

        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        # Definir los botones del menú de pacientes
        botones = [
            ("Registrar Paciente", self.abrir_dialogo_registrar),
            ("Consultar Paciente", self.abrir_dialogo_consultar),
            ("Historia Clínica", self.abrir_historia_clinica),
            ("Registrar Anamnesis", self.abrir_anamnesis),
            ("Actualizar Dirección", self.abrir_actualizar_direccion),
            ("Actualizar Teléfono", self.abrir_actualizar_telefono),
            ("Actualizar E-mail", self.abrir_actualizar_email),
            ("Salir", self.close),
        ]

        # Crear botones en una cuadrícula 4x2
        for i, (texto, funcion) in enumerate(botones):
            btn = QPushButton(texto)
            if texto == "Salir":
                btn.setObjectName("btn_salir")
            else:
                btn.setProperty("class", "menu_btn")
            btn.clicked.connect(funcion)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            row = i // 2
            col = i % 2
            grid_layout.addWidget(btn, row, col)

        return container

    def abrir_dialogo_consultar(self):
        """Abre el diálogo para consultar un paciente."""
        from .dialogs import ConsultarPacienteDialog
        dialogo = ConsultarPacienteDialog(self.controller, None, self)
        dialogo.exec()

    def abrir_actualizar_direccion(self):
        """Abre el diálogo para actualizar dirección."""
        from .dialogs import ActualizarDatosDialog
        dialogo = ActualizarDatosDialog(self.controller, "direccion", self)
        dialogo.exec()

    def abrir_actualizar_telefono(self):
        """Abre el diálogo para actualizar teléfono."""
        from .dialogs import ActualizarDatosDialog
        dialogo = ActualizarDatosDialog(self.controller, "telefono", self)
        dialogo.exec()

    def abrir_actualizar_email(self):
        """Abre el diálogo para actualizar email."""
        from .dialogs import ActualizarDatosDialog
        dialogo = ActualizarDatosDialog(self.controller, "email", self)
        dialogo.exec()

    def abrir_dialogo_registrar(self):
        """Abre el diálogo para registrar un nuevo paciente."""
        from .dialogs import RegistrarPacienteDialog
        dialogo = RegistrarPacienteDialog(self.controller, self)
        dialogo.exec()

    def abrir_historia_clinica(self):
        """Abre el diálogo de historia clínica del paciente."""
        from .dialogs import HistoriaClinicaDialog
        dialogo = HistoriaClinicaDialog(self.controller, self)
        dialogo.exec()

    def abrir_anamnesis(self):
        """Abre el diálogo para registrar anamnesis del paciente."""
        from .dialogs import RegistrarAnamnesisDilaog
        dialogo = RegistrarAnamnesisDilaog(self.controller, self)
        dialogo.exec()
