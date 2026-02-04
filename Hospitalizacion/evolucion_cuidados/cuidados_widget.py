from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QFrame, QInputDialog, QMessageBox
from core.theme import AppPalette as HospitalPalette
from .repository import repo_evolucion

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
        lbl_style = f"color: {HospitalPalette.black_01}; font-weight: bold; border: none;"
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

        # Conectar registro a repositorio
        self.btn_registrar.clicked.connect(self._on_registrar)

    def _on_registrar(self):
        # pedir cédula del paciente
        cedula, ok = QInputDialog.getText(self, "Paciente", "Ingrese cédula del paciente:")
        if not ok or not cedula:
            return
        datos = {k: v.text().strip() for k, v in self.inputs.items()}
        # Guardar como texto simple (podría ser JSON)
        datos_str = "; ".join([f"{k}: {v}" for k, v in datos.items()])
        ok_save = repo_evolucion.registrar_evolucion(cedula.strip(), f"Signos vitales: {datos_str}")
        if ok_save:
            QMessageBox.information(self, "Guardado", "Signos vitales registrados en la base de datos.")
            for t in self.inputs.values():
                t.clear()
        else:
            QMessageBox.warning(self, "Error", "No se pudo registrar en la BD.")