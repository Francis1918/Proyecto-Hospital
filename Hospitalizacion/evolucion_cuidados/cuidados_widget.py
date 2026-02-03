from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QFrame
from core.theme import AppPalette as HospitalPalette

class CuidadosWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        grid_card = QFrame()
        grid_card.setStyleSheet(f"background-color: white; border: 1px solid {HospitalPalette.Border}; border-radius: 12px;")
        grid = QGridLayout(grid_card)
        grid.setContentsMargins(25, 25, 25, 25)
        grid.setSpacing(20)

        # Estilo común para etiquetas e inputs
        lbl_style = f"color: {HospitalPalette.text_secondary}; font-weight: bold; border: none;"
        input_style = "padding: 10px; border: 1px solid #cbd5e0; border-radius: 6px; color: #2d3748;"

        campos = [
            ("Frecuencia Cardíaca (bpm)", "60-100"),
            ("Presión Arterial (mmHg)", "120/80"),
            ("Saturación O2 (%)", "95-100"),
            ("Temperatura (°C)", "36.5")
        ]

        self.inputs = {}
        for i, (label, placeholder) in enumerate(campos):
            lbl = QLabel(label)
            lbl.setStyleSheet(lbl_style)
            txt = QLineEdit()
            txt.setPlaceholderText(placeholder)
            txt.setStyleSheet(input_style)
            
            grid.addWidget(lbl, i // 2, (i % 2) * 2)
            grid.addWidget(txt, i // 2, (i % 2) * 2 + 1)
            self.inputs[label] = txt

        self.btn_registrar = QPushButton("Registrar Signos Vitales")
        self.btn_registrar.setStyleSheet(f"background-color: {HospitalPalette.Success}; color: white; padding: 12px; font-weight: bold; border-radius: 6px;")
        
        layout.addWidget(grid_card)
        layout.addWidget(self.btn_registrar)
        layout.addStretch()