from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from .evolucion_widget import EvolucionWidget
from .cuidados_widget import CuidadosWidget
from core.theme import AppPalette as HospitalPalette

class EvolucionCuidadosView(QWidget):
    def __init__(self, parent_hospitalizacion):
        super().__init__()
        self.parent_hosp = parent_hospitalizacion
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header (sin botón de volver redundante)
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Título de sección con color oscuro para evitar letras blancas
        lbl_seccion = QLabel("Gestión de Evolución Médica y Cuidados")
        lbl_seccion.setStyleSheet(f"color: {HospitalPalette.black_01}; font-size: 20px; font-weight: bold;")
        layout.addWidget(lbl_seccion)

        # Sistema de Pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: 1px solid {HospitalPalette.Border}; border-radius: 8px; background: white; }}
            QTabBar::tab {{ padding: 12px 25px; background: #edf2f7; color: {HospitalPalette.black_02}; }}
            QTabBar::tab:selected {{ background: white; color: {HospitalPalette.Primary}; font-weight: bold; }}
        """)
        
        self.tabs.addTab(EvolucionWidget(), "Evolución Médica")
        self.tabs.addTab(CuidadosWidget(), "Cuidados de Enfermería")
        
        layout.addWidget(self.tabs)