from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QTextEdit, QTabWidget, QWidget
)
from PyQt6.QtCore import Qt
from ..paciente_controller import PacienteController


class ConsultarPacienteDialog(QDialog):
    """
    Diálogo para consultar información del paciente.
    Implementa los casos de uso:
    - consultarPaciente
    - consultarTeléfonoDeReferencia (extend)
    - consultarDirecciónDePaciente (extend)
    - consultarTeléfonoDePaciente (extend)
    - consultarAnamnesis (extend)
    """

    def __init__(self, controller: PacienteController, cc_paciente: str = None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.cc_paciente = cc_paciente
        self.paciente = None
        self.init_ui()

        if self.cc_paciente:
            self.txt_buscar_cc.setText(self.cc_paciente)
            self.consultar_paciente()

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
            QLabel {
                color: #1a365d;
                font-size: 13px;
                font-weight: bold;
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
                color: #2d3748;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #2c5282;
            }
            QLineEdit:read-only, QTextEdit:read-only {
                background-color: #f7fafc;
                color: #2d3748;
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
            QPushButton#btn_cerrar {
                background-color: #718096;
            }
            QPushButton#btn_cerrar:hover {
                background-color: #4a5568;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3182ce;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                padding-top: 25px;
                background-color: white;
            }
            QGroupBox::title {
                color: #1a365d;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                top: 5px;
                padding: 0 8px;
                background-color: white;
                font-size: 14px;
            }
        """

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Consultar Paciente")
        self.setModal(True)
        self.setMinimumSize(700, 600)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Título
        titulo = QLabel("Consultar Paciente")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Sección de búsqueda
        group_busqueda = QGroupBox("Buscar Paciente")
        hbox_busqueda = QHBoxLayout()

        hbox_busqueda.addWidget(QLabel("Cédula:"))
        self.txt_buscar_cc = QLineEdit()
        self.txt_buscar_cc.setPlaceholderText("Ingrese la cédula del paciente")
        hbox_busqueda.addWidget(self.txt_buscar_cc)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.consultar_paciente)
        hbox_busqueda.addWidget(btn_buscar)

        group_busqueda.setLayout(hbox_busqueda)
        layout.addWidget(group_busqueda)

        # Pestañas de información
        self.tabs = QTabWidget()
        self.tabs.setEnabled(False)

        # Pestaña 1: Datos Personales
        tab_datos = self.crear_tab_datos_personales()
        self.tabs.addTab(tab_datos, "Datos Personales")

        # Pestaña 2: Información de Contacto
        tab_contacto = self.crear_tab_contacto()
        self.tabs.addTab(tab_contacto, "Información de Contacto")

        # Pestaña 3: Anamnesis
        tab_anamnesis = self.crear_tab_anamnesis()
        self.tabs.addTab(tab_anamnesis, "Anamnesis")

        layout.addWidget(self.tabs)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        btn_imprimir = QPushButton("Imprimir Información")
        btn_imprimir.clicked.connect(self.imprimir_informacion)
        buttons_layout.addWidget(btn_imprimir)

        btn_exportar = QPushButton("Exportar a PDF")
        btn_exportar.clicked.connect(self.exportar_pdf)
        buttons_layout.addWidget(btn_exportar)

        buttons_layout.addStretch()

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("btn_cerrar")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)

        layout.addLayout(buttons_layout)

    def crear_tab_datos_personales(self) -> QWidget:
        """Crea la pestaña de datos personales."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group = QGroupBox("Información Personal")
        form = QFormLayout()

        self.lbl_cc = QLabel("-")
        form.addRow("Cédula:", self.lbl_cc)

        self.lbl_num_unic = QLabel("-")
        form.addRow("Número Único:", self.lbl_num_unic)

        self.lbl_nombre = QLabel("-")
        form.addRow("Nombre:", self.lbl_nombre)

        self.lbl_apellido = QLabel("-")
        form.addRow("Apellido:", self.lbl_apellido)

        self.lbl_fecha_registro = QLabel("-")
        form.addRow("Fecha de Registro:", self.lbl_fecha_registro)

        self.lbl_id_fac = QLabel("-")
        form.addRow("ID Facultad:", self.lbl_id_fac)

        group.setLayout(form)
        layout.addWidget(group)
        layout.addStretch()

        return widget

    def crear_tab_contacto(self) -> QWidget:
        """Crea la pestaña de información de contacto."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Grupo: Contacto Principal
        group_principal = QGroupBox("Contacto Principal")
        form_principal = QFormLayout()

        self.lbl_direccion = QLabel("-")
        self.lbl_direccion.setWordWrap(True)
        form_principal.addRow("Dirección:", self.lbl_direccion)

        self.lbl_telefono = QLabel("-")
        form_principal.addRow("Teléfono:", self.lbl_telefono)

        self.lbl_email = QLabel("-")
        form_principal.addRow("Email:", self.lbl_email)

        group_principal.setLayout(form_principal)
        layout.addWidget(group_principal)

        # Grupo: Contacto de Referencia
        group_referencia = QGroupBox("Contacto de Referencia")
        form_referencia = QFormLayout()

        self.lbl_telefono_ref = QLabel("-")
        form_referencia.addRow("Teléfono de Referencia:", self.lbl_telefono_ref)

        group_referencia.setLayout(form_referencia)
        layout.addWidget(group_referencia)

        # Botones de consulta específica
        buttons_layout = QHBoxLayout()

        btn_consultar_dir = QPushButton("Consultar Solo Dirección")
        btn_consultar_dir.clicked.connect(self.consultar_direccion)
        buttons_layout.addWidget(btn_consultar_dir)

        btn_consultar_tel = QPushButton("Consultar Solo Teléfono")
        btn_consultar_tel.clicked.connect(self.consultar_telefono)
        buttons_layout.addWidget(btn_consultar_tel)

        btn_consultar_tel_ref = QPushButton("Consultar Tel. Referencia")
        btn_consultar_tel_ref.clicked.connect(self.consultar_telefono_referencia)
        buttons_layout.addWidget(btn_consultar_tel_ref)

        layout.addLayout(buttons_layout)
        layout.addStretch()

        return widget

    def crear_tab_anamnesis(self) -> QWidget:
        """Crea la pestaña de anamnesis."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Información de Anamnesis")
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 11pt;")
        layout.addWidget(lbl_titulo)

        self.txt_anamnesis = QTextEdit()
        self.txt_anamnesis.setReadOnly(True)
        layout.addWidget(self.txt_anamnesis)

        btn_consultar_anamnesis = QPushButton("Actualizar Anamnesis")
        btn_consultar_anamnesis.clicked.connect(self.consultar_anamnesis)
        layout.addWidget(btn_consultar_anamnesis)

        return widget

    def consultar_paciente(self):
        """Consulta y muestra la información completa del paciente."""
        cc = self.txt_buscar_cc.text().strip()

        if not cc:
            QMessageBox.warning(self, "Advertencia", "Ingrese una cédula para buscar")
            return

        self.paciente = self.controller.consultar_paciente(cc)

        if not self.paciente:
            QMessageBox.information(self, "No encontrado",
                                    f"No se encontró un paciente con cédula {cc}")
            self.tabs.setEnabled(False)
            return

        # Habilitar pestañas
        self.tabs.setEnabled(True)

        # Llenar datos personales
        self.lbl_cc.setText(self.paciente.cc)
        self.lbl_num_unic.setText(self.paciente.num_unic)
        self.lbl_nombre.setText(self.paciente.nombre)
        self.lbl_apellido.setText(self.paciente.apellido)
        self.lbl_fecha_registro.setText(str(self.paciente.fecha_registro))
        self.lbl_id_fac.setText(str(self.paciente.id_fac) if self.paciente.id_fac else "No asignado")

        # Llenar información de contacto
        self.lbl_direccion.setText(self.paciente.direccion)
        self.lbl_telefono.setText(self.paciente.telefono)
        self.lbl_email.setText(self.paciente.email)
        self.lbl_telefono_ref.setText(
            self.paciente.telefono_referencia or "No registrado"
        )

        # Consultar anamnesis
        self.consultar_anamnesis()

        QMessageBox.information(self, "Éxito",
                                f"Paciente {self.paciente.nombre} {self.paciente.apellido} encontrado")

    def consultar_direccion(self):
        """Consulta solo la dirección del paciente."""
        if not self.paciente:
            QMessageBox.warning(self, "Advertencia", "Primero busque un paciente")
            return

        direccion = self.controller.consultar_direccion_paciente(self.paciente.cc)
        QMessageBox.information(self, "Dirección del Paciente",
                                f"Dirección: {direccion}")

    def consultar_telefono(self):
        """Consulta solo el teléfono del paciente."""
        if not self.paciente:
            QMessageBox.warning(self, "Advertencia", "Primero busque un paciente")
            return

        telefono = self.controller.consultar_telefono_paciente(self.paciente.cc)
        QMessageBox.information(self, "Teléfono del Paciente",
                                f"Teléfono: {telefono}")

    def consultar_telefono_referencia(self):
        """Consulta solo el teléfono de referencia del paciente."""
        if not self.paciente:
            QMessageBox.warning(self, "Advertencia", "Primero busque un paciente")
            return

        telefono_ref = self.controller.consultar_telefono_referencia(self.paciente.cc)
        QMessageBox.information(self, "Teléfono de Referencia",
                                f"Teléfono de Referencia: {telefono_ref or 'No registrado'}")

    def consultar_anamnesis(self):
        """Consulta la anamnesis del paciente."""
        if not self.paciente:
            return

        anamnesis = self.controller.consultar_anamnesis(self.paciente.cc)

        if anamnesis:
            texto = f"""
MOTIVO DE CONSULTA:
{anamnesis.get('motivo_consulta', 'No registrado')}

ENFERMEDAD ACTUAL:
{anamnesis.get('enfermedad_actual', 'No registrado')}

ANTECEDENTES PERSONALES:
{anamnesis.get('antecedentes_personales', 'No registrado')}

ANTECEDENTES FAMILIARES:
{anamnesis.get('antecedentes_familiares', 'No registrado')}

ALERGIAS:
{anamnesis.get('alergias', 'No registrado')}
            """
            self.txt_anamnesis.setText(texto.strip())
        else:
            self.txt_anamnesis.setText("No hay información de anamnesis registrada para este paciente.")

    def imprimir_informacion(self):
        """Imprime la información del paciente."""
        if not self.paciente:
            QMessageBox.warning(self, "Advertencia", "No hay información para imprimir")
            return

        QMessageBox.information(self, "Imprimir",
                                "Función de impresión en desarrollo")

    def exportar_pdf(self):
        """Exporta la información del paciente a PDF."""
        if not self.paciente:
            QMessageBox.warning(self, "Advertencia", "No hay información para exportar")
            return

        QMessageBox.information(self, "Exportar PDF",
                                "Función de exportación a PDF en desarrollo")