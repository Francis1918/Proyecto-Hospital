from datetime import date
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QCheckBox, QDateEdit, QScrollArea, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal

# Importamos tema y utilidades
from core.theme import AppPalette, STYLES
from core.utils import get_icon
from Pacientes.paciente import Paciente
# Asegúrate de que esta importación apunte a tu diálogo existente
from Pacientes.dialogs import RegistrarAnamnesisDilaog 

class RegistrarPacienteView(QWidget):
    # Señal para avisar al módulo principal que se creó un paciente (para refrescar tablas)
    paciente_registrado_signal = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        # Layout Principal (sin márgenes para que el scroll pegue a los bordes)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- 1. ÁREA DE SCROLL (Para pantallas pequeñas) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        # Widget contenedor dentro del scroll
        content_widget = QWidget()
        self.layout_content = QVBoxLayout(content_widget)
        self.layout_content.setSpacing(20)
        self.layout_content.setContentsMargins(20, 20, 30, 20) # Margen derecho extra para la barra scroll

        # --- 2. SECCIONES DEL FORMULARIO (Tarjetas) ---
        self.setup_identificacion()
        self.setup_datos_personales()
        self.setup_contacto()

        # --- 4. SECCIÓN ANAMNESIS (Integrada) ---
        self.setup_anamnesis()




        self.layout_content.addStretch() # Empuja todo hacia arriba
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # --- 3. BARRA DE ACCIONES INFERIOR (Fija) ---
        action_bar = QFrame()
        action_bar.setStyleSheet(f"background-color: {AppPalette.white_01}; border-top: 1px solid {AppPalette.Border};")
        bar_layout = QHBoxLayout(action_bar)
        bar_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botón Limpiar
        self.btn_limpiar = QPushButton(" Limpiar Formulario")
        self.btn_limpiar.setIcon(get_icon("refresh.svg", AppPalette.black_02))
        self.btn_limpiar.setStyleSheet(STYLES["btn_icon_ghost"])
        self.btn_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)

        # Botón Guardar
        self.btn_guardar = QPushButton(" Guardar Paciente")
        self.btn_guardar.setIcon(get_icon("save.svg", "white"))
        self.btn_guardar.setStyleSheet(STYLES["btn_primary"])
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.setMinimumHeight(45)
        self.btn_guardar.setMinimumWidth(200)
        self.btn_guardar.clicked.connect(self.guardar_paciente)

        bar_layout.addWidget(self.btn_limpiar)
        bar_layout.addStretch()
        bar_layout.addWidget(self.btn_guardar)

        main_layout.addWidget(action_bar)

    # --- MÉTODOS DE CONSTRUCCIÓN DE UI ---
    def setup_identificacion(self):
        frame = QFrame()
        frame.setStyleSheet(STYLES["card"])
        l = QVBoxLayout(frame)
        l.setContentsMargins(20, 20, 20, 20)
        
        # Título de sección con icono (opcional)
        l.addWidget(QLabel("Identificación", objectName="h2"))
        
        self.txt_cc = QLineEdit()
        self.txt_cc.setPlaceholderText("Ej: 1712345678")
        
        # Usamos un FormLayout para alinear etiqueta y campo
        form = QFormLayout()
        form.addRow("Número de Cédula / DNI *:", self.txt_cc)
        
        l.addLayout(form)
        self.layout_content.addWidget(frame)

    def setup_datos_personales(self):
        frame = QFrame()
        frame.setStyleSheet(STYLES["card"])
        l = QVBoxLayout(frame)
        l.setContentsMargins(20, 20, 20, 20)
        
        l.addWidget(QLabel("Datos Personales", objectName="h2"))
        
        # Grid para poner Nombre y Apellido en la misma fila
        grid = QHBoxLayout()
        
        # Nombre
        v1 = QVBoxLayout()
        v1.addWidget(QLabel("Nombres *:"))
        self.txt_nombre = QLineEdit()
        v1.addWidget(self.txt_nombre)
        
        # Apellido
        v2 = QVBoxLayout()
        v2.addWidget(QLabel("Apellidos *:"))
        self.txt_apellido = QLineEdit()
        v2.addWidget(self.txt_apellido)
        
        grid.addLayout(v1)
        grid.addLayout(v2)
        l.addLayout(grid)

        l.addSpacing(10)

        # Fecha Nacimiento
        row_fecha = QHBoxLayout()
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setCalendarPopup(True)
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.date_nacimiento.setDate(QDate.currentDate())
        self.date_nacimiento.setFixedWidth(160)
        
        row_fecha.addWidget(QLabel("Fecha de Nacimiento *: "))
        
        # Configuración forzada del calendario interno
        calendar = self.date_nacimiento.calendarWidget()
        calendar.setVerticalHeaderFormat(calendar.VerticalHeaderFormat.NoVerticalHeader)
        calendar.setNavigationBarVisible(True)

        # Estilo específico inyectado para corregir calendario (Hardcoded Styles)
        self.date_nacimiento.setStyleSheet("""
            QDateEdit {
                color: #2d3748;
                font-weight: bold;
                padding: 5px;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #f7fafc; 
            }
        """)
        row_fecha.addWidget(self.date_nacimiento)
        row_fecha.addStretch()
        
        l.addLayout(row_fecha)
        self.layout_content.addWidget(frame)

    def setup_contacto(self):
        frame = QFrame()
        frame.setStyleSheet(STYLES["card"])
        l = QVBoxLayout(frame)
        l.setContentsMargins(20, 20, 20, 20)
        
        l.addWidget(QLabel("Información de Contacto", objectName="h2"))
        
        form = QFormLayout()
        form.setSpacing(12)
        
        self.txt_direccion = QLineEdit()
        self.txt_telefono = QLineEdit()
        self.txt_email = QLineEdit()
        self.txt_telefono_ref = QLineEdit()
        
        form.addRow("Dirección:", self.txt_direccion)
        form.addRow("Teléfono Móvil:", self.txt_telefono)
        form.addRow("Correo Electrónico:", self.txt_email)
        form.addRow("Tel. Referencia (Emergencia):", self.txt_telefono_ref)
        
        l.addLayout(form)
        self.layout_content.addWidget(frame)

    def setup_anamnesis(self):
        """Crea la sección de anamnesis en el formulario principal."""
        frame = QFrame()
        frame.setStyleSheet(STYLES["card"])
        l = QVBoxLayout(frame)
        l.setContentsMargins(20, 20, 20, 20)
        l.setSpacing(15)
        
        l.addWidget(QLabel("Antecedentes (Anamnesis)", objectName="h2"))
        
        # Campos de texto multilínea
        self.txt_motivo = QTextEdit()
        self.txt_motivo.setPlaceholderText("Motivo de consulta...")
        self.txt_motivo.setMinimumHeight(60)
        l.addWidget(QLabel("Motivo de Consulta:"))
        l.addWidget(self.txt_motivo)
        
        self.txt_enfermedad = QTextEdit()
        self.txt_enfermedad.setPlaceholderText("Enfermedad actual...")
        self.txt_enfermedad.setMinimumHeight(60)
        l.addWidget(QLabel("Enfermedad Actual:"))
        l.addWidget(self.txt_enfermedad)
        
        # Grid para antecedentes
        grid = QHBoxLayout()
        
        v1 = QVBoxLayout()
        v1.addWidget(QLabel("Ant. Personales:"))
        self.txt_ant_personales = QTextEdit()
        self.txt_ant_personales.setMinimumHeight(60)
        v1.addWidget(self.txt_ant_personales)
        
        v2 = QVBoxLayout()
        v2.addWidget(QLabel("Ant. Familiares:"))
        self.txt_ant_familiares = QTextEdit()
        self.txt_ant_familiares.setMinimumHeight(60)
        v2.addWidget(self.txt_ant_familiares)
        
        grid.addLayout(v1)
        grid.addLayout(v2)
        l.addLayout(grid)
        
        self.txt_alergias = QTextEdit()
        self.txt_alergias.setPlaceholderText("Alergias conocidas...")
        self.txt_alergias.setMinimumHeight(50)
        l.addWidget(QLabel("Alergias:"))
        l.addWidget(self.txt_alergias)

        self.layout_content.addWidget(frame)

    # --- LÓGICA DE NEGOCIO ---
    def guardar_paciente(self):
        # 1. Validaciones
        cc = self.txt_cc.text().strip()
        nombre = self.txt_nombre.text().strip()
        apellido = self.txt_apellido.text().strip()
        
        # Validar Anamnesis Obligatoria (Antes de guardar nada)
        motivo = self.txt_motivo.toPlainText().strip()
        enfermedad = self.txt_enfermedad.toPlainText().strip()
        ant_personales = self.txt_ant_personales.toPlainText().strip()
        ant_familiares = self.txt_ant_familiares.toPlainText().strip()
        alergias = self.txt_alergias.toPlainText().strip()

        if not motivo or not enfermedad or not ant_personales or not ant_familiares or not alergias:
             QMessageBox.warning(self, "Anamnesis Incompleta", 
                                 "Todos los campos de la Anamnesis son obligatorios:\n"
                                 "- Motivo de Consulta\n- Enfermedad Actual\n"
                                 "- Antecedentes (Personales/Familiares)\n- Alergias")
             return

        # 2. Crear Objeto Paciente
        # Se omite pre-validación manual para delegar todo a paciente.validar_datos()


        # 2. Crear Objeto Paciente
        fecha_nac = self.date_nacimiento.date().toPyDate()
        paciente = Paciente(
            cc=cc,
            nombre=nombre,
            apellido=apellido,
            direccion=self.txt_direccion.text().strip(),
            telefono=self.txt_telefono.text().strip(),
            email=self.txt_email.text().strip(),
            fecha_nacimiento=fecha_nac,
            telefono_referencia=self.txt_telefono_ref.text().strip() or None
        )

        # 3. Guardar Paciente (Insertar BD)
        # Nota: registrar_paciente llama internamente a validaciones de lógica de negocio (regex, edad, etc)
        exito, mensaje = self.controller.registrar_paciente(paciente)

        if not exito:
            QMessageBox.warning(self, "Error al Registrar", mensaje)
            return

        # 4. Crear Historia Clínica (Obligatorio)
        exito_hc, msg_hc = self.controller.crear_historia_clinica(paciente.cc)
        if not exito_hc:
            # ROLLBACK: Borrar paciente recién creado si falla la HC
            self.controller.eliminar_paciente(paciente.cc)
            QMessageBox.critical(self, "Error Crítico", 
                               f"No se pudo crear la historia clínica.\nError: {msg_hc}\n\n"
                               "La operación ha sido cancelada y el paciente no se guardó.")
            return

        # 5. Registrar Anamnesis (Si hay datos ingresados)
        # 5. Registrar Anamnesis (Obligatorio)
        datos_anamnesis = {
            'cc_paciente': paciente.cc,
            'motivo_consulta': motivo,
            'enfermedad_actual': enfermedad,
            'antecedentes_personales': ant_personales,
            'antecedentes_familiares': ant_familiares,
            'alergias': alergias
        }
        
        exito_ana, msg_ana = self.controller.registrar_anamnesis(paciente.cc, datos_anamnesis)
        if not exito_ana:
             # Si falla anamnesis, advertimos (Aunque el paciente ya se guardó con HC, esto es un error parcial)
             QMessageBox.warning(self, "Advertencia", 
                               f"Paciente guardado e HC creada, pero hubo un error al guardar anamnesis: {msg_ana}")

        # 6. Confirmación y Limpieza
        QMessageBox.information(self, "Registro Exitoso", 
                              f"PACIENTE REGISTRADO CORRECTAMENTE.\n\n"
                              f"• Datos Personales: OK\n"
                              f"• Historia Clínica: Creada ({msg_hc})")
        
        self.paciente_registrado_signal.emit()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.txt_cc.clear()
        self.txt_nombre.clear()
        self.txt_apellido.clear()
        self.txt_direccion.clear()
        self.txt_telefono.clear()
        self.txt_email.clear()
        self.txt_telefono_ref.clear()
        self.date_nacimiento.setDate(QDate.currentDate())
        
        # Limpiar Anamnesis
        if hasattr(self, 'txt_motivo'):
            self.txt_motivo.clear()
            self.txt_enfermedad.clear()
            self.txt_ant_personales.clear()
            self.txt_ant_familiares.clear()
            self.txt_alergias.clear()
            
        self.txt_cc.setFocus()