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

    def __init__(self, controller: PacienteController, tipo_campo: str = "", parent=None, paciente=None):
        super().__init__(parent)
        self.controller = controller
        self.tipo_campo = tipo_campo  # "direccion", "telefono", "email" o None para todos
        self.cc_paciente = paciente.cc if paciente else None
        self.paciente = paciente
        self.paciente_precargado = paciente is not None  # Indica si viene del submenú
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        titulos = {
            "direccion": "Actualizar Dirección",
            "telefono": "Actualizar Teléfono",
            "email": "Actualizar E-mail",
            "telefono_referencia": "Actualizar Teléfono de Referencia"
        }
        titulo = titulos.get(self.tipo_campo, "Actualizar Datos del Paciente")

        self.setWindowTitle(titulo)
        self.setModal(True)
        self.setMinimumSize(500, 450 if self.paciente_precargado else 600)
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

        # Sección de búsqueda de paciente (oculta si viene precargado)
        self.group_buscar = QGroupBox("Buscar Paciente")
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
        cedula_layout.addWidget(lbl_cedula)
        cedula_layout.addWidget(self.txt_cc)
        buscar_layout.addLayout(cedula_layout)

        # Botón buscar
        btn_buscar = QPushButton("Buscar Paciente")
        btn_buscar.clicked.connect(self.buscar_paciente)
        btn_buscar.setMinimumHeight(40)
        buscar_layout.addWidget(btn_buscar)

        self.group_buscar.setLayout(buscar_layout)
        container_layout.addWidget(self.group_buscar)

        # Ocultar sección de búsqueda si el paciente viene precargado
        if self.paciente_precargado:
            self.group_buscar.setVisible(False)

        # Sección de datos del paciente (oculta inicialmente)
        self.group_datos = QGroupBox("Datos del Paciente")
        datos_layout = QVBoxLayout()
        datos_layout.setSpacing(10)
        datos_layout.setContentsMargins(10, 25, 10, 10)

        # Nombre del paciente
        nombre_layout = QHBoxLayout()
        lbl_nombre_titulo = QLabel("Nombre:")
        lbl_nombre_titulo.setMinimumWidth(120)
        self.lbl_nombre = QLabel("-")
        self.lbl_nombre.setStyleSheet("font-weight: normal; color: #2d3748;")
        nombre_layout.addWidget(lbl_nombre_titulo)
        nombre_layout.addWidget(self.lbl_nombre)
        datos_layout.addLayout(nombre_layout)

        # Dato actual
        actual_layout = QHBoxLayout()
        label_actual = {
            "direccion": "Dirección actual:",
            "telefono": "Teléfono actual:",
            "email": "Email actual:",
            "telefono_referencia": "Tel. Ref. actual:"
        }.get(self.tipo_campo, "Dato actual:")
        lbl_actual_titulo = QLabel(label_actual)
        lbl_actual_titulo.setMinimumWidth(120)
        self.lbl_dato_actual = QLabel("-")
        self.lbl_dato_actual.setStyleSheet("font-weight: normal; color: #2d3748;")
        actual_layout.addWidget(lbl_actual_titulo)
        actual_layout.addWidget(self.lbl_dato_actual)
        datos_layout.addLayout(actual_layout)

        # Campo para nuevo valor
        nuevo_layout = QHBoxLayout()
        label_nuevo = {
            "direccion": "Nueva dirección:",
            "telefono": "Nuevo teléfono:",
            "email": "Nuevo email:",
            "telefono_referencia": "Nuevo Tel. Ref.:"
        }.get(self.tipo_campo, "Nuevo valor:")
        lbl_nuevo_titulo = QLabel(label_nuevo)
        lbl_nuevo_titulo.setMinimumWidth(120)
        self.txt_nuevo_valor = QLineEdit()
        self.txt_nuevo_valor.setMinimumHeight(35)
        placeholder = {
            "direccion": "Ingrese la nueva dirección",
            "telefono": "Ingrese el nuevo teléfono",
            "email": "Ingrese el nuevo email",
            "telefono_referencia": "Ingrese el nuevo teléfono de referencia"
        }.get(self.tipo_campo, "Ingrese el nuevo valor")
        self.txt_nuevo_valor.setPlaceholderText(placeholder)
        nuevo_layout.addWidget(lbl_nuevo_titulo)
        nuevo_layout.addWidget(self.txt_nuevo_valor)
        datos_layout.addLayout(nuevo_layout)

        self.group_datos.setLayout(datos_layout)
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

        # Si el paciente viene precargado, mostrar sus datos automáticamente
        if self.paciente_precargado and self.paciente:
            self.mostrar_datos_paciente()

    def buscar_paciente(self):
        """Busca el paciente por cédula."""
        cc = self.txt_cc.text().strip()
        if not cc:
            QMessageBox.warning(self, "Advertencia", "Ingrese una cédula para buscar")
            return

        self.paciente = self.controller.consultar_paciente(cc)

        if self.paciente:
            self.cc_paciente = cc
            self.mostrar_datos_paciente()
        else:
            QMessageBox.warning(self, "No encontrado",
                              f"No se encontró un paciente con cédula {cc}")
            self.group_datos.setVisible(False)
            self.btn_actualizar.setEnabled(False)

    def mostrar_datos_paciente(self):
        """Muestra los datos del paciente en el formulario."""
        if not self.paciente:
            return

        self.lbl_nombre.setText(f"{self.paciente.nombre} {self.paciente.apellido}")

        # Mostrar el dato actual según el tipo
        dato_actual = {
            "direccion": self.paciente.direccion,
            "telefono": self.paciente.telefono,
            "email": self.paciente.email,
            "telefono_referencia": self.paciente.telefono_referencia
        }.get(self.tipo_campo, "-")
        self.lbl_dato_actual.setText(dato_actual or "No registrado")

        self.group_datos.setVisible(True)
        self.btn_actualizar.setEnabled(True)

    def cargar_datos_paciente(self):
        """Carga los datos del paciente en los campos del formulario."""
        if not self.paciente:
            return

        self.txt_cc.setText(self.cc_paciente)
        self.lbl_nombre.setText(f"{self.paciente.nombre} {self.paciente.apellido}")

        # Cargar el dato actual según el tipo
        dato_actual = {
            "direccion": self.paciente.direccion,
            "telefono": self.paciente.telefono,
            "email": self.paciente.email,
            "telefono_referencia": self.paciente.telefono_referencia
        }.get(self.tipo_campo, "-")
        self.lbl_dato_actual.setText(dato_actual or "No registrado")

    def recopilar_datos(self):
        """Recopila los datos del formulario."""
        return {
            'cedula': self.txt_cc.text().strip(),
            'nombre': self.lbl_nombre.text().strip(),
            'nuevo_valor': self.txt_nuevo_valor.text().strip(),
            'tipo_campo': self.tipo_campo
        }

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
        elif self.tipo_campo == "telefono_referencia":
            exito, mensaje = self.controller.actualizar_telefono_referencia(self.cc_paciente, nuevo_valor)
        else:
            exito, mensaje = False, "Tipo de campo no válido"

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.datos_actualizados.emit(self.cc_paciente)
            # Cerrar la ventana después de actualizar
            self.accept()
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        self.txt_cc.clear()
        self.txt_nuevo_valor.clear()
        self.lbl_nombre.setText("-")
        self.lbl_dato_actual.setText("-")
        self.cc_paciente = None
        self.btn_actualizar.setEnabled(False)

