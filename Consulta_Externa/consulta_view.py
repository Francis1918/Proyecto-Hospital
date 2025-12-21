from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QTabWidget, 
                             QGroupBox, QFormLayout, QLineEdit, QTextEdit, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt

class ConsultaExternaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.cita_seleccionada = None
        self.init_ui()

    def init_ui(self):
        self.layout_principal = QVBoxLayout(self)
        self.setStyleSheet("""
                /* Regla General: Fondo claro y TEXTO OSCURO */
                QWidget { 
                    background-color: #f8fafc;
                    color: #2d3748;  /* <--- ESTA ES LA LÍNEA CLAVE */
                    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                }

                /* Regla Específica para Botones: Fondo degradado y texto BLANCO */
                QPushButton { 
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
                    color: white; /* Esto sobrescribe el color oscuro general solo para botones */
                    border-radius: 8px; 
                    padding: 10px; 
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5a67d8, stop:1 #6b46c1);
                }

                /* Estilos para otros elementos para mejorar la definición */
                QGroupBox { 
                    font-weight: bold; 
                    border: 1px solid #cbd5e0; 
                    border-radius: 8px; 
                    margin-top: 10px; 
                    padding: 15px; 
                }
                QTableWidget { 
                    border: 1px solid #e2e8f0; 
                    border-radius: 5px; 
                    background: white;
                    gridline-color: #e2e8f0;
                }
                QHeaderView::section {
                    background-color: #edf2f7;
                    padding: 5px;
                    border: none;
                    font-weight: bold;
                    color: #4a5568;
                }
                QLineEdit, QTextEdit {
                    border: 1px solid #e2e8f0;
                    border-radius: 4px;
                    padding: 5px;
                    background: white; /* Asegura fondo blanco para campos de entrada */
                }
            """)

        self.tabs = QTabWidget()
        self.setup_tab_enfermera()
        self.setup_tab_medico()
        
        self.layout_principal.addWidget(self.tabs)

    def setup_tab_enfermera(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 1. Caso de uso: consultarAgenda
        layout.addWidget(QLabel("<h3>Agenda Médica del Día</h3>"))
        self.tabla_agenda = QTableWidget(0, 4)
        self.tabla_agenda.setHorizontalHeaderLabels(["ID Cita", "Paciente", "Hora", "Estado"])
        self.tabla_agenda.itemSelectionChanged.connect(self.seleccionar_cita)
        layout.addWidget(self.tabla_agenda)
        self.cargar_agenda()

        # 2. Caso de uso: registrarAnamnesis
        grupo = QGroupBox("Registrar Anamnesis (Triaje)")
        form = QFormLayout()
        self.in_peso = QLineEdit(); self.in_talla = QLineEdit()
        self.in_presion = QLineEdit(); self.in_motivo = QTextEdit()
        form.addRow("Peso (kg):", self.in_peso)
        form.addRow("Talla (m):", self.in_talla)
        form.addRow("Presión:", self.in_presion)
        form.addRow("Motivo:", self.in_motivo)
        
        btn = QPushButton("Guardar Anamnesis")
        btn.clicked.connect(self.guardar_anamnesis)
        
        layout_grupo = QVBoxLayout()
        layout_grupo.addLayout(form); layout_grupo.addWidget(btn)
        grupo.setLayout(layout_grupo)
        layout.addWidget(grupo)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "👨‍⚕️ Área Enfermería")

    def setup_tab_medico(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 1. Caso de uso: consultarHistoriaClínica
        layout.addWidget(QLabel("<h3>Consulta Médica Activa</h3>"))
        self.lbl_paciente = QLabel("Paciente: Seleccione en Agenda")
        layout.addWidget(self.lbl_paciente)
        
        btn_hc = QPushButton("Consultar Historia Clínica")
        btn_hc.clicked.connect(self.ver_hc)
        layout.addWidget(btn_hc)

        # 2. Caso de uso: registrarDiagnóstico
        grupo_diag = QGroupBox("Diagnóstico (CIE-10)")
        f_diag = QFormLayout()
        self.in_cie10 = QLineEdit()
        self.in_obs = QLineEdit()
        f_diag.addRow("Código CIE-10:", self.in_cie10)
        f_diag.addRow("Observaciones:", self.in_obs)
        grupo_diag.setLayout(f_diag)
        layout.addWidget(grupo_diag)

        # 3. Caso de uso: emitirReceta + <<extend>>
        grupo_receta = QGroupBox("Receta y Órdenes Adicionales")
        f_rec = QFormLayout()
        self.in_meds = QTextEdit()
        f_rec.addRow("Medicamentos:", self.in_meds)
        
        self.chk_ex = QCheckBox("Pedido de Exámenes"); self.chk_eco = QCheckBox("Pedido Eco"); self.chk_tomo = QCheckBox("Pedido Tomografía")
        
        btn_final = QPushButton("Finalizar Atención y Emitir Receta")
        btn_final.clicked.connect(self.finalizar_atencion)

        l_receta = QVBoxLayout()
        l_receta.addLayout(f_rec); l_receta.addWidget(self.chk_ex); l_receta.addWidget(self.chk_eco); l_receta.addWidget(self.chk_tomo); l_receta.addWidget(btn_final)
        grupo_receta.setLayout(l_receta)
        layout.addWidget(grupo_receta)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "🩺 Área Médica")

    # --- Lógica de Interfaz ---
    def cargar_agenda(self):
        agenda = self.controller.consultar_agenda()
        self.tabla_agenda.setRowCount(len(agenda))
        for i, cita in enumerate(agenda):
            self.tabla_agenda.setItem(i, 0, QTableWidgetItem(cita["id_cita"]))
            self.tabla_agenda.setItem(i, 1, QTableWidgetItem(cita["paciente"]))
            self.tabla_agenda.setItem(i, 2, QTableWidgetItem(cita["hora"]))
            self.tabla_agenda.setItem(i, 3, QTableWidgetItem(cita["estado"]))

    def seleccionar_cita(self):
        row = self.tabla_agenda.currentRow()
        if row >= 0:
            self.cita_seleccionada = self.tabla_agenda.item(row, 0).text()
            nombre = self.tabla_agenda.item(row, 1).text()
            self.lbl_paciente.setText(f"Paciente: {nombre} (Cita: {self.cita_seleccionada})")

    def guardar_anamnesis(self):
        datos = {'peso': self.in_peso.text(), 'talla': self.in_talla.text(), 
                 'presion': self.in_presion.text(), 'motivo': self.in_motivo.toPlainText()}
        exito, msg = self.controller.registrar_anamnesis(self.cita_seleccionada, datos)
        if exito:
            QMessageBox.information(self, "Éxito", msg)
            self.cargar_agenda()
        else:
            QMessageBox.warning(self, "Error", msg)

    def ver_hc(self):
        if not self.cita_seleccionada: return
        hc = self.controller.consultar_historia_clinica("CC-Simulada")
        QMessageBox.information(self, "Historia Clínica", hc)

    def finalizar_atencion(self):
        # Primero registrar diagnóstico
        d_exito, d_msg = self.controller.registrar_diagnostico(self.cita_seleccionada, self.in_cie10.text(), self.in_obs.text())
        if not d_exito:
            QMessageBox.warning(self, "Error", d_msg); return

        # Luego emitir receta con extensiones
        extras = []
        if self.chk_ex.isChecked(): extras.append("Exámenes")
        if self.chk_eco.isChecked(): extras.append("Econosografía")
        if self.chk_tomo.isChecked(): extras.append("Tomografía")
        
        r_exito, r_msg = self.controller.emitir_receta(self.cita_seleccionada, {"meds": self.in_meds.toPlainText()}, extras)
        QMessageBox.information(self, "Atención Finalizada", r_msg)
        self.cargar_agenda()