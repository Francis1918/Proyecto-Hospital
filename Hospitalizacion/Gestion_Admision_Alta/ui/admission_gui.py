from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QMessageBox

class AdmissionWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<h2>Registrar Ingreso de Paciente</h2>"))
        self.txt_cedula = QLineEdit()
        self.txt_cedula.setPlaceholderText("Ingrese Cédula del Paciente (10 dígitos)") # 
        
        self.txt_motivo = QLineEdit()
        self.txt_motivo.setPlaceholderText("Motivo de Ingreso") # [cite: 34]
        
        self.cb_area = QComboBox()
        self.cb_area.addItems(["General", "Cuidados Intensivos", "Pediatría"]) # [cite: 35]
        
        self.btn_submit = QPushButton("Registrar Ingreso")
        self.btn_submit.clicked.connect(self.process_admission)

        layout.addWidget(QLabel("Cédula:"))
        layout.addWidget(self.txt_cedula)
        layout.addWidget(QLabel("Motivo:"))
        layout.addWidget(self.txt_motivo)
        layout.addWidget(QLabel("Área:"))
        layout.addWidget(self.cb_area)
        layout.addWidget(self.btn_submit)
        layout.addStretch()

    def process_admission(self):
        res = self.controller.registrar_ingreso(
            self.txt_cedula.text(), 
            self.txt_motivo.text(), 
            self.cb_area.currentText()
        )
        QMessageBox.information(self, "Resultado", res)