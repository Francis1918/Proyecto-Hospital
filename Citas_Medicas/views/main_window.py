from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Citas Médicas")
        self.setFixedSize(400, 300)

        central = QWidget()
        layout = QVBoxLayout()

        titulo = QLabel("Seleccione Rol")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_paciente = QPushButton("Paciente")
        self.btn_recepcionista = QPushButton("Recepcionista")
        self.btn_jefe = QPushButton("Jefe")

        layout.addWidget(titulo)
        layout.addWidget(self.btn_paciente)
        layout.addWidget(self.btn_recepcionista)
        layout.addWidget(self.btn_jefe)

        central.setLayout(layout)
        self.setCentralWidget(central)
