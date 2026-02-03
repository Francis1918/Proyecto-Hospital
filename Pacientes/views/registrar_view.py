from datetime import date
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QCheckBox, QDateEdit, QScrollArea, QFrame
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

        # Opciones Extra (Checkbox)
        self.chk_crear_historia = QCheckBox(" Crear Historia Clínica automáticamente al guardar")
        self.chk_crear_historia.setChecked(True)
        self.chk_crear_historia.setStyleSheet(f"font-size: 14px; color: {AppPalette.text_primary}; font-weight: bold;")
        self.layout_content.addWidget(self.chk_crear_historia)

        self.layout_content.addStretch() # Empuja todo hacia arriba
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # --- 3. BARRA DE ACCIONES INFERIOR (Fija) ---
        action_bar = QFrame()
        action_bar.setStyleSheet(f"background-color: {AppPalette.bg_sidebar}; border-top: 1px solid {AppPalette.Border};")
        bar_layout = QHBoxLayout(action_bar)
        bar_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botón Limpiar
        self.btn_limpiar = QPushButton(" Limpiar Formulario")
        self.btn_limpiar.setIcon(get_icon("refresh.svg", AppPalette.text_secondary))
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

    # --- LÓGICA DE NEGOCIO ---
    def guardar_paciente(self):
        # 1. Validaciones
        cc = self.txt_cc.text().strip()
        nombre = self.txt_nombre.text().strip()
        apellido = self.txt_apellido.text().strip()

        if not cc or not nombre or not apellido:
            QMessageBox.warning(self, "Campos Incompletos", "Los campos Cédula, Nombre y Apellido son obligatorios.")
            self.txt_cc.setFocus()
            return

        # 2. Crear Objeto
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

        # 3. Guardar en Base de Datos (Controller)
        exito, mensaje = self.controller.registrar_paciente(paciente)

        if not exito:
            QMessageBox.warning(self, "Error", mensaje)
            return

        # 4. Procesos opcionales (Historia Clínica)
        msg_extra = ""
        if self.chk_crear_historia.isChecked():
            ok_hist, txt_hist = self.controller.crear_historia_clinica(paciente.cc)
            if ok_hist:
                msg_extra = f"\n- {txt_hist}"
            else:
                msg_extra = f"\n- (Ojo) {txt_hist}"

        # 5. Confirmación Exitosa
        QMessageBox.information(self, "Registro Exitoso", 
                              f"Paciente {nombre} {apellido} guardado correctamente.{msg_extra}")
        
        # 6. Emitir señal para actualizar otras vistas
        self.paciente_registrado_signal.emit()

        # 7. Preguntar por Anamnesis (Flujo original)
        resp = QMessageBox.question(
            self, "Registrar Anamnesis",
            "¿Desea registrar los antecedentes (Anamnesis) ahora?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if resp == QMessageBox.StandardButton.Yes:
            # Abrimos el diálogo de anamnesis existente (Pop-up)
            dlg = RegistrarAnamnesisDilaog(self.controller, self)
            dlg.txt_cc.setText(paciente.cc)
            dlg.buscar_paciente() # Auto-buscar
            dlg.exec()
        
        # Limpiamos todo para el siguiente
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
        self.txt_cc.setFocus()