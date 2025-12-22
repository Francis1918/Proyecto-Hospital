from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox

class DischargeWidget(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<h2>Registrar Alta de Paciente</h2>"))
        self.txt_cedula = QLineEdit()
        self.txt_cedula.setPlaceholderText("Cédula del Paciente") # [cite: 164]
        
        self.txt_motivo_alta = QLineEdit()
        self.txt_motivo_alta.setPlaceholderText("Motivo de Alta") # [cite: 167]
        
        self.btn_submit = QPushButton("Confirmar Alta")
        self.btn_submit.clicked.connect(self.process_discharge)

        layout.addWidget(QLabel("Cédula:"))
        layout.addWidget(self.txt_cedula)
        layout.addWidget(QLabel("Motivo de Alta:"))
        layout.addWidget(self.txt_motivo_alta)
        layout.addWidget(self.btn_submit)
        layout.addStretch()

    def process_discharge(self):
        res = self.controller.registrar_alta(self.txt_cedula.text(), self.txt_motivo_alta.text())
        QMessageBox.information(self, "Resultado", res)