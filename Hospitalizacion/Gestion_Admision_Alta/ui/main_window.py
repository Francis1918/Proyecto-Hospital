from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget
)

from .admission_gui import AdmissionWidget
from .discharge_gui import DischargeWidget
from .views_gui import HistoryWidget, AvailabilityWidget

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Sistema de Gestión de Admisión y Alta")
        self.resize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Sidebar de navegación
        self.sidebar = QVBoxLayout()
        self.btn_ingreso = QPushButton("Registrar Ingreso")
        self.btn_alta = QPushButton("Registrar Alta")
        self.btn_historial = QPushButton("Consultar Historial")
        self.btn_dispo = QPushButton("Verificar Disponibilidad")
        
        for btn in [self.btn_ingreso, self.btn_alta, self.btn_historial, self.btn_dispo]:
            self.sidebar.addWidget(btn)
        self.sidebar.addStretch()
        self.layout.addLayout(self.sidebar, 1)

        # Contenedor de Vistas
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack, 4)

        self.init_views()
        self.btn_ingreso.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_alta.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_historial.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_dispo.clicked.connect(lambda: self.stack.setCurrentIndex(3))

    def init_views(self):
        self.stack.addWidget(AdmissionWidget(self.controller))
        self.stack.addWidget(DischargeWidget(self.controller))
        self.stack.addWidget(HistoryWidget(self.controller))
        self.stack.addWidget(AvailabilityWidget(self.controller))