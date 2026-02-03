"""
Vista principal del módulo de Médicos para integrarse con el sistema hospitalario.
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class MedicosView(QMainWindow):
    """
    Vista temporal del módulo de Médicos.
    TODO: Integrar con el módulo completo una vez se resuelvan las dependencias.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Médicos")
        
        # Widget central temporal
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Mensaje temporal
        label = QLabel("Módulo de Médicos")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1F2937;")
        layout.addWidget(label)
        
        info_label = QLabel("Este módulo está en desarrollo.\nLas funcionalidades completas se integrarán próximamente.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("font-size: 14px; color: #718096; margin-top: 10px; line-height: 1.5;")
        layout.addWidget(info_label)

