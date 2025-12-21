from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
from ..paciente_controller import PacienteController


class ActualizarDatosDialog(QDialog):
    """
    Diálogo para actualizar datos del paciente.
    Implementa los casos de uso:
    - actualizarDirección
    - actualizarTeléfono
    - actualizarE-mail
    - actualizarTeléfonoDeReferencia
    """

    datos_actualizados = pyqtSignal(str)

    def __init__(self, controller: PacienteController, tipo_campo: str = None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.tipo_campo = tipo_campo  # "direccion", "telefono", "email" o None para todos
        self.cc_paciente = None
        self.paciente = None
        self.init_ui()

    def get_styles(self):
        """Retorna los estilos CSS para el diálogo."""
        return """
            QDialog {
                background-color: #e8f4fc;
            }
            QLabel#titulo {
                color: #1a365d;
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
            }
            QFrame#container {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #3182ce;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2c5282;
            }
            QPushButton {
                background-color: #3182ce;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2c5282;
            }
            QPushButton:pressed {
                background-color: #1a365d;
            }
            QPushButton#btn_cancelar {
                background-color: #718096;
            }
            QPushButton#btn_cancelar:hover {
                background-color: #4a5568;
            }
            QLabel {
                color: #2d3748;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3182ce;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                color: #1a365d;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        titulos = {
            "direccion": "Actualizar Dirección",
            "telefono": "Actualizar Teléfono",
            "email": "Actualizar E-mail"
        }
        titulo = titulos.get(self.tipo_campo, "Actualizar Datos del Paciente")

        self.setWindowTitle(titulo)
        self.setModal(True)
        self.setMinimumSize(500, 400)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        # Título
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("titulo")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)

        # Contenedor principal
        container = QFrame()
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(15)

        # Sección de búsqueda de paciente
        group_buscar = QGroupBox("Buscar Paciente")
        form_buscar = QFormLayout()

        self.txt_cc = QLineEdit()
        self.txt_cc.setPlaceholderText("Ingrese la cédula del paciente")
        form_buscar.addRow("Cédula:", self.txt_cc)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_paciente)
        form_buscar.addRow("", btn_buscar)

        group_buscar.setLayout(form_buscar)
        container_layout.addWidget(group_buscar)

        # Sección de datos del paciente (oculta inicialmente)
        self.group_datos = QGroupBox("Datos del Paciente")
        self.form_datos = QFormLayout()

        self.lbl_nombre = QLabel("-")
        self.form_datos.addRow("Nombre:", self.lbl_nombre)

        self.lbl_dato_actual = QLabel("-")
        label_actual = {
            "direccion": "Dirección actual:",
            "telefono": "Teléfono actual:",
            "email": "Email actual:"
        }.get(self.tipo_campo, "Dato actual:")
        self.form_datos.addRow(label_actual, self.lbl_dato_actual)

        # Campo para nuevo valor
        self.txt_nuevo_valor = QLineEdit()
        placeholder = {
            "direccion": "Ingrese la nueva dirección",
            "telefono": "Ingrese el nuevo teléfono",
            "email": "Ingrese el nuevo email"
        }.get(self.tipo_campo, "Ingrese el nuevo valor")
        self.txt_nuevo_valor.setPlaceholderText(placeholder)

        label_nuevo = {
            "direccion": "Nueva dirección:",
            "telefono": "Nuevo teléfono:",
            "email": "Nuevo email:"
        }.get(self.tipo_campo, "Nuevo valor:")
        self.form_datos.addRow(label_nuevo, self.txt_nuevo_valor)

        self.group_datos.setLayout(self.form_datos)
        self.group_datos.setVisible(False)
        container_layout.addWidget(self.group_datos)

        layout.addWidget(container)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.actualizar_dato)
        self.btn_actualizar.setEnabled(False)
        buttons_layout.addWidget(self.btn_actualizar)

        btn_cancelar = QPushButton("Cerrar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cancelar)

        layout.addLayout(buttons_layout)

    def buscar_paciente(self):
        """Busca el paciente por cédula."""
        cc = self.txt_cc.text().strip()
        if not cc:
            QMessageBox.warning(self, "Advertencia", "Ingrese una cédula para buscar")
            return

        self.paciente = self.controller.consultar_paciente(cc)

        if self.paciente:
            self.cc_paciente = cc
            self.lbl_nombre.setText(f"{self.paciente.nombre} {self.paciente.apellido}")

            # Mostrar el dato actual según el tipo
            dato_actual = {
                "direccion": self.paciente.direccion,
                "telefono": self.paciente.telefono,
                "email": self.paciente.email
            }.get(self.tipo_campo, "-")
            self.lbl_dato_actual.setText(dato_actual or "No registrado")

            self.group_datos.setVisible(True)
            self.btn_actualizar.setEnabled(True)
        else:
            QMessageBox.warning(self, "No encontrado",
                              f"No se encontró un paciente con cédula {cc}")
            self.group_datos.setVisible(False)
            self.btn_actualizar.setEnabled(False)

    def actualizar_dato(self):
        """Actualiza el dato según el tipo de campo."""
        nuevo_valor = self.txt_nuevo_valor.text().strip()

        if not nuevo_valor:
            QMessageBox.warning(self, "Advertencia", "Ingrese un valor válido")
            return

        if not self.cc_paciente:
            QMessageBox.warning(self, "Advertencia", "Primero busque un paciente")
            return

        # Ejecutar la actualización según el tipo
        if self.tipo_campo == "direccion":
            exito, mensaje = self.controller.actualizar_direccion(self.cc_paciente, nuevo_valor)
        elif self.tipo_campo == "telefono":
            exito, mensaje = self.controller.actualizar_telefono(self.cc_paciente, nuevo_valor)
        elif self.tipo_campo == "email":
            exito, mensaje = self.controller.actualizar_email(self.cc_paciente, nuevo_valor)
        else:
            exito, mensaje = False, "Tipo de campo no válido"

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.lbl_dato_actual.setText(nuevo_valor)
            self.txt_nuevo_valor.clear()
            self.datos_actualizados.emit(self.cc_paciente)
        else:
            QMessageBox.warning(self, "Error", mensaje)
