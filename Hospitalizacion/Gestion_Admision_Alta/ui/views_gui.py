from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem

class AvailabilityWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Disponibilidad por Área</h2>"))
        
        self.area_input = QLineEdit()
        self.area_input.setPlaceholderText("Escriba el nombre del área") # [cite: 72]
        self.btn_check = QPushButton("Consultar Espacios")
        self.lbl_result = QLabel("-")

        self.btn_check.clicked.connect(self.check)
        layout.addWidget(self.area_input)
        layout.addWidget(self.btn_check)
        layout.addWidget(self.lbl_result)
        layout.addStretch()

    def check(self):
        espacios = self.controller.verificar_disponibilidad(self.area_input.text())
        self.lbl_result.setText(f"Espacios disponibles: {espacios}") # [cite: 74]

class HistoryWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Historial de Hospitalizaciones</h2>"))
        
        self.txt_cedula = QLineEdit()
        self.btn_search = QPushButton("Buscar Historial") # [cite: 83]
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Fecha", "Diagnóstico", "Estado"])

        self.btn_search.clicked.connect(self.search)
        layout.addWidget(self.txt_cedula)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.table)

    def search(self):
        cedula = self.txt_cedula.text()
        historial = self.controller.historiales.get(cedula, [])
        self.table.setRowCount(0)
        for row_data in historial:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, val in enumerate(row_data):
                self.table.setItem(row, i, QTableWidgetItem(val))