from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt
from ..paciente_controller import PacienteController


class SubmenuActualizarDialog(QDialog):
    """
    Diálogo para buscar paciente antes de actualizar sus datos.
    """

    def __init__(self, controller: PacienteController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.paciente = None
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Actualizar Datos del Paciente")
        self.setModal(True)
        self.setMinimumSize(450, 280)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        # Título
        lbl_titulo = QLabel("Actualizar Datos del Paciente")
        lbl_titulo.setObjectName("titulo")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)

        # Sección de búsqueda de paciente
        group_buscar = QGroupBox("Buscar Paciente")
        buscar_layout = QVBoxLayout()
        buscar_layout.setSpacing(10)
        buscar_layout.setContentsMargins(10, 25, 10, 10)

        # Fila de cédula
        cedula_layout = QHBoxLayout()
        lbl_cedula = QLabel("Cédula:")
        lbl_cedula.setMinimumWidth(80)
        self.txt_cc = QLineEdit()
        self.txt_cc.setPlaceholderText("Ingrese la cédula del paciente")
        self.txt_cc.setMinimumHeight(35)
        self.txt_cc.returnPressed.connect(self.buscar_paciente)
        cedula_layout.addWidget(lbl_cedula)
        cedula_layout.addWidget(self.txt_cc)
        buscar_layout.addLayout(cedula_layout)

        # Botón buscar
        btn_buscar = QPushButton("Buscar Paciente")
        btn_buscar.clicked.connect(self.buscar_paciente)
        btn_buscar.setMinimumHeight(40)
        buscar_layout.addWidget(btn_buscar)

        group_buscar.setLayout(buscar_layout)
        layout.addWidget(group_buscar)

        layout.addStretch()

        # Botón cerrar
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("btn_cancelar")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

    def buscar_paciente(self):
        """Busca el paciente por cédula y abre la ventana de opciones."""
        cc = self.txt_cc.text().strip()
        if not cc:
            QMessageBox.warning(self, "Advertencia", "Ingrese una cédula para buscar")
            return

        self.paciente = self.controller.consultar_paciente(cc)

        if self.paciente:
            # Abrir la nueva ventana con los botones de actualización
            ventana_opciones = VentanaOpcionesActualizar(self.controller, self.paciente, self)
            ventana_opciones.exec()
            # Limpiar el campo de cédula después de cerrar
            self.txt_cc.clear()
        else:
            QMessageBox.warning(self, "No encontrado",
                              f"No se encontró un paciente con cédula {cc}")


class VentanaOpcionesActualizar(QDialog):
    """
    Ventana que muestra las opciones de actualización para un paciente.
    """

    def __init__(self, controller: PacienteController, paciente, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.paciente = paciente
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Opciones de Actualización")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        # Información del paciente en la parte superior
        self.lbl_info_paciente = QLabel(
            f"Paciente: {self.paciente.nombre} {self.paciente.apellido}\nCC: {self.paciente.cc}"
        )
        self.lbl_info_paciente.setObjectName("info_paciente")
        self.lbl_info_paciente.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_info_paciente)

        # Contenedor de botones de actualización
        group_opciones = QGroupBox("Seleccione qué desea actualizar")
        opciones_layout = QGridLayout()
        opciones_layout.setSpacing(15)
        opciones_layout.setContentsMargins(15, 25, 15, 15)

        # Botones de actualización
        btn_direccion = QPushButton("Actualizar Dirección")
        btn_direccion.setProperty("class", "menu_btn")
        btn_direccion.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_direccion.clicked.connect(lambda: self.abrir_actualizar("direccion"))
        opciones_layout.addWidget(btn_direccion, 0, 0)

        btn_telefono = QPushButton("Actualizar Teléfono")
        btn_telefono.setProperty("class", "menu_btn")
        btn_telefono.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_telefono.clicked.connect(lambda: self.abrir_actualizar("telefono"))
        opciones_layout.addWidget(btn_telefono, 0, 1)

        btn_email = QPushButton("Actualizar E-mail")
        btn_email.setProperty("class", "menu_btn")
        btn_email.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_email.clicked.connect(lambda: self.abrir_actualizar("email"))
        opciones_layout.addWidget(btn_email, 1, 0)

        btn_tel_ref = QPushButton("Actualizar Tel. Referencia")
        btn_tel_ref.setProperty("class", "menu_btn")
        btn_tel_ref.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_tel_ref.clicked.connect(lambda: self.abrir_actualizar("telefono_referencia"))
        opciones_layout.addWidget(btn_tel_ref, 1, 1)

        group_opciones.setLayout(opciones_layout)
        layout.addWidget(group_opciones)

        layout.addStretch()

        # Botón cerrar
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("btn_cancelar")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

    def abrir_actualizar(self, tipo_campo: str):
        """Abre el diálogo de actualización para el campo específico."""
        from .actualizar_datos_dialog import ActualizarDatosDialog
        # Pasar el paciente directamente para no tener que buscarlo de nuevo
        dialogo = ActualizarDatosDialog(self.controller, tipo_campo, self, paciente=self.paciente)
        dialogo.exec()

        # Refrescar los datos del paciente después de actualizar
        self.paciente = self.controller.consultar_paciente(self.paciente.cc)
        if self.paciente:
            self.lbl_info_paciente.setText(
                f"Paciente: {self.paciente.nombre} {self.paciente.apellido}\nCC: {self.paciente.cc}"
            )

