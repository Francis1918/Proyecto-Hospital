from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QCheckBox, QTextEdit, QTabWidget, QWidget
)
from PyQt6.QtCore import pyqtSignal, Qt
from ..paciente import Paciente
from ..paciente_controller import PacienteController


class RegistrarPacienteDialog(QDialog):
    """
    Diálogo para registrar un nuevo paciente.
    Implementa los casos de uso:
    - registrarPaciente
    - registrarAnamnesis (include)
    - crearHistoriaClinica (include)
    """

    paciente_registrado = pyqtSignal(Paciente)

    def __init__(self, controller: PacienteController, parent=None):
        super().__init__(parent)
        self.controller = controller
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
            QTabWidget::pane {
                border: 2px solid #3182ce;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e2e8f0;
                color: #1a365d;
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #3182ce;
                color: white;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #3182ce;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #2c5282;
            }
            QPushButton {
                background-color: #3182ce;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
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
            QCheckBox {
                font-size: 14px;
                color: #2d3748;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Registrar Nuevo Paciente")
        self.setModal(True)
        self.setMinimumSize(600, 700)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Título
        titulo = QLabel("Registrar Nuevo Paciente")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Crear pestañas para organizar la información
        tabs = QTabWidget()

        # Pestaña 1: Datos Personales
        tab_datos = self.crear_tab_datos_personales()
        tabs.addTab(tab_datos, "Datos Personales")

        # Pestaña 2: Anamnesis
        tab_anamnesis = self.crear_tab_anamnesis()
        tabs.addTab(tab_anamnesis, "Anamnesis")

        layout.addWidget(tabs)

        # Checkbox para crear historia clínica
        self.chk_crear_historia = QCheckBox("Crear Historia Clínica automáticamente")
        self.chk_crear_historia.setChecked(True)
        layout.addWidget(self.chk_crear_historia)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        btn_guardar = QPushButton("Guardar Paciente")
        btn_guardar.clicked.connect(self.guardar_paciente)
        buttons_layout.addWidget(btn_guardar)

        btn_limpiar = QPushButton("Limpiar Formulario")
        btn_limpiar.clicked.connect(self.limpiar_formulario)
        buttons_layout.addWidget(btn_limpiar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.clicked.connect(self.reject)
        buttons_layout.addWidget(btn_cancelar)

        layout.addLayout(buttons_layout)

    def crear_tab_datos_personales(self) -> QWidget:
        """Crea la pestaña de datos personales."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Grupo: Identificación
        group_identificacion = QGroupBox("Identificación")
        form_id = QFormLayout()

        self.txt_cc = QLineEdit()
        self.txt_cc.setPlaceholderText("Ej: 1234567890")
        form_id.addRow("Cédula *:", self.txt_cc)

        self.txt_num_unic = QLineEdit()
        self.txt_num_unic.setPlaceholderText("Número único del sistema")
        form_id.addRow("Número Único *:", self.txt_num_unic)

        group_identificacion.setLayout(form_id)
        layout.addWidget(group_identificacion)

        # Grupo: Datos Personales
        group_personales = QGroupBox("Datos Personales")
        form_personal = QFormLayout()

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre del paciente")
        form_personal.addRow("Nombre *:", self.txt_nombre)

        self.txt_apellido = QLineEdit()
        self.txt_apellido.setPlaceholderText("Apellido del paciente")
        form_personal.addRow("Apellido *:", self.txt_apellido)

        group_personales.setLayout(form_personal)
        layout.addWidget(group_personales)

        # Grupo: Información de Contacto
        group_contacto = QGroupBox("Información de Contacto")
        form_contacto = QFormLayout()

        self.txt_direccion = QLineEdit()
        self.txt_direccion.setPlaceholderText("Dirección completa")
        form_contacto.addRow("Dirección *:", self.txt_direccion)

        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("Ej: 3001234567")
        form_contacto.addRow("Teléfono *:", self.txt_telefono)

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("correo@ejemplo.com")
        form_contacto.addRow("Email *:", self.txt_email)

        self.txt_telefono_ref = QLineEdit()
        self.txt_telefono_ref.setPlaceholderText("Teléfono de contacto de emergencia")
        form_contacto.addRow("Teléfono Referencia:", self.txt_telefono_ref)

        group_contacto.setLayout(form_contacto)
        layout.addWidget(group_contacto)

        # Nota de campos obligatorios
        lbl_nota = QLabel("* Campos obligatorios")
        lbl_nota.setStyleSheet("color: red; font-style: italic;")
        layout.addWidget(lbl_nota)

        layout.addStretch()

        return widget

    def crear_tab_anamnesis(self) -> QWidget:
        """Crea la pestaña de anamnesis."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_info = QLabel("Registre la información de anamnesis del paciente:")
        lbl_info.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl_info)

        # Motivo de consulta
        layout.addWidget(QLabel("Motivo de Consulta:"))
        self.txt_motivo_consulta = QTextEdit()
        self.txt_motivo_consulta.setPlaceholderText("Describa el motivo de la consulta...")
        self.txt_motivo_consulta.setMaximumHeight(80)
        layout.addWidget(self.txt_motivo_consulta)

        # Enfermedad actual
        layout.addWidget(QLabel("Enfermedad Actual:"))
        self.txt_enfermedad_actual = QTextEdit()
        self.txt_enfermedad_actual.setPlaceholderText("Describa la enfermedad actual...")
        self.txt_enfermedad_actual.setMaximumHeight(80)
        layout.addWidget(self.txt_enfermedad_actual)

        # Antecedentes personales
        layout.addWidget(QLabel("Antecedentes Personales:"))
        self.txt_antecedentes_personales = QTextEdit()
        self.txt_antecedentes_personales.setPlaceholderText("Antecedentes médicos personales...")
        self.txt_antecedentes_personales.setMaximumHeight(80)
        layout.addWidget(self.txt_antecedentes_personales)

        # Antecedentes familiares
        layout.addWidget(QLabel("Antecedentes Familiares:"))
        self.txt_antecedentes_familiares = QTextEdit()
        self.txt_antecedentes_familiares.setPlaceholderText("Antecedentes médicos familiares...")
        self.txt_antecedentes_familiares.setMaximumHeight(80)
        layout.addWidget(self.txt_antecedentes_familiares)

        # Alergias
        layout.addWidget(QLabel("Alergias:"))
        self.txt_alergias = QLineEdit()
        self.txt_alergias.setPlaceholderText("Alergias conocidas...")
        layout.addWidget(self.txt_alergias)

        layout.addStretch()

        return widget

    def guardar_paciente(self):
        """Guarda el nuevo paciente con su anamnesis e historia clínica."""
        # Crear objeto Paciente
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

        # Registrar paciente
        exito, mensaje = self.controller.registrar_paciente(paciente)

        if not exito:
            QMessageBox.warning(self, "Error", mensaje)
            return

        # Registrar anamnesis si hay datos
        datos_anamnesis = {
            'cc_paciente': paciente.cc,
            'motivo_consulta': self.txt_motivo_consulta.toPlainText().strip(),
            'enfermedad_actual': self.txt_enfermedad_actual.toPlainText().strip(),
            'antecedentes_personales': self.txt_antecedentes_personales.toPlainText().strip(),
            'antecedentes_familiares': self.txt_antecedentes_familiares.toPlainText().strip(),
            'alergias': self.txt_alergias.text().strip()
        }

        if any(datos_anamnesis.values()):
            exito_anam, mensaje_anam = self.controller.registrar_anamnesis(
                paciente.cc, datos_anamnesis
            )
            if not exito_anam:
                QMessageBox.warning(self, "Advertencia",
                                    f"Paciente registrado pero: {mensaje_anam}")

        # Crear historia clínica si está marcado
        if self.chk_crear_historia.isChecked():
            exito_hist, mensaje_hist = self.controller.crear_historia_clinica(paciente.cc)
            if not exito_hist:
                QMessageBox.warning(self, "Advertencia",
                                    f"Paciente registrado pero: {mensaje_hist}")

        # Emitir señal y cerrar
        self.paciente_registrado.emit(paciente)
        QMessageBox.information(self, "Éxito",
                                f"Paciente {paciente.nombre} {paciente.apellido} registrado exitosamente")
        self.accept()

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        respuesta = QMessageBox.question(
            self, "Confirmar",
            "¿Está seguro de limpiar todos los campos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            # Limpiar datos personales
            self.txt_cc.clear()
            self.txt_num_unic.clear()
            self.txt_nombre.clear()
            self.txt_apellido.clear()
            self.txt_direccion.clear()
            self.txt_telefono.clear()
            self.txt_email.clear()
            self.txt_telefono_ref.clear()

            # Limpiar anamnesis
            self.txt_motivo_consulta.clear()
            self.txt_enfermedad_actual.clear()
            self.txt_antecedentes_personales.clear()
            self.txt_antecedentes_familiares.clear()
            self.txt_alergias.clear()

            self.txt_cc.setFocus()