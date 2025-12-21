from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QTextEdit, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt
from ..paciente_controller import PacienteController


class HistoriaClinicaDialog(QDialog):
    """
    Diálogo para consultar la historia clínica de un paciente.
    Permite buscar por cédula o código único.
    """

    def __init__(self, controller: PacienteController, parent=None, paciente=None):
        super().__init__(parent)
        self.controller = controller
        self.paciente = paciente
        self.cc_paciente = paciente.cc if paciente else None
        self.paciente_precargado = paciente is not None
        self.init_ui()

        # Si viene con paciente precargado, cargar datos automáticamente
        if self.paciente_precargado:
            self.cargar_historia_clinica()

    def get_styles(self):
        """Retorna los estilos CSS para el diálogo."""
        return """
            QDialog {
                background-color: #e8f4fc;
            }
            QWidget#fondo_principal {
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
                padding: 2px;
            }
            QLabel#info_label {
                font-weight: normal;
                color: #2d3748;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #3182ce;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                color: #2d3748;
            }
            QLineEdit:focus {
                border-color: #2c5282;
            }
            QTextEdit {
                padding: 10px;
                border: 2px solid #3182ce;
                border-radius: 6px;
                font-size: 13px;
                background-color: #f7fafc;
                color: #2d3748;
            }
            QPushButton {
                background-color: #3182ce;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
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
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Historia Clínica")
        self.setModal(True)
        self.setMinimumSize(700, 650)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Título
        titulo = QLabel("Historia Clínica")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Grupo: Buscar Paciente (oculto si viene precargado)
        self.group_buscar = QGroupBox("Buscar Paciente")
        form_buscar = QHBoxLayout()
        form_buscar.setSpacing(10)

        lbl_cc = QLabel("Cédula:")
        form_buscar.addWidget(lbl_cc)

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Ingrese cédula")
        self.txt_buscar.returnPressed.connect(self.buscar_paciente)
        form_buscar.addWidget(self.txt_buscar)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_paciente)
        form_buscar.addWidget(btn_buscar)

        self.group_buscar.setLayout(form_buscar)
        layout.addWidget(self.group_buscar)

        # Ocultar búsqueda si viene precargado
        if self.paciente_precargado:
            self.group_buscar.setVisible(False)

        # Scroll Area para el contenido de la historia clínica
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setObjectName("fondo_principal")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Grupo: Información del Paciente
        self.group_paciente = QGroupBox("Información del Paciente")
        form_paciente = QFormLayout()
        form_paciente.setSpacing(10)

        self.lbl_num_historia = QLabel("-")
        self.lbl_num_historia.setObjectName("info_label")
        self.lbl_num_historia.setStyleSheet("color: #3182ce; font-weight: bold;")
        form_paciente.addRow(QLabel("N° Historia Clínica:"), self.lbl_num_historia)

        self.lbl_cc = QLabel("-")
        self.lbl_cc.setObjectName("info_label")
        form_paciente.addRow(QLabel("Cédula:"), self.lbl_cc)

        self.lbl_nombre = QLabel("-")
        self.lbl_nombre.setObjectName("info_label")
        form_paciente.addRow(QLabel("Nombre Completo:"), self.lbl_nombre)

        self.lbl_fecha_nacimiento = QLabel("-")
        self.lbl_fecha_nacimiento.setObjectName("info_label")
        form_paciente.addRow(QLabel("Fecha de Nacimiento:"), self.lbl_fecha_nacimiento)

        self.lbl_telefono = QLabel("-")
        self.lbl_telefono.setObjectName("info_label")
        form_paciente.addRow(QLabel("Teléfono:"), self.lbl_telefono)

        self.lbl_email = QLabel("-")
        self.lbl_email.setObjectName("info_label")
        form_paciente.addRow(QLabel("Email:"), self.lbl_email)

        self.lbl_direccion = QLabel("-")
        self.lbl_direccion.setObjectName("info_label")
        form_paciente.addRow(QLabel("Dirección:"), self.lbl_direccion)

        self.lbl_fecha_registro = QLabel("-")
        self.lbl_fecha_registro.setObjectName("info_label")
        form_paciente.addRow(QLabel("Fecha de Registro:"), self.lbl_fecha_registro)

        self.lbl_estado_historia = QLabel("-")
        self.lbl_estado_historia.setObjectName("info_label")
        form_paciente.addRow(QLabel("Estado:"), self.lbl_estado_historia)

        self.group_paciente.setLayout(form_paciente)
        self.group_paciente.setVisible(False)
        scroll_layout.addWidget(self.group_paciente)

        # Grupo: Anamnesis
        self.group_anamnesis = QGroupBox("Anamnesis")
        anamnesis_layout = QVBoxLayout()
        anamnesis_layout.setSpacing(10)

        lbl_motivo = QLabel("Motivo de Consulta:")
        anamnesis_layout.addWidget(lbl_motivo)
        self.txt_motivo = QTextEdit()
        self.txt_motivo.setReadOnly(True)
        self.txt_motivo.setMaximumHeight(60)
        anamnesis_layout.addWidget(self.txt_motivo)

        lbl_enfermedad = QLabel("Enfermedad Actual:")
        anamnesis_layout.addWidget(lbl_enfermedad)
        self.txt_enfermedad = QTextEdit()
        self.txt_enfermedad.setReadOnly(True)
        self.txt_enfermedad.setMaximumHeight(60)
        anamnesis_layout.addWidget(self.txt_enfermedad)

        lbl_ant_personales = QLabel("Antecedentes Personales:")
        anamnesis_layout.addWidget(lbl_ant_personales)
        self.txt_ant_personales = QTextEdit()
        self.txt_ant_personales.setReadOnly(True)
        self.txt_ant_personales.setMaximumHeight(60)
        anamnesis_layout.addWidget(self.txt_ant_personales)

        lbl_ant_familiares = QLabel("Antecedentes Familiares:")
        anamnesis_layout.addWidget(lbl_ant_familiares)
        self.txt_ant_familiares = QTextEdit()
        self.txt_ant_familiares.setReadOnly(True)
        self.txt_ant_familiares.setMaximumHeight(60)
        anamnesis_layout.addWidget(self.txt_ant_familiares)

        lbl_alergias = QLabel("Alergias:")
        anamnesis_layout.addWidget(lbl_alergias)
        self.txt_alergias = QLineEdit()
        self.txt_alergias.setReadOnly(True)
        anamnesis_layout.addWidget(self.txt_alergias)

        self.group_anamnesis.setLayout(anamnesis_layout)
        self.group_anamnesis.setVisible(False)
        scroll_layout.addWidget(self.group_anamnesis)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.btn_imprimir = QPushButton("Imprimir")
        self.btn_imprimir.clicked.connect(self.imprimir_historia)
        self.btn_imprimir.setEnabled(False)
        buttons_layout.addWidget(self.btn_imprimir)

        buttons_layout.addStretch()

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("btn_cerrar")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)

        layout.addLayout(buttons_layout)

    def cargar_historia_clinica(self):
        """Carga la historia clínica cuando el paciente viene precargado."""
        if not self.paciente or not self.cc_paciente:
            return

        # Verificar si tiene historia clínica
        historia = self.controller.consultar_historia_clinica(self.cc_paciente)

        if historia:
            self.mostrar_datos_paciente(historia)
            self.cargar_anamnesis()
            self.group_paciente.setVisible(True)
            self.group_anamnesis.setVisible(True)
            self.btn_imprimir.setEnabled(True)
        else:
            # El paciente existe pero no tiene historia clínica
            respuesta = QMessageBox.question(
                self, "Sin Historia Clínica",
                f"El paciente {self.paciente.nombre} {self.paciente.apellido} no tiene historia clínica.\n¿Desea crearla ahora?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                exito, mensaje = self.controller.crear_historia_clinica(self.cc_paciente)
                if exito:
                    QMessageBox.information(self, "Éxito", mensaje)
                    historia = self.controller.consultar_historia_clinica(self.cc_paciente)
                    self.mostrar_datos_paciente(historia)
                    self.cargar_anamnesis()
                    self.group_paciente.setVisible(True)
                    self.group_anamnesis.setVisible(True)
                    self.btn_imprimir.setEnabled(True)
                else:
                    QMessageBox.warning(self, "Error", mensaje)
            else:
                self.limpiar_datos()

    def buscar_paciente(self):
        """Busca el paciente por cédula o código único."""
        busqueda = self.txt_buscar.text().strip()
        if not busqueda:
            QMessageBox.warning(self, "Advertencia", "Ingrese una cédula o código único para buscar")
            return

        # Intentar buscar por cédula primero
        self.paciente = self.controller.consultar_paciente(busqueda)

        # Si no encuentra por cédula, buscar por código único
        if not self.paciente:
            self.paciente = self.controller.consultar_paciente_por_codigo(busqueda)

        if self.paciente:
            self.cc_paciente = self.paciente.cc

            # Verificar si tiene historia clínica
            historia = self.controller.consultar_historia_clinica(self.cc_paciente)

            if historia:
                self.mostrar_datos_paciente(historia)
                self.cargar_anamnesis()
                self.group_paciente.setVisible(True)
                self.group_anamnesis.setVisible(True)
                self.btn_imprimir.setEnabled(True)
            else:
                # El paciente existe pero no tiene historia clínica
                respuesta = QMessageBox.question(
                    self, "Sin Historia Clínica",
                    f"El paciente {self.paciente.nombre} {self.paciente.apellido} no tiene historia clínica.\n¿Desea crearla ahora?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if respuesta == QMessageBox.StandardButton.Yes:
                    exito, mensaje = self.controller.crear_historia_clinica(self.cc_paciente)
                    if exito:
                        QMessageBox.information(self, "Éxito", mensaje)
                        historia = self.controller.consultar_historia_clinica(self.cc_paciente)
                        self.mostrar_datos_paciente(historia)
                        self.cargar_anamnesis()
                        self.group_paciente.setVisible(True)
                        self.group_anamnesis.setVisible(True)
                        self.btn_imprimir.setEnabled(True)
                    else:
                        QMessageBox.warning(self, "Error", mensaje)
                else:
                    self.limpiar_datos()
        else:
            QMessageBox.warning(self, "No encontrado",
                              f"No se encontró un paciente con cédula o código: {busqueda}")
            self.limpiar_datos()

    def mostrar_datos_paciente(self, historia=None):
        """Muestra los datos del paciente en el formulario."""
        if self.paciente:
            # Mostrar número de historia clínica
            if historia:
                self.lbl_num_historia.setText(historia.get('numero_historia', 'No asignado'))
                self.lbl_estado_historia.setText(historia.get('estado', 'Desconocido'))
            else:
                self.lbl_num_historia.setText("No tiene historia clínica")
                self.lbl_estado_historia.setText("-")

            self.lbl_cc.setText(self.paciente.cc)
            self.lbl_nombre.setText(f"{self.paciente.nombre} {self.paciente.apellido}")

            # Mostrar fecha de nacimiento
            if self.paciente.fecha_nacimiento:
                fecha_nac = self.paciente.fecha_nacimiento.strftime("%d/%m/%Y")
                self.lbl_fecha_nacimiento.setText(fecha_nac)
            else:
                self.lbl_fecha_nacimiento.setText("No registrada")

            self.lbl_telefono.setText(self.paciente.telefono or "-")
            self.lbl_email.setText(self.paciente.email or "-")
            self.lbl_direccion.setText(self.paciente.direccion or "-")
            self.lbl_fecha_registro.setText(str(self.paciente.fecha_registro) if self.paciente.fecha_registro else "-")

    def cargar_anamnesis(self):
        """Carga los datos de anamnesis del paciente."""
        if not self.cc_paciente:
            return

        anamnesis = self.controller.consultar_anamnesis(self.cc_paciente)

        if anamnesis:
            self.txt_motivo.setText(anamnesis.get('motivo_consulta', 'No registrado'))
            self.txt_enfermedad.setText(anamnesis.get('enfermedad_actual', 'No registrado'))
            self.txt_ant_personales.setText(anamnesis.get('antecedentes_personales', 'No registrado'))
            self.txt_ant_familiares.setText(anamnesis.get('antecedentes_familiares', 'No registrado'))
            self.txt_alergias.setText(anamnesis.get('alergias', 'No registrado'))
        else:
            self.txt_motivo.setText("No hay anamnesis registrada")
            self.txt_enfermedad.setText("No hay anamnesis registrada")
            self.txt_ant_personales.setText("No hay anamnesis registrada")
            self.txt_ant_familiares.setText("No hay anamnesis registrada")
            self.txt_alergias.setText("No hay anamnesis registrada")

    def limpiar_datos(self):
        """Limpia todos los datos mostrados."""
        self.lbl_num_historia.setText("-")
        self.lbl_cc.setText("-")
        self.lbl_nombre.setText("-")
        self.lbl_fecha_nacimiento.setText("-")
        self.lbl_telefono.setText("-")
        self.lbl_email.setText("-")
        self.lbl_direccion.setText("-")
        self.lbl_fecha_registro.setText("-")
        self.lbl_estado_historia.setText("-")
        self.txt_motivo.clear()
        self.txt_enfermedad.clear()
        self.txt_ant_personales.clear()
        self.txt_ant_familiares.clear()
        self.txt_alergias.clear()
        self.group_paciente.setVisible(False)
        self.group_anamnesis.setVisible(False)
        self.btn_imprimir.setEnabled(False)
        self.cc_paciente = None
        self.paciente = None

    def imprimir_historia(self):
        """Función para imprimir la historia clínica."""
        if not self.paciente:
            QMessageBox.warning(self, "Advertencia", "No hay historia clínica para imprimir")
            return

        QMessageBox.information(self, "Imprimir",
                              f"Preparando impresión de historia clínica de:\n{self.paciente.nombre} {self.paciente.apellido}\n\nFuncionalidad de impresión en desarrollo.")

