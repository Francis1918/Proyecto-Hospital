from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
from core.theme import AppPalette as HospitalPalette #

class EvolucionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        lbl_titulo = QLabel("Evolución Médica Diaria")
        lbl_titulo.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {HospitalPalette.Primary};")
        
        self.txt_evolucion = QTextEdit()
        self.txt_evolucion.setPlaceholderText("Escriba aquí la evolución detallada del paciente...")
        
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Evolución")
        self.btn_guardar.setStyleSheet(f"background-color: {HospitalPalette.Success}; color: white; padding: 10px; border-radius: 5px;")
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_guardar)
        
        layout.addWidget(lbl_titulo)
        layout.addWidget(self.txt_evolucion)
        layout.addLayout(btn_layout)