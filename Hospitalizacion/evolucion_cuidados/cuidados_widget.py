from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel
from core.theme import AppPalette as HospitalPalette #

class CuidadosWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        lbl_titulo = QLabel("Registro de Cuidados y Signos Vitales")
        lbl_titulo.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {HospitalPalette.Primary};")
        
        form = QFormLayout()
        self.input_presion = QLineEdit()
        self.input_temperatura = QLineEdit()
        self.input_frecuencia = QLineEdit()
        
        form.addRow("Presión Arterial:", self.input_presion)
        form.addRow("Temperatura (°C):", self.input_temperatura)
        form.addRow("Frecuencia Cardíaca:", self.input_frecuencia)
        
        self.btn_registrar = QPushButton("Registrar Signos")
        self.btn_registrar.setStyleSheet(f"background-color: {HospitalPalette.Primary}; color: white; padding: 8px;")
        
        layout.addWidget(lbl_titulo)
        layout.addLayout(form)
        layout.addWidget(self.btn_registrar)
        layout.addStretch()