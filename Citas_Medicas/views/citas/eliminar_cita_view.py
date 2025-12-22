from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox

class EliminarCitaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Eliminar Cita")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.txt_id = QLineEdit()
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar)

        layout.addWidget(QLabel("ID de la Cita"))
        layout.addWidget(self.txt_id)
        layout.addWidget(btn_eliminar)

        self.setLayout(layout)

    def eliminar(self):
        self.controller.eliminar_cita(int(self.txt_id.text()))
        QMessageBox.information(self, "Éxito", "Cita eliminada")
        self.close()
