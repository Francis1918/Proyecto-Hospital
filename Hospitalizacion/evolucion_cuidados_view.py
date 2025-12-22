import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

# =================================================================
# 1. CONTROLADOR (Lógica de Negocio basada en UML)
# =================================================================
class EvolucionController:
    def __init__(self):
        # Almacenamiento temporal (Cédula -> lista de eventos clínicos)
        self._historial_clinico = {}

    def consultar_paciente(self, cedula):
        """Caso de uso: buscarPaciente [cite: 537]"""
        # Validación de criterios [cite: 539, 543]
        if len(cedula) < 10 or not cedula.isdigit():
            return None
            
        # Simulación de respuesta si el paciente existe [cite: 540]
        return {"cc": cedula, "nombre": "Juan Pérez (Hospitalizado)", "estado": "hospitalizado"}

    def guardar_evolucion(self, cedula, texto, medico="Médico Responsable"):
        """Caso de uso: registrarEvolucionDiaria [cite: 476]"""
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tipo": "Evolución Médica",
            "personal": medico,
            "descripcion": texto
        }
        self._historial_clinico.setdefault(cedula, []).append(evento)
        return True

    def guardar_cuidados(self, cedula, procedimiento, observaciones, personal="Enfermería"):
        """Caso de uso: registrarCuidadosYProcedimientos [cite: 492]"""
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tipo": "Cuidado/Procedimiento",
            "personal": personal,
            "descripcion": f"{procedimiento}: {observaciones}"
        }
        self._historial_clinico.setdefault(cedula, []).append(evento)
        return True

    def obtener_historial(self, cedula):
        """Caso de uso: consultarEvolucionYCuidados [cite: 507, 510]"""
        return self._historial_clinico.get(cedula, [])

# =================================================================
# 2. VISTA (Interfaz Gráfica PyQt6)
# =================================================================
class EvolucionCuidadosView(QWidget):
    def __init__(self, rol="MEDICO", controller=None):
        super().__init__()
        self.rol = rol  # Puede ser "MEDICO" o "JEFE" según auth.py del repo
        self.controller = controller if controller else EvolucionController()
        self.paciente_actual = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sistema Hospitalario - Evolución y Cuidados")
        self.resize(900, 700)
        self.setStyleSheet("background-color: #f8fafc; font-family: 'Segoe UI';")
        
        layout_principal = QVBoxLayout(self)

        # SECCIÓN BÚSQUEDA (buscarPaciente [cite: 537])
        search_group = QGroupBox("Búsqueda de Paciente")
        search_layout = QHBoxLayout()
        self.txt_cedula = QLineEdit()
        self.txt_cedula.setPlaceholderText("Ingrese cédula de 10 dígitos...")
        btn_buscar = QPushButton("🔍 Buscar")
        btn_buscar.setStyleSheet("background-color: #3182ce; color: white; font-weight: bold; padding: 8px;")
        btn_buscar.clicked.connect(self.handler_buscar)
        
        search_layout.addWidget(self.txt_cedula)
        search_layout.addWidget(btn_buscar)
        search_group.setLayout(search_layout)
        layout_principal.addWidget(search_group)

        self.lbl_paciente = QLabel("Paciente: Ninguno seleccionado")
        self.lbl_paciente.setStyleSheet("font-weight: bold; color: #2c5282; margin: 10px;")
        layout_principal.addWidget(self.lbl_paciente)

        # PESTAÑAS (Roles definidos en UML [cite: 451, 453])
        self.tabs = QTabWidget()
        self.setup_tab_evolucion()
        self.setup_tab_cuidados()
        self.setup_tab_historial()
        
        layout_principal.addWidget(self.tabs)
        self.tabs.setEnabled(False) # Bloqueado hasta encontrar paciente

    def setup_tab_evolucion(self):
        """Pestaña Médico Responsable [cite: 451]"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.txt_evolucion = QTextEdit()
        btn_save = QPushButton("Guardar Evolución Diaria")
        btn_save.clicked.connect(self.handler_save_evolucion)
        
        layout.addWidget(QLabel("Nota Médica de Evolución:"))
        layout.addWidget(self.txt_evolucion)
        layout.addWidget(btn_save)
        
        # Restricción de rol según UML
        if self.rol != "JEFE": # En el repo, JEFE suele actuar como el rol superior médico
            tab.setEnabled(False)
            layout.addWidget(QLabel("⚠️ Acceso exclusivo para el Médico Responsable."))
            
        self.tabs.addTab(tab, "🩺 Evolución (Médico)")

    def setup_tab_cuidados(self):
        """Pestaña Personal de Enfermería [cite: 453]"""
        tab = QWidget()
        layout = QFormLayout(tab)
        self.txt_proc = QLineEdit()
        self.txt_obs = QTextEdit()
        btn_save = QPushButton("Registrar Procedimiento")
        btn_save.clicked.connect(self.handler_save_cuidados)
        
        layout.addRow("Procedimiento:", self.txt_proc)
        layout.addRow("Observaciones:", self.txt_obs)
        layout.addRow(btn_save)
        self.tabs.addTab(tab, "💉 Cuidados (Enfermería)")

    def setup_tab_historial(self):
        """Pestaña Consulta [cite: 507]"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Tipo", "Personal", "Descripción"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla)
        self.tabs.addTab(tab, "📚 Historial Clínico")

    # --- HANDLERS ---
    def handler_buscar(self):
        cedula = self.txt_cedula.text().strip()
        paciente = self.controller.consultar_paciente(cedula)
        
        if paciente:
            self.paciente_actual = paciente
            self.lbl_paciente.setText(f"Paciente: {paciente['nombre']} | Cédula: {paciente['cc']}")
            self.tabs.setEnabled(True)
            self.refresh_tabla()
        else:
            QMessageBox.critical(self, "Error", "Paciente no encontrado o cédula inválida [cite: 547]")
            self.tabs.setEnabled(False)

    def handler_save_evolucion(self):
        texto = self.txt_evolucion.toPlainText().strip()
        if len(texto) < 5:
            QMessageBox.warning(self, "Aviso", "Por favor, detalle la evolución clínica.")
            return
        self.controller.guardar_evolucion(self.paciente_actual['cc'], texto)
        QMessageBox.information(self, "Éxito", "Evolución registrada con éxito [cite: 482]")
        self.txt_evolucion.clear()
        self.refresh_tabla()

    def handler_save_cuidados(self):
        proc = self.txt_proc.text().strip()
        obs = self.txt_obs.toPlainText().strip()
        if not proc:
            return
        self.controller.guardar_cuidados(self.paciente_actual['cc'], proc, obs)
        QMessageBox.information(self, "Éxito", "Cuidados registrados con éxito [cite: 497]")
        self.txt_proc.clear(); self.txt_obs.clear()
        self.refresh_tabla()

    def refresh_tabla(self):
        eventos = self.controller.obtener_historial(self.paciente_actual['cc'])
        self.tabla.setRowCount(len(eventos))
        for i, ev in enumerate(eventos):
            self.tabla.setItem(i, 0, QTableWidgetItem(ev['fecha']))
            self.tabla.setItem(i, 1, QTableWidgetItem(ev['tipo']))
            self.tabla.setItem(i, 2, QTableWidgetItem(ev['personal']))
            self.tabla.setItem(i, 3, QTableWidgetItem(ev['descripcion']))

# =================================================================
# 3. BLOQUE DE EJECUCIÓN (Standalone)
# =================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ejemplo con rol de Médico (JEFE) para habilitar todas las funciones
    ventana = EvolucionCuidadosView(rol="JEFE")
    ventana.show()
    sys.exit(app.exec())