from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QLabel, QGroupBox, QFormLayout, QDialog
)
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

    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle("Gestión de Pacientes")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Sección de búsqueda
        search_group = self.crear_seccion_busqueda()
        main_layout.addWidget(search_group)

        # Botones de acción
        buttons_layout = self.crear_botones_accion()
        main_layout.addLayout(buttons_layout)

        # Tabla de pacientes
        self.tabla_pacientes = self.crear_tabla_pacientes()
        main_layout.addWidget(self.tabla_pacientes)

        # Cargar datos iniciales
        self.cargar_pacientes()

    def crear_seccion_busqueda(self) -> QGroupBox:
        """Crea la sección de búsqueda de pacientes."""
        group = QGroupBox("Buscar Paciente")
        layout = QHBoxLayout()

        layout.addWidget(QLabel("Cédula:"))
        self.txt_buscar_cc = QLineEdit()
        self.txt_buscar_cc.setPlaceholderText("Ingrese cédula del paciente")
        layout.addWidget(self.txt_buscar_cc)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_paciente)
        layout.addWidget(btn_buscar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_busqueda)
        layout.addWidget(btn_limpiar)

        group.setLayout(layout)
        return group

    def crear_botones_accion(self) -> QHBoxLayout:
        """Crea los botones de acción principales."""
        layout = QHBoxLayout()

        btn_registrar = QPushButton("Registrar Paciente")
        btn_registrar.clicked.connect(self.abrir_dialogo_registrar)
        layout.addWidget(btn_registrar)

        btn_actualizar = QPushButton("Actualizar Datos")
        btn_actualizar.clicked.connect(self.abrir_dialogo_actualizar)
        layout.addWidget(btn_actualizar)

        btn_consultar = QPushButton("Consultar Detalles")
        btn_consultar.clicked.connect(self.consultar_detalles)
        layout.addWidget(btn_consultar)

        btn_historia = QPushButton("Historia Clínica")
        btn_historia.clicked.connect(self.abrir_historia_clinica)
        layout.addWidget(btn_historia)

        btn_anamnesis = QPushButton("Anamnesis")
        btn_anamnesis.clicked.connect(self.abrir_anamnesis)
        layout.addWidget(btn_anamnesis)

        layout.addStretch()

        return layout

    def crear_tabla_pacientes(self) -> QTableWidget:
        """Crea la tabla para mostrar los pacientes."""
        tabla = QTableWidget()
        tabla.setColumnCount(7)
        tabla.setHorizontalHeaderLabels([
            "Cédula", "Número Único", "Nombre", "Apellido",
            "Teléfono", "Email", "Dirección"
        ])
        tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabla.horizontalHeader().setStretchLastSection(True)

        return tabla

    def cargar_pacientes(self):
        """Carga todos los pacientes en la tabla."""
        pacientes = self.controller.listar_pacientes()
        self.tabla_pacientes.setRowCount(len(pacientes))

        for row, paciente in enumerate(pacientes):
            self.tabla_pacientes.setItem(row, 0, QTableWidgetItem(paciente.cc))
            self.tabla_pacientes.setItem(row, 1, QTableWidgetItem(paciente.num_unic))
            self.tabla_pacientes.setItem(row, 2, QTableWidgetItem(paciente.nombre))
            self.tabla_pacientes.setItem(row, 3, QTableWidgetItem(paciente.apellido))
            self.tabla_pacientes.setItem(row, 4, QTableWidgetItem(paciente.telefono))
            self.tabla_pacientes.setItem(row, 5, QTableWidgetItem(paciente.email))
            self.tabla_pacientes.setItem(row, 6, QTableWidgetItem(paciente.direccion))

    def buscar_paciente(self):
        """Busca un paciente por cédula."""
        cc = self.txt_buscar_cc.text().strip()
        if not cc:
            QMessageBox.warning(self, "Advertencia", "Ingrese una cédula para buscar")
            return

        paciente = self.controller.consultar_paciente(cc)
        if paciente:
            self.tabla_pacientes.setRowCount(1)
            self.tabla_pacientes.setItem(0, 0, QTableWidgetItem(paciente.cc))
            self.tabla_pacientes.setItem(0, 1, QTableWidgetItem(paciente.num_unic))
            self.tabla_pacientes.setItem(0, 2, QTableWidgetItem(paciente.nombre))
            self.tabla_pacientes.setItem(0, 3, QTableWidgetItem(paciente.apellido))
            self.tabla_pacientes.setItem(0, 4, QTableWidgetItem(paciente.telefono))
            self.tabla_pacientes.setItem(0, 5, QTableWidgetItem(paciente.email))
            self.tabla_pacientes.setItem(0, 6, QTableWidgetItem(paciente.direccion))
        else:
            QMessageBox.information(self, "No encontrado", "No se encontró el paciente")

    def limpiar_busqueda(self):
        """Limpia la búsqueda y recarga todos los pacientes."""
        self.txt_buscar_cc.clear()
        self.cargar_pacientes()

    def abrir_dialogo_registrar(self):
        """Abre el diálogo para registrar un nuevo paciente."""
        dialogo = RegistrarPacienteDialog(self.controller, self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.cargar_pacientes()

    def abrir_dialogo_actualizar(self):
        """Abre el diálogo para actualizar datos del paciente."""
        fila_seleccionada = self.tabla_pacientes.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente de la tabla")
            return

        cc = self.tabla_pacientes.item(fila_seleccionada, 0).text()
        dialogo = ActualizarDatosDialog(self.controller, cc, self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.cargar_pacientes()

    def consultar_detalles(self):
        """Consulta y muestra los detalles completos del paciente."""
        fila_seleccionada = self.tabla_pacientes.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente de la tabla")
            return

        cc = self.tabla_pacientes.item(fila_seleccionada, 0).text()
        paciente = self.controller.consultar_paciente(cc)

        if paciente:
            detalles = f"""
            Cédula: {paciente.cc}
            Número Único: {paciente.num_unic}
            Nombre: {paciente.nombre} {paciente.apellido}
            Dirección: {paciente.direccion}
            Teléfono: {paciente.telefono}
            Email: {paciente.email}
            Teléfono de Referencia: {paciente.telefono_referencia or 'No registrado'}
            Fecha de Registro: {paciente.fecha_registro}
            """
            QMessageBox.information(self, "Detalles del Paciente", detalles)

    def abrir_historia_clinica(self):
        """Abre la historia clínica del paciente."""
        fila_seleccionada = self.tabla_pacientes.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente de la tabla")
            return

        cc = self.tabla_pacientes.item(fila_seleccionada, 0).text()
        QMessageBox.information(self, "Historia Clínica",
                                f"Abriendo historia clínica del paciente {cc}")

    def abrir_anamnesis(self):
        """Abre la anamnesis del paciente."""
        fila_seleccionada = self.tabla_pacientes.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente de la tabla")
            return

        cc = self.tabla_pacientes.item(fila_seleccionada, 0).text()
        anamnesis = self.controller.consultar_anamnesis(cc)

        if anamnesis:
            QMessageBox.information(self, "Anamnesis", f"Anamnesis del paciente {cc}")
        else:
            QMessageBox.information(self, "Anamnesis", "No hay anamnesis registrada")


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