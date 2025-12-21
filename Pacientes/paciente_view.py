from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QLabel, QDialog,
    QFrame, QGridLayout
)
from PyQt6.QtCore import Qt
from .paciente_controller import PacienteController
from .paciente import Paciente


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
        """Abre la historia clínica del paciente."""
        QMessageBox.information(self, "Historia Clínica",
                                "Módulo de Historia Clínica.\n\nSeleccione un paciente para ver su historia.")

    def abrir_anamnesis(self):
        """Abre la anamnesis del paciente."""
        QMessageBox.information(self, "Registrar Anamnesis",
                                "Módulo de Anamnesis.\n\nFuncionalidad para registrar anamnesis del paciente.")


class RegistrarPacienteDialog(QDialog):
    """Diálogo para registrar un nuevo paciente."""

    def __init__(self, controller: PacienteController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Registrar Nuevo Paciente")
        self.setModal(True)
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.txt_cc = QLineEdit()
        form_layout.addRow("Cédula:", self.txt_cc)

        self.txt_num_unic = QLineEdit()
        form_layout.addRow("Número Único:", self.txt_num_unic)

        self.txt_nombre = QLineEdit()
        form_layout.addRow("Nombre:", self.txt_nombre)

        self.txt_apellido = QLineEdit()
        form_layout.addRow("Apellido:", self.txt_apellido)

        self.txt_direccion = QLineEdit()
        form_layout.addRow("Dirección:", self.txt_direccion)

        self.txt_telefono = QLineEdit()
        form_layout.addRow("Teléfono:", self.txt_telefono)

        self.txt_email = QLineEdit()
        form_layout.addRow("Email:", self.txt_email)

        self.txt_telefono_ref = QLineEdit()
        form_layout.addRow("Teléfono Referencia:", self.txt_telefono_ref)

        layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_paciente)
        buttons_layout.addWidget(btn_guardar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        buttons_layout.addWidget(btn_cancelar)

        layout.addLayout(buttons_layout)

    def guardar_paciente(self):
        """Guarda el nuevo paciente."""
        paciente = Paciente(
            cc=self.txt_cc.text().strip(),
            num_unic=self.txt_num_unic.text().strip(),
            nombre=self.txt_nombre.text().strip(),
            apellido=self.txt_apellido.text().strip(),
            direccion=self.txt_direccion.text().strip(),
            telefono=self.txt_telefono.text().strip(),
            email=self.txt_email.text().strip(),
            telefono_referencia=self.txt_telefono_ref.text().strip() or None
        )

        exito, mensaje = self.controller.registrar_paciente(paciente)

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", mensaje)


class ActualizarDatosDialog(QDialog):
    """Diálogo para actualizar datos del paciente."""

    def __init__(self, controller: PacienteController, cc_paciente: str, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.cc_paciente = cc_paciente
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Actualizar Datos del Paciente")
        self.setModal(True)
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.txt_direccion = QLineEdit()
        form_layout.addRow("Nueva Dirección:", self.txt_direccion)

        self.txt_telefono = QLineEdit()
        form_layout.addRow("Nuevo Teléfono:", self.txt_telefono)

        self.txt_email = QLineEdit()
        form_layout.addRow("Nuevo Email:", self.txt_email)

        self.txt_telefono_ref = QLineEdit()
        form_layout.addRow("Nuevo Tel. Referencia:", self.txt_telefono_ref)

        layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()

        btn_actualizar_dir = QPushButton("Actualizar Dirección")
        btn_actualizar_dir.clicked.connect(self.actualizar_direccion)
        buttons_layout.addWidget(btn_actualizar_dir)

        btn_actualizar_tel = QPushButton("Actualizar Teléfono")
        btn_actualizar_tel.clicked.connect(self.actualizar_telefono)
        buttons_layout.addWidget(btn_actualizar_tel)

        layout.addLayout(buttons_layout)

        buttons_layout2 = QHBoxLayout()

        btn_actualizar_email = QPushButton("Actualizar Email")
        btn_actualizar_email.clicked.connect(self.actualizar_email)
        buttons_layout2.addWidget(btn_actualizar_email)

        btn_actualizar_tel_ref = QPushButton("Actualizar Tel. Ref.")
        btn_actualizar_tel_ref.clicked.connect(self.actualizar_telefono_ref)
        buttons_layout2.addWidget(btn_actualizar_tel_ref)

        layout.addLayout(buttons_layout2)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

    def actualizar_direccion(self):
        """Actualiza la dirección del paciente."""
        nueva_direccion = self.txt_direccion.text().strip()
        if nueva_direccion:
            exito, mensaje = self.controller.actualizar_direccion(self.cc_paciente, nueva_direccion)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.txt_direccion.clear()
            else:
                QMessageBox.warning(self, "Error", mensaje)

    def actualizar_telefono(self):
        """Actualiza el teléfono del paciente."""
        nuevo_telefono = self.txt_telefono.text().strip()
        if nuevo_telefono:
            exito, mensaje = self.controller.actualizar_telefono(self.cc_paciente, nuevo_telefono)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.txt_telefono.clear()
            else:
                QMessageBox.warning(self, "Error", mensaje)

    def actualizar_email(self):
        """Actualiza el email del paciente."""
        nuevo_email = self.txt_email.text().strip()
        if nuevo_email:
            exito, mensaje = self.controller.actualizar_email(self.cc_paciente, nuevo_email)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.txt_email.clear()
            else:
                QMessageBox.warning(self, "Error", mensaje)

    def actualizar_telefono_ref(self):
        """Actualiza el teléfono de referencia del paciente."""
        nuevo_telefono_ref = self.txt_telefono_ref.text().strip()
        if nuevo_telefono_ref:
            exito, mensaje = self.controller.actualizar_telefono_referencia(self.cc_paciente, nuevo_telefono_ref)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.txt_telefono_ref.clear()
            else:
                QMessageBox.warning(self, "Error", mensaje)