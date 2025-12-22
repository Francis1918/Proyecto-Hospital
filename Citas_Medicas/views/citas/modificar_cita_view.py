from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox
)

class ModificarCitaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Modificar Cita")
        self.setFixedSize(350, 300)

        layout = QVBoxLayout()

        self.txt_id = QLineEdit()
        self.txt_fecha = QLineEdit()
        self.txt_hora = QLineEdit()

        btn_fecha = QPushButton("Modificar Fecha")
        btn_hora = QPushButton("Modificar Hora")
        btn_ambos = QPushButton("Modificar Fecha y Hora")

        btn_fecha.clicked.connect(self.modificar_fecha)
        btn_hora.clicked.connect(self.modificar_hora)
        btn_ambos.clicked.connect(self.modificar_ambos)

        layout.addWidget(QLabel("ID Cita"))
        layout.addWidget(self.txt_id)
        layout.addWidget(QLabel("Nueva Fecha"))
        layout.addWidget(self.txt_fecha)
        layout.addWidget(QLabel("Nueva Hora"))
        layout.addWidget(self.txt_hora)

        layout.addWidget(btn_fecha)
        layout.addWidget(btn_hora)
        layout.addWidget(btn_ambos)

        self.setLayout(layout)

    def modificar_fecha(self):
        if self.controller.modificar_cita_fecha(
            int(self.txt_id.text()), self.txt_fecha.text()):
            QMessageBox.information(self, "Éxito", "Fecha modificada")
            self.close()

    def modificar_hora(self):
        if self.controller.modificar_cita_hora(
            int(self.txt_id.text()), self.txt_hora.text()):
            QMessageBox.information(self, "Éxito", "Hora modificada")
            self.close()

    def modificar_ambos(self):
        if self.controller.modificar_cita_fecha_hora(
            int(self.txt_id.text()),
            self.txt_fecha.text(),
            self.txt_hora.text()):
            QMessageBox.information(self, "Éxito", "Fecha y hora modificadas")
            self.close()
