from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QTabWidget, 
    QFrame, QFormLayout, QLineEdit, QTextEdit, 
    QCheckBox, QMessageBox, QHeaderView, QAbstractItemView, QScrollArea
)
from PyQt6.QtCore import Qt, QSize

# --- IMPORTACIONES DEL NÚCLEO ---
from core.theme import AppPalette, get_sheet, STYLES
from core.utils import get_icon

# Reutilizar el mismo diálogo de Historia Clínica del módulo Pacientes
from Pacientes.paciente_controller import PacienteController
from Pacientes.dialogs.historia_clinica_dialog import HistoriaClinicaDialog

class ConsultaExternaView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.init_ui()

    def _wrap_in_scroll(self, content: QWidget) -> QScrollArea:
        """Envuelve una vista en un scroll vertical para pantallas pequeñas."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(content)
        return scroll

    def set_controller(self, controller):
        self.controller = controller
        # Conectar señales después de que el controller está seteado
        self.btn_guardar_signos.clicked.connect(self.controller.guardar_signos_vitales)
        self.btn_actualizar_tabla.clicked.connect(self.controller.cargar_signos_vitales_en_vista)
        self.controller.cargar_signos_vitales_en_vista()


    def init_ui(self):
        # 1. APLICAMOS EL TEMA GLOBAL
        self.setStyleSheet(get_sheet())

        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        # --- HEADER (Estilo Tarjeta) ---
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppPalette.white_02}; 
                border-radius: 8px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        icon_lbl = QLabel()
        icon_pixmap = get_icon("clipboard.svg", color=AppPalette.Primary, size=40).pixmap(40, 40)
        icon_lbl.setPixmap(icon_pixmap)
        
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        
        lbl_titulo = QLabel("Consulta Externa")
        lbl_titulo.setObjectName("h1")
        
        lbl_sub = QLabel("Atención ambulatoria, triaje y diagnóstico médico.")
        lbl_sub.setStyleSheet(f"color: {AppPalette.black_02}; font-size: 14px;")
        
        title_layout.addWidget(lbl_titulo)
        title_layout.addWidget(lbl_sub)

        # 3. Ensamblaje
        header_layout.addWidget(icon_lbl)
        header_layout.addSpacing(15)
        header_layout.addWidget(title_container)
        header_layout.addStretch()

        self.layout_principal.addWidget(header_frame)

        # 2. CONFIGURACIÓN DE PESTAÑAS CON ICONOS
        self.tabs = QTabWidget()
        self.tabs.setIconSize(QSize(20, 20))
        
        self.setup_tab_enfermera()
        self.setup_tab_medico()
        
        self.layout_principal.addWidget(self.tabs)


    # =======================================================
    # PESTAÑA 1: REGISTRO DE SIGNOS VITALES
    # =======================================================
    def setup_tab_enfermera(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # --- FORMULARIO DE REGISTRO DE SIGNOS VITALES (CARD) ---
        container_signos = QFrame()
        container_signos.setStyleSheet(STYLES["card"])
        layout_signos = QVBoxLayout(container_signos)
        
        lbl_titulo_signos = QLabel("Registro de Signos Vitales")
        lbl_titulo_signos.setObjectName("h2")
        layout_signos.addWidget(lbl_titulo_signos)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setContentsMargins(20, 20, 20, 20)
        form.setSpacing(15)
        
        self.in_cc_paciente = QLineEdit()
        self.in_cc_paciente.setPlaceholderText("Cédula de Identidad del Paciente")
        self.in_cc_paciente.setMinimumHeight(30)
        self.in_cc_paciente.setStyleSheet("padding: 5px;")
        
        self.in_peso = QLineEdit()
        self.in_peso.setPlaceholderText("kg")
        self.in_peso.setMinimumHeight(30)
        self.in_peso.setStyleSheet("padding: 5px;")
        
        self.in_talla = QLineEdit()
        self.in_talla.setPlaceholderText("metros")
        self.in_talla.setMinimumHeight(30)
        self.in_talla.setStyleSheet("padding: 5px;")
        
        self.in_presion = QLineEdit()
        self.in_presion.setPlaceholderText("ej. 120/80")
        self.in_presion.setMinimumHeight(30)
        self.in_presion.setStyleSheet("padding: 5px;")
        
        self.in_motivo = QTextEdit()
        self.in_motivo.setMaximumHeight(80)
        self.in_motivo.setPlaceholderText("Motivo de la consulta o comentarios...")
        self.in_motivo.setStyleSheet("padding: 5px;")

        form.addRow("Cédula Paciente:", self.in_cc_paciente)
        form.addRow("Peso:", self.in_peso)
        form.addRow("Talla:", self.in_talla)
        form.addRow("Presión:", self.in_presion)
        form.addRow("Motivo:", self.in_motivo)
        
        layout_signos.addLayout(form)
        
        self.btn_guardar_signos = QPushButton(" Guardar Signos Vitales")
        self.btn_guardar_signos.setIcon(get_icon("save.svg", color="white"))
        self.btn_guardar_signos.setStyleSheet(STYLES["btn_primary"])
        self.btn_guardar_signos.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar_signos.setMinimumHeight(40)
        
        layout_signos.addWidget(self.btn_guardar_signos)
        
        layout.addWidget(container_signos)

        # --- TABLA DE REGISTROS DE SIGNOS VITALES ---
        container_tabla = QFrame()
        container_tabla.setStyleSheet(STYLES["card"])
        layout_tabla = QVBoxLayout(container_tabla)
        
        lbl_titulo_tabla = QLabel("Registros de Signos Vitales")
        lbl_titulo_tabla.setObjectName("h2")
        layout_tabla.addWidget(lbl_titulo_tabla)

        # Crear tabla
        self.tabla_signos_vitales = QTableWidget()
        self.tabla_signos_vitales.setColumnCount(11)
        self.tabla_signos_vitales.setHorizontalHeaderLabels([
            "ID", "Cédula", "Paciente", "Peso (kg)", 
            "Talla (m)", "Presión", "Motivo", "Fecha/Hora",
            "Código CIE-10", "Observaciones", "Plan Tratamiento"
        ])
        
        # Configuración de la tabla
        self.tabla_signos_vitales.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_signos_vitales.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla_signos_vitales.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        # Ajustar columnas
        header = self.tabla_signos_vitales.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        
        # Estilo de la tabla
        self.tabla_signos_vitales.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {AppPalette.white_02};
                border-radius: 4px;
                gridline-color: {AppPalette.white_02};
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: {AppPalette.Focus_Bg};
                color: {AppPalette.Primary};
            }}
            QHeaderView::section {{
                background-color: {AppPalette.white_02};
                padding: 8px;
                border: none;
                font-weight: bold;
                color: {AppPalette.black_01};
            }}
        """)
        
        layout_tabla.addWidget(self.tabla_signos_vitales)

        # Evita que la tabla se vea demasiado aplastada en ventanas pequeñas
        self.tabla_signos_vitales.setMinimumHeight(260)
        
        # Botón para actualizar tabla
        self.btn_actualizar_tabla = QPushButton(" Actualizar Registros")
        self.btn_actualizar_tabla.setIcon(get_icon("activity.svg", color=AppPalette.Primary))
        self.btn_actualizar_tabla.setStyleSheet(STYLES["btn_icon_ghost"])
        self.btn_actualizar_tabla.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_actualizar_tabla.setMinimumHeight(35)
        
        layout_tabla.addWidget(self.btn_actualizar_tabla)
        
        layout.addWidget(container_tabla)

        # Añadir pestaña con icono
        icon_heartbeat = get_icon("activity.svg", color=AppPalette.black_02)
        self.tabs.addTab(self._wrap_in_scroll(content), icon_heartbeat, "Signos Vitales")

    # =======================================================
    # PESTAÑA 2: MÉDICO (Atención)
    # =======================================================
    def setup_tab_medico(self):
        content = QWidget()
        layout = QVBoxLayout(content)
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
        
        self.lbl_paciente = QLabel("Ingrese la Cédula del Paciente para comenzar la atención médica.")
        self.lbl_paciente.setStyleSheet(f"color: {AppPalette.Primary}; font-weight: bold; font-size: 15px;")
        
        self.in_cedula_medico = QLineEdit()
        self.in_cedula_medico.setPlaceholderText("Cédula del Paciente")
        self.in_cedula_medico.setMinimumHeight(30)
        self.in_cedula_medico.setStyleSheet("padding: 5px;")

        btn_hc = QPushButton(" Ver Historia Clínica")
        btn_hc.setIcon(get_icon("file-text.svg", color=AppPalette.black_02))
        btn_hc.setStyleSheet(STYLES["btn_icon_ghost"])
        btn_hc.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_hc.clicked.connect(self.ver_hc)

        info_layout.addWidget(self.lbl_paciente)
        info_layout.addWidget(self.in_cedula_medico)
        info_layout.addWidget(btn_hc)
        
        layout.addWidget(info_frame)

        # --- AREA DE TRABAJO (2 COLUMNAS) ---
        work_area = QHBoxLayout()
        work_area.setStretch(0, 1)
        work_area.setStretch(1, 1)
        
        # 1. Diagnóstico
        card_diag = QFrame()
        card_diag.setStyleSheet(STYLES["card"])
        l_diag = QVBoxLayout(card_diag)
        l_diag.addWidget(QLabel("Diagnóstico (CIE-10)", objectName="h2"))
        
        f_diag = QFormLayout()
        self.in_cie10 = QLineEdit()
        self.in_cie10.setPlaceholderText("Código CIE-10")
        self.in_cie10.setStyleSheet("padding: 5px;")
        
        self.in_obs = QLineEdit()
        self.in_obs.setPlaceholderText("Observaciones del diagnóstico")
        self.in_obs.setStyleSheet("padding: 5px;")
        
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
        self.in_meds.setStyleSheet("padding: 5px;")
        l_rec.addWidget(self.in_meds)
        
        # Checkboxes con funcionalidad automática
        check_layout = QHBoxLayout()
        self.chk_laboratorio = QCheckBox("Laboratorio")
        self.chk_eco = QCheckBox("Ecografía")
        self.chk_tomo = QCheckBox("Tomografía")
        
        # Conectar checkboxes para actualizar automáticamente el plan de tratamiento
        self.chk_laboratorio.stateChanged.connect(self.actualizar_plan_tratamiento)
        self.chk_eco.stateChanged.connect(self.actualizar_plan_tratamiento)
        self.chk_tomo.stateChanged.connect(self.actualizar_plan_tratamiento)
        
        check_layout.addWidget(self.chk_laboratorio)
        check_layout.addWidget(self.chk_eco)
        check_layout.addWidget(self.chk_tomo)
        l_rec.addLayout(check_layout)
        
        work_area.addWidget(card_diag)
        work_area.addWidget(card_receta)
        layout.addLayout(work_area)

        # --- BOTÓN FINALIZAR ---
        btn_final = QPushButton(" Finalizar Atención y Guardar Diagnóstico")
        btn_final.setIcon(get_icon("save.svg", color="white"))
        btn_final.setStyleSheet(STYLES["btn_primary"])
        btn_final.setMinimumHeight(45)
        btn_final.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_final.clicked.connect(self.finalizar_atencion)
        
        layout.addWidget(btn_final)

        icon_doc = get_icon("clipboard.svg", color=AppPalette.black_02)
        self.tabs.addTab(self._wrap_in_scroll(content), icon_doc, "Consulta Médica")

    # =======================================================
    # LÓGICA - PESTAÑA SIGNOS VITALES
    # =======================================================
    def get_valores_signos_vitales(self):
        """Devuelve un diccionario con los valores de los campos de entrada."""
        return {
            "cedula": self.in_cc_paciente.text(),
            "peso": self.in_peso.text(),
            "talla": self.in_talla.text(),
            "presion": self.in_presion.text(),
            "motivo": self.in_motivo.toPlainText(),
        }

    def limpiar_campos_signos_vitales(self):
        """Limpia todos los campos de entrada del formulario."""
        self.in_cc_paciente.clear()
        self.in_peso.clear()
        self.in_talla.clear()
        self.in_presion.clear()
        self.in_motivo.clear()
        self.in_cc_paciente.setFocus()

    def actualizar_tabla_signos_vitales(self, registros):
        """Actualiza la tabla con los registros de signos vitales"""
        self.tabla_signos_vitales.setRowCount(0)  # Limpiar tabla
        
        for row_idx, registro in enumerate(registros):
            self.tabla_signos_vitales.insertRow(row_idx)
            # (id, cedula, nombre_paciente, peso, talla, presion, motivo, fecha_registro, 
            #  codigo_cie10, observaciones, plan_tratamiento)
            self.tabla_signos_vitales.setItem(row_idx, 0, QTableWidgetItem(str(registro[0]))) # ID
            self.tabla_signos_vitales.setItem(row_idx, 1, QTableWidgetItem(registro[1])) # Cedula
            self.tabla_signos_vitales.setItem(row_idx, 2, QTableWidgetItem(registro[2])) # Paciente
            self.tabla_signos_vitales.setItem(row_idx, 3, QTableWidgetItem(str(registro[3]))) # Peso
            self.tabla_signos_vitales.setItem(row_idx, 4, QTableWidgetItem(str(registro[4]))) # Talla
            self.tabla_signos_vitales.setItem(row_idx, 5, QTableWidgetItem(registro[5])) # Presion
            self.tabla_signos_vitales.setItem(row_idx, 6, QTableWidgetItem(registro[6] if registro[6] else "")) # Motivo
            self.tabla_signos_vitales.setItem(row_idx, 7, QTableWidgetItem(str(registro[7]))) # Fecha
            self.tabla_signos_vitales.setItem(row_idx, 8, QTableWidgetItem(registro[8] if registro[8] else "")) # CIE-10
            self.tabla_signos_vitales.setItem(row_idx, 9, QTableWidgetItem(registro[9] if registro[9] else "")) # Observaciones
            self.tabla_signos_vitales.setItem(row_idx, 10, QTableWidgetItem(registro[10] if registro[10] else "")) # Plan


    # =======================================================
    # LÓGICA - PESTAÑA MÉDICO
    # =======================================================
    def actualizar_plan_tratamiento(self):
        """Actualiza automáticamente el plan de tratamiento cuando se marcan los checkboxes"""
        plan_actual = self.in_meds.toPlainText().strip()
        
        # Lista de órdenes médicas seleccionadas
        ordenes = []
        if self.chk_laboratorio.isChecked():
            ordenes.append("- Orden de LABORATORIO")
        if self.chk_eco.isChecked():
            ordenes.append("- Orden de ECOGRAFÍA")
        if self.chk_tomo.isChecked():
            ordenes.append("- Orden de TOMOGRAFÍA")
        
        # Si hay medicamentos ya escritos, agregar las órdenes al final
        if ordenes:
            # Verificar si ya hay órdenes en el texto
            lineas_plan = plan_actual.split('\n')
            # Filtrar las líneas que no son órdenes
            lineas_sin_ordenes = [l for l in lineas_plan if not l.strip().startswith('- Orden de')]
            
            # Reconstruir el plan
            nuevo_plan = '\n'.join(lineas_sin_ordenes).strip()
            
            if nuevo_plan:
                nuevo_plan += '\n\n'
            
            nuevo_plan += '\n'.join(ordenes)
            
            self.in_meds.setPlainText(nuevo_plan)

    def ver_hc(self):
        cedula = self.in_cedula_medico.text().strip()
        if not cedula:
            QMessageBox.warning(self, "Alerta", "Ingrese la cédula del paciente para ver la Historia Clínica.")
            return

        paciente_controller = PacienteController()
        paciente = paciente_controller.consultar_paciente(cedula)
        if not paciente:
            QMessageBox.warning(self, "No encontrado", f"No se encontró un paciente con cédula {cedula}.")
            return

        dlg = HistoriaClinicaDialog(paciente_controller, self, paciente=paciente)
        dlg.exec()

    def finalizar_atencion(self):
        cedula = self.in_cedula_medico.text().strip()
        if not cedula:
            QMessageBox.warning(self, "Alerta", "Ingrese la cédula del paciente para finalizar la atención.")
            return

        cie10 = self.in_cie10.text().strip()
        observaciones = self.in_obs.text().strip()
        plan_tratamiento = self.in_meds.toPlainText().strip()

        # Registrar Diagnóstico
        exito, mensaje = self.controller.registrar_diagnostico(cedula, cie10, observaciones, plan_tratamiento)
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            # Limpiar formulario médico
            self.lbl_paciente.setText("Ingrese la Cédula del Paciente para comenzar la atención médica.")
            self.in_cedula_medico.clear()
            self.in_cie10.clear()
            self.in_obs.clear()
            self.in_meds.clear()
            self.chk_laboratorio.setChecked(False)
            self.chk_eco.setChecked(False)
            self.chk_tomo.setChecked(False)
            
            # Actualizar tabla de signos vitales
            self.controller.cargar_signos_vitales_en_vista()
        else:
            QMessageBox.warning(self, "Error", mensaje)