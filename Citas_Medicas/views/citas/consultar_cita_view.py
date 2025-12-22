from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel
)

class ConsultarCitaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Consultar Citas")
        self.setFixedSize(600, 350)

        layout = QVBoxLayout()
        citas = self.controller.consultar_citas()

        if not citas:
            layout.addWidget(QLabel("No hay citas registradas"))
        else:
            tabla = QTableWidget()
            tabla.setRowCount(len(citas))
            tabla.setColumnCount(5)
            tabla.setHorizontalHeaderLabels(
                ["ID", "Paciente", "Fecha", "Hora", "Motivo"]
            )

            for fila, cita in enumerate(citas):
                tabla.setItem(fila, 0, QTableWidgetItem(str(cita.id_cita)))
                tabla.setItem(fila, 1, QTableWidgetItem(cita.paciente))
                tabla.setItem(fila, 2, QTableWidgetItem(cita.fecha))
                tabla.setItem(fila, 3, QTableWidgetItem(cita.hora))
                tabla.setItem(fila, 4, QTableWidgetItem(cita.motivo))

            tabla.resizeColumnsToContents()
            layout.addWidget(tabla)

        self.setLayout(layout)
