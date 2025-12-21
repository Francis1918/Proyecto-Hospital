from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QCheckBox, QWidget, QDateEdit, QCalendarWidget
)
from PyQt6.QtCore import pyqtSignal, Qt, QDate
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
            QLabel {
                color: #1a365d;
                font-size: 13px;
                font-weight: bold;
                padding: 2px;
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
            QDateEdit {
                padding: 8px;
                border: 2px solid #3182ce;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                color: #2d3748;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: 30px;
                border-left: 1px solid #3182ce;
            }
            QCalendarWidget {
                background-color: white;
            }
            QCalendarWidget QToolButton {
                color: #1a365d;
                background-color: #e8f4fc;
                border-radius: 4px;
                padding: 5px;
            }
            QCalendarWidget QMenu {
                background-color: white;
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
            QCheckBox {
                font-size: 14px;
                color: #2d3748;
                font-weight: normal;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QWidget#tab_widget {
                background-color: white;
            }
        """

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Registrar Nuevo Paciente")
        self.setModal(True)
        self.setMinimumSize(550, 900)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Título
        titulo = QLabel("Registrar Nuevo Paciente")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Contenido del formulario de datos personales
        contenido = self.crear_formulario_datos()
        layout.addWidget(contenido)

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

    def crear_formulario_datos(self) -> QWidget:
        """Crea el formulario de datos personales."""
        widget = QWidget()
        widget.setObjectName("tab_widget")
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        # Grupo: Identificación
        group_identificacion = QGroupBox("Identificación")
        form_id = QFormLayout()
        form_id.setSpacing(10)

        lbl_cc = QLabel("Cédula *:")
        self.txt_cc = QLineEdit()
        self.txt_cc.setPlaceholderText("Ej: 1234567890")
        form_id.addRow(lbl_cc, self.txt_cc)

        '''
        lbl_num_unic = QLabel("Número Único *:")
        self.txt_num_unic = QLineEdit()
        self.txt_num_unic.setPlaceholderText("Número único del sistema")
        form_id.addRow(lbl_num_unic, self.txt_num_unic)
        '''

        group_identificacion.setLayout(form_id)
        layout.addWidget(group_identificacion)
        
        # Grupo: Datos Personales
        group_personales = QGroupBox("Datos Personales")
        form_personal = QFormLayout()
        form_personal.setSpacing(10)

        lbl_nombre = QLabel("Nombre *:")
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre del paciente")
        form_personal.addRow(lbl_nombre, self.txt_nombre)

        lbl_apellido = QLabel("Apellido *:")
        self.txt_apellido = QLineEdit()
        self.txt_apellido.setPlaceholderText("Apellido del paciente")
        form_personal.addRow(lbl_apellido, self.txt_apellido)

        lbl_fecha_nac = QLabel("Fecha de Nacimiento *:")
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setCalendarPopup(True)  # Habilitar popup de calendario
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.date_nacimiento.setDate(QDate.currentDate())
        # Configurar el calendario
        calendario = QCalendarWidget()
        calendario.setGridVisible(True)
        self.date_nacimiento.setCalendarWidget(calendario)
        form_personal.addRow(lbl_fecha_nac, self.date_nacimiento)

        group_personales.setLayout(form_personal)
        layout.addWidget(group_personales)

        # Grupo: Información de Contacto
        group_contacto = QGroupBox("Información de Contacto")
        form_contacto = QFormLayout()
        form_contacto.setSpacing(10)

        lbl_direccion = QLabel("Dirección *:")
        self.txt_direccion = QLineEdit()
        self.txt_direccion.setPlaceholderText("Dirección completa")
        form_contacto.addRow(lbl_direccion, self.txt_direccion)

        lbl_telefono = QLabel("Teléfono *:")
        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("Ej: 3001234567")
        form_contacto.addRow(lbl_telefono, self.txt_telefono)

        lbl_email = QLabel("Email *:")
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("correo@ejemplo.com")
        form_contacto.addRow(lbl_email, self.txt_email)

        lbl_tel_ref = QLabel("Teléfono Referencia:")
        self.txt_telefono_ref = QLineEdit()
        self.txt_telefono_ref.setPlaceholderText("Teléfono de contacto de emergencia")
        form_contacto.addRow(lbl_tel_ref, self.txt_telefono_ref)

        group_contacto.setLayout(form_contacto)
        layout.addWidget(group_contacto)

        # Nota de campos obligatorios
        lbl_nota = QLabel("* Campos obligatorios")
        lbl_nota.setStyleSheet("color: red; font-style: italic;")
        layout.addWidget(lbl_nota)

        layout.addStretch()

        return widget

    def guardar_paciente(self):
        """Guarda el nuevo paciente con su historia clínica."""
        # Obtener fecha de nacimiento del calendario
        fecha_nac = self.date_nacimiento.date().toPyDate()

        # Crear objeto Paciente
        paciente = Paciente(
            cc=self.txt_cc.text().strip(),
            #num_unic=self.txt_num_unic.text().strip(),
            nombre=self.txt_nombre.text().strip(),
            apellido=self.txt_apellido.text().strip(),
            direccion=self.txt_direccion.text().strip(),
            telefono=self.txt_telefono.text().strip(),
            email=self.txt_email.text().strip(),
            fecha_nacimiento=fecha_nac,
            telefono_referencia=self.txt_telefono_ref.text().strip() or None
        )

        # Registrar paciente
        exito, mensaje = self.controller.registrar_paciente(paciente)

        if not exito:
            QMessageBox.warning(self, "Error", mensaje)
            return

        # Crear historia clínica si está marcado (include: crearHistoriaClinica)
        mensaje_historia = ""
        if self.chk_crear_historia.isChecked():
            exito_hist, mensaje_hist = self.controller.crear_historia_clinica(paciente.cc)
            if exito_hist:
                mensaje_historia = f"\n{mensaje_hist}"
            else:
                QMessageBox.warning(self, "Advertencia",
                                    f"Paciente registrado pero: {mensaje_hist}")

        # Emitir señal
        self.paciente_registrado.emit(paciente)
        QMessageBox.information(self, "Éxito",
                                f"Paciente {paciente.nombre} {paciente.apellido} registrado exitosamente{mensaje_historia}")

        # Abrir diálogo de anamnesis (include: registrarAnamnesis)
        respuesta = QMessageBox.question(
            self, "Registrar Anamnesis",
            "¿Desea registrar la anamnesis del paciente ahora?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            from .registrar_anamnesis_dialog import RegistrarAnamnesisDilaog
            dialogo_anamnesis = RegistrarAnamnesisDilaog(self.controller, self)
            dialogo_anamnesis.txt_cc.setText(paciente.cc)
            dialogo_anamnesis.buscar_paciente()  # Auto-buscar el paciente
            dialogo_anamnesis.exec()
        
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
            #self.txt_num_unic.clear()
            self.txt_nombre.clear()
            self.txt_apellido.clear()
            self.txt_direccion.clear()
            self.txt_telefono.clear()
            self.txt_email.clear()
            self.txt_telefono_ref.clear()
            self.date_nacimiento.setDate(QDate.currentDate())


            self.txt_cc.setFocus()

    def recopilar_datos(self):
        """Recopila los datos del formulario."""
        return {
            'cc': self.txt_cc.text().strip(),
            'nombre': self.txt_nombre.text().strip(),
            'apellido': self.txt_apellido.text().strip(),
            'direccion': self.txt_direccion.text().strip(),
            'telefono': self.txt_telefono.text().strip(),
            'email': self.txt_email.text().strip(),
            'fecha_nacimiento': self.date_nacimiento.date().toPyDate(),
            'telefono_referencia': self.txt_telefono_ref.text().strip(),
        }