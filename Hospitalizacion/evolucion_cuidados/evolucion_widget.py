from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFrame, QHBoxLayout, QInputDialog, QMessageBox
from core.theme import AppPalette as HospitalPalette
from .repository import repo_evolucion

class EvolucionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Contenedor tipo Tarjeta (Card)
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {HospitalPalette.Border};
                border-radius: 12px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)

        lbl_instruccion = QLabel("Resumen de Evolución Clínica")
        lbl_instruccion.setStyleSheet(f"color: {HospitalPalette.black_01}; font-size: 16px; font-weight: bold; border: none;")
        
        self.txt_evolucion = QTextEdit()
        self.txt_evolucion.setPlaceholderText("Ingrese observaciones, diagnósticos y cambios en el tratamiento...")
        self.txt_evolucion.setStyleSheet(f"""
            QTextEdit {{
                color: #2d3748;
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
            }}
            QTextEdit:focus {{ border: 2px solid {HospitalPalette.Primary}; }}
        """)

        # Barra de acciones inferior
        actions = QHBoxLayout()
        self.btn_guardar = QPushButton("Finalizar Registro")
        self.btn_guardar.setFixedWidth(180)
        self.btn_guardar.setStyleSheet(f"""
            QPushButton {{
                background-color: {HospitalPalette.Primary};
                color: white;
                font-weight: bold;
                padding: 12px;
                border-radius: 6px;
            }}
            QPushButton:hover {{ background-color: {HospitalPalette.hover}; }}
        """)
        actions.addStretch()
        actions.addWidget(self.btn_guardar)

        # Conectar guardado a repositorio
        self.btn_guardar.clicked.connect(self._on_guardar)

        card_layout.addWidget(lbl_instruccion)
        card_layout.addWidget(self.txt_evolucion)
        card_layout.addLayout(actions)
        
        layout.addWidget(card)
        layout.addStretch()

    def _on_guardar(self):
        texto = self.txt_evolucion.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Error", "Ingrese observaciones antes de guardar.")
            return
        cedula, ok = QInputDialog.getText(self, "Paciente", "Ingrese cédula del paciente:")
        if not ok or not cedula:
            return
        ok_save = repo_evolucion.registrar_evolucion(cedula.strip(), texto)
        if ok_save:
            QMessageBox.information(self, "Guardado", "Evolución registrada en la base de datos.")
            self.txt_evolucion.clear()
        else:
            QMessageBox.warning(self, "Error", "No se pudo registrar la evolución en la BD.")