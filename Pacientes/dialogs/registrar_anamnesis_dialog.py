from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QTextEdit, QScrollArea, QWidget
)
from PyQt6.QtCore import pyqtSignal, Qt
from ..paciente_controller import PacienteController

class RegistrarAnamnesisDilaog(QDialog):
    """
    Diálogo para registrar la anamnesis de un paciente.
    Permite buscar un paciente por cédula y registrar su anamnesis.
    """

    anamnesis_registrada = pyqtSignal(str)

    def __init__(self, controller: PacienteController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.cc_paciente = None
        self.paciente = None
        self.init_ui()

    def get_styles(self):
        """Retorna los estilos CSS para el diálogo."""
        return """
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
            QFrame#container {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
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
        self.setWindowTitle("Registrar Anamnesis")
        self.setModal(True)
        # Aumenté un poco la altura total de la ventana para acomodar los campos más grandes
        self.setMinimumSize(700, 850) 
        self.setStyleSheet(self.get_styles())

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(25, 20, 25, 20)

        # --- ÁREA DE DESPLAZAMIENTO (SCROLL) ---
        # Dado que los campos ahora son grandes, es mejor meter el formulario
        # en un ScrollArea por si la pantalla es pequeña.
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame) # Sin bordes feos
        
        # Widget contenedor dentro del scroll
        scroll_content = QWidget()
        scroll_content.setObjectName("fondo_principal")
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 10, 0) # Margen derecho para la barra de scroll

        # Título
        titulo = QLabel("Registrar Anamnesis")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Grupo: Buscar Paciente
        group_buscar = QGroupBox("Buscar Paciente")
        form_buscar = QFormLayout()
        form_buscar.setSpacing(10)

        lbl_cc = QLabel("Cédula:")
        self.txt_cc = QLineEdit()
        self.txt_cc.setPlaceholderText("Ingrese la cédula del paciente")
        form_buscar.addRow(lbl_cc, self.txt_cc)

        btn_buscar = QPushButton("Buscar Paciente")
        btn_buscar.clicked.connect(self.buscar_paciente)
        form_buscar.addRow("", btn_buscar)

        group_buscar.setLayout(form_buscar)
        layout.addWidget(group_buscar)

        # Grupo: Información del Paciente (oculto inicialmente)
        self.group_info = QGroupBox("Información del Paciente")
        form_info = QFormLayout()

        self.lbl_nombre = QLabel("-")
        self.lbl_nombre.setStyleSheet("font-weight: normal;")
        form_info.addRow(QLabel("Nombre:"), self.lbl_nombre)

        self.group_info.setLayout(form_info)
        self.group_info.setVisible(False)
        layout.addWidget(self.group_info)

        # Grupo: Datos de Anamnesis (oculto inicialmente)
        self.group_anamnesis = QGroupBox("Datos de Anamnesis")
        form_anamnesis = QVBoxLayout()
        form_anamnesis.setSpacing(15) # Más espacio entre preguntas

        # CAMBIOS APLICADOS AQUI:
        # Se cambió setMaximumHeight(80) por setMinimumHeight(100 o 120)

        # Motivo de consulta
        lbl_motivo = QLabel("Motivo de Consulta:")
        form_anamnesis.addWidget(lbl_motivo)
        self.txt_motivo_consulta = QTextEdit()
        self.txt_motivo_consulta.setPlaceholderText("Describa el motivo de la consulta...")
        self.txt_motivo_consulta.setMinimumHeight(120) # Mínimo 120px de alto
        form_anamnesis.addWidget(self.txt_motivo_consulta)

        # Enfermedad actual
        lbl_enfermedad = QLabel("Enfermedad Actual:")
        form_anamnesis.addWidget(lbl_enfermedad)
        self.txt_enfermedad_actual = QTextEdit()
        self.txt_enfermedad_actual.setPlaceholderText("Describa la enfermedad actual...")
        self.txt_enfermedad_actual.setMinimumHeight(120) # Mínimo 120px de alto
        form_anamnesis.addWidget(self.txt_enfermedad_actual)

        # Antecedentes personales
        lbl_ant_personales = QLabel("Antecedentes Personales:")
        form_anamnesis.addWidget(lbl_ant_personales)
        self.txt_antecedentes_personales = QTextEdit()
        self.txt_antecedentes_personales.setPlaceholderText("Antecedentes médicos personales...")
        self.txt_antecedentes_personales.setMinimumHeight(100)
        form_anamnesis.addWidget(self.txt_antecedentes_personales)

        # Antecedentes familiares
        lbl_ant_familiares = QLabel("Antecedentes Familiares:")
        form_anamnesis.addWidget(lbl_ant_familiares)
        self.txt_antecedentes_familiares = QTextEdit()
        self.txt_antecedentes_familiares.setPlaceholderText("Antecedentes médicos familiares...")
        self.txt_antecedentes_familiares.setMinimumHeight(100)
        form_anamnesis.addWidget(self.txt_antecedentes_familiares)

        # Alergias (Convertido a QTextEdit para que sea grande también)
        lbl_alergias = QLabel("Alergias:")
        form_anamnesis.addWidget(lbl_alergias)
        self.txt_alergias = QTextEdit() # Antes era QLineEdit
        self.txt_alergias.setPlaceholderText("Alergias conocidas...")
        self.txt_alergias.setMinimumHeight(80) 
        form_anamnesis.addWidget(self.txt_alergias)

        self.group_anamnesis.setLayout(form_anamnesis)
        self.group_anamnesis.setVisible(False)
        layout.addWidget(self.group_anamnesis)

        layout.addStretch()

        # Configurar el scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Botones de acción (fuera del scroll para que siempre se vean abajo)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.btn_guardar = QPushButton("Guardar Anamnesis")
        self.btn_guardar.clicked.connect(self.guardar_anamnesis)
        self.btn_guardar.setEnabled(False)
        buttons_layout.addWidget(self.btn_guardar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_formulario)
        buttons_layout.addWidget(btn_limpiar)

        btn_cancelar = QPushButton("Cerrar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cancelar)

        main_layout.addLayout(buttons_layout)

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
            self.group_info.setVisible(True)
            self.group_anamnesis.setVisible(True)
            self.btn_guardar.setEnabled(True)
        else:
            QMessageBox.warning(self, "No encontrado",
                              f"No se encontró un paciente con cédula {cc}")
            self.group_info.setVisible(False)
            self.group_anamnesis.setVisible(False)
            self.btn_guardar.setEnabled(False)

    def guardar_anamnesis(self):
        """Guarda la anamnesis del paciente."""
        if not self.cc_paciente:
            QMessageBox.warning(self, "Advertencia", "Primero busque un paciente")
            return

        # Validar que al menos un campo tenga datos
        # Nota: txt_alergias ahora usa toPlainText() porque lo cambiamos a QTextEdit
        if not any([
            self.txt_motivo_consulta.toPlainText().strip(),
            self.txt_enfermedad_actual.toPlainText().strip(),
            self.txt_antecedentes_personales.toPlainText().strip(),
            self.txt_antecedentes_familiares.toPlainText().strip(),
            self.txt_alergias.toPlainText().strip() 
        ]):
            QMessageBox.warning(self, "Advertencia",
                              "Ingrese al menos un dato de anamnesis")
            return

        datos_anamnesis = {
            'cc_paciente': self.cc_paciente,
            'motivo_consulta': self.txt_motivo_consulta.toPlainText().strip(),
            'enfermedad_actual': self.txt_enfermedad_actual.toPlainText().strip(),
            'antecedentes_personales': self.txt_antecedentes_personales.toPlainText().strip(),
            'antecedentes_familiares': self.txt_antecedentes_familiares.toPlainText().strip(),
            'alergias': self.txt_alergias.toPlainText().strip() # Actualizado
        }

        exito, mensaje = self.controller.registrar_anamnesis(self.cc_paciente, datos_anamnesis)

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.anamnesis_registrada.emit(self.cc_paciente)
            self.accept()  # Cerrar la ventana después de guardar
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.txt_cc.clear()
        self.txt_motivo_consulta.clear()
        self.txt_enfermedad_actual.clear()
        self.txt_antecedentes_personales.clear()
        self.txt_antecedentes_familiares.clear()
        self.txt_alergias.clear()
        self.lbl_nombre.setText("-")
        self.group_info.setVisible(False)
        self.group_anamnesis.setVisible(False)
        self.btn_guardar.setEnabled(False)
        self.cc_paciente = None
        self.paciente = None
        self.txt_cc.setFocus()