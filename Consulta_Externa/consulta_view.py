from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QTabWidget, 
    QFrame, QFormLayout, QLineEdit, QTextEdit, 
    QCheckBox, QMessageBox, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, QSize

# --- IMPORTACIONES DEL NÚCLEO ---
from core.theme import AppPalette, get_sheet, STYLES
from core.utils import get_icon

class ConsultaExternaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.cita_seleccionada = None
        self.init_ui()

    def init_ui(self):
        # 1. APLICAMOS EL TEMA GLOBAL
        self.setStyleSheet(get_sheet())

        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        # Encabezado del Módulo
        header = QLabel("Consulta Externa")
        header.setObjectName("h1")
        self.layout_principal.addWidget(header)

        # 2. CONFIGURACIÓN DE PESTAÑAS CON ICONOS
        self.tabs = QTabWidget()
        self.tabs.setIconSize(QSize(20, 20))
        
        self.setup_tab_enfermera()
        self.setup_tab_medico()
        
        self.layout_principal.addWidget(self.tabs)

    # =======================================================
    # PESTAÑA 1: ENFERMERÍA (Triaje)
    # =======================================================
    def setup_tab_enfermera(self):
        tab = QWidget()
        layout = QHBoxLayout(tab) # Usamos Horizontal para aprovechar pantalla ancha
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # --- COLUMNA IZQUIERDA: AGENDA ---
        col_izq = QVBoxLayout()
        
        lbl_agenda = QLabel("Agenda del Día")
        lbl_agenda.setObjectName("h2")
        col_izq.addWidget(lbl_agenda)

        self.tabla_agenda = QTableWidget(0, 4)
        self.tabla_agenda.setHorizontalHeaderLabels(["ID", "Paciente", "Hora", "Estado"])
        self.tabla_agenda.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_agenda.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_agenda.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_agenda.itemSelectionChanged.connect(self.seleccionar_cita)
        
        col_izq.addWidget(self.tabla_agenda)
        layout.addLayout(col_izq, stretch=60) # 60% del ancho

        # --- COLUMNA DERECHA: TRIAJE (CARD) ---
        container_triaje = QFrame()
        container_triaje.setStyleSheet(STYLES["card"])
        layout_triaje = QVBoxLayout(container_triaje)
        
        lbl_triaje = QLabel("Registrar Signos Vitales")
        lbl_triaje.setObjectName("h2")
        lbl_triaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_triaje.addWidget(lbl_triaje)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.in_peso = QLineEdit(); self.in_peso.setPlaceholderText("kg")
        self.in_talla = QLineEdit(); self.in_talla.setPlaceholderText("metros")
        self.in_presion = QLineEdit(); self.in_presion.setPlaceholderText("ej. 120/80")
        self.in_motivo = QTextEdit(); self.in_motivo.setMaximumHeight(80)

        form.addRow("Peso:", self.in_peso)
        form.addRow("Talla:", self.in_talla)
        form.addRow("Presión:", self.in_presion)
        form.addRow("Motivo:", self.in_motivo)
        
        layout_triaje.addLayout(form)
        
        btn_guardar = QPushButton(" Guardar Anamnesis")
        btn_guardar.setIcon(get_icon("save.svg", color="white"))
        btn_guardar.setStyleSheet(STYLES["btn_primary"])
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.clicked.connect(self.guardar_anamnesis)
        
        layout_triaje.addStretch()
        layout_triaje.addWidget(btn_guardar)
        
        layout.addWidget(container_triaje, stretch=40) # 40% del ancho
        
        # Añadir pestaña con icono
        icon_nurse = get_icon("activity.svg", color=AppPalette.black_02)
        self.tabs.addTab(tab, icon_nurse, "Área Enfermería")

    # =======================================================
    # PESTAÑA 2: MÉDICO (Atención)
    # =======================================================
    def setup_tab_medico(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # --- HEADER DEL PACIENTE ---
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppPalette.Focus_Bg}; 
                border: 1px solid {AppPalette.Primary}; 
                border-radius: 6px;
            }}
        """)
        info_layout = QHBoxLayout(info_frame)
        
        self.lbl_paciente = QLabel("Paciente no seleccionado")
        self.lbl_paciente.setStyleSheet(f"color: {AppPalette.Primary}; font-weight: bold; font-size: 15px;")
        
        btn_hc = QPushButton(" Ver Historia Clínica")
        btn_hc.setIcon(get_icon("file-text.svg", color=AppPalette.black_02))
        btn_hc.setStyleSheet(STYLES["btn_icon_ghost"])
        btn_hc.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_hc.clicked.connect(self.ver_hc)

        info_layout.addWidget(self.lbl_paciente)
        info_layout.addStretch()
        info_layout.addWidget(btn_hc)
        
        layout.addWidget(info_frame)

        # --- AREA DE TRABAJO (2 COLUMNAS) ---
        work_area = QHBoxLayout()
        
        # 1. Diagnóstico
        card_diag = QFrame()
        card_diag.setStyleSheet(STYLES["card"])
        l_diag = QVBoxLayout(card_diag)
        l_diag.addWidget(QLabel("Diagnóstico (CIE-10)", objectName="h2"))
        
        f_diag = QFormLayout()
        self.in_cie10 = QLineEdit()
        self.in_obs = QLineEdit()
        f_diag.addRow("Código:", self.in_cie10)
        f_diag.addRow("Observaciones:", self.in_obs)
        l_diag.addLayout(f_diag)
        l_diag.addStretch()
        
        # 2. Receta y Acciones
        card_receta = QFrame()
        card_receta.setStyleSheet(STYLES["card"])
        l_rec = QVBoxLayout(card_receta)
        l_rec.addWidget(QLabel("Plan Tratamiento", objectName="h2"))
        
        self.in_meds = QTextEdit()
        self.in_meds.setPlaceholderText("Medicamentos y posología...")
        l_rec.addWidget(self.in_meds)
        
        # Checkboxes
        check_layout = QHBoxLayout()
        self.chk_ex = QCheckBox("Laboratorio")
        self.chk_eco = QCheckBox("Ecografía")
        self.chk_tomo = QCheckBox("Tomografía")
        check_layout.addWidget(self.chk_ex)
        check_layout.addWidget(self.chk_eco)
        check_layout.addWidget(self.chk_tomo)
        l_rec.addLayout(check_layout)
        
        work_area.addWidget(card_diag)
        work_area.addWidget(card_receta)
        layout.addLayout(work_area)

        # --- BOTÓN FINALIZAR ---
        btn_final = QPushButton(" Finalizar Atención y Emitir Receta")
        btn_final.setIcon(get_icon("send.svg", color="white"))
        btn_final.setStyleSheet(STYLES["btn_primary"])
        btn_final.setMinimumHeight(45)
        btn_final.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_final.clicked.connect(self.finalizar_atencion)
        
        layout.addWidget(btn_final)

        icon_doc = get_icon("clipboard.svg", color=AppPalette.black_02)
        self.tabs.addTab(tab, icon_doc, "Consulta Médica")

    # =======================================================
    # LÓGICA (Mantenida igual pero adaptada a UI nueva)
    # =======================================================
    def cargar_agenda(self):
        agenda = self.controller.consultar_agenda()
        self.tabla_agenda.setRowCount(len(agenda))
        for i, cita in enumerate(agenda):
            self.tabla_agenda.setItem(i, 0, QTableWidgetItem(cita["id_cita"]))
            self.tabla_agenda.setItem(i, 1, QTableWidgetItem(cita["paciente"]))
            self.tabla_agenda.setItem(i, 2, QTableWidgetItem(cita["hora"]))
            
            # Colorear estado
            item_estado = QTableWidgetItem(cita["estado"])
            if cita["estado"] == "Pendiente":
                item_estado.setForeground(Qt.GlobalColor.darkYellow)
            elif cita["estado"] == "Atendido":
                item_estado.setForeground(Qt.GlobalColor.green)
            
            self.tabla_agenda.setItem(i, 3, item_estado)

    def seleccionar_cita(self):
        row = self.tabla_agenda.currentRow()
        if row >= 0:
            self.cita_seleccionada = self.tabla_agenda.item(row, 0).text()
            nombre = self.tabla_agenda.item(row, 1).text()
            # Actualizamos la etiqueta azul en la pestaña del médico
            self.lbl_paciente.setText(f"👤 Paciente: {nombre} | ID Cita: {self.cita_seleccionada}")
            
            # Sugerencia UX: Cambiar automáticamente a la pestaña de médico si es médico
            # self.tabs.setCurrentIndex(1) 

    def guardar_anamnesis(self):
        if not self.cita_seleccionada:
            QMessageBox.warning(self, "Alerta", "Seleccione una cita de la agenda primero.")
            return

        datos = {'peso': self.in_peso.text(), 'talla': self.in_talla.text(), 
                 'presion': self.in_presion.text(), 'motivo': self.in_motivo.toPlainText()}
        exito, msg = self.controller.registrar_anamnesis(self.cita_seleccionada, datos)
        if exito:
            QMessageBox.information(self, "Éxito", msg)
            self.cargar_agenda()
            # Limpiar campos
            self.in_peso.clear(); self.in_talla.clear(); self.in_presion.clear(); self.in_motivo.clear()
        else:
            QMessageBox.warning(self, "Error", msg)

    def ver_hc(self):
        if not self.cita_seleccionada: 
            QMessageBox.warning(self, "Alerta", "Seleccione un paciente de la agenda.")
            return
        hc = self.controller.consultar_historia_clinica("CC-Simulada")
        QMessageBox.information(self, "Historia Clínica", hc)

    def finalizar_atencion(self):
        if not self.cita_seleccionada:
            QMessageBox.warning(self, "Alerta", "No hay paciente en atención.")
            return

        # 1. Registrar Diagnóstico
        d_exito, d_msg = self.controller.registrar_diagnostico(self.cita_seleccionada, self.in_cie10.text(), self.in_obs.text())
        if not d_exito:
            QMessageBox.warning(self, "Error", d_msg); return

        # 2. Emitir Receta
        extras = []
        if self.chk_ex.isChecked(): extras.append("Exámenes")
        if self.chk_eco.isChecked(): extras.append("Econosografía")
        if self.chk_tomo.isChecked(): extras.append("Tomografía")
        
        r_exito, r_msg = self.controller.emitir_receta(self.cita_seleccionada, {"meds": self.in_meds.toPlainText()}, extras)
        
        QMessageBox.information(self, "Atención Finalizada", r_msg)
        self.cargar_agenda()
        
        # Limpiar formulario médico
        self.lbl_paciente.setText("Paciente no seleccionado")
        self.in_cie10.clear(); self.in_obs.clear(); self.in_meds.clear()
        self.chk_ex.setChecked(False); self.chk_eco.setChecked(False); self.chk_tomo.setChecked(False)
        self.cita_seleccionada = None