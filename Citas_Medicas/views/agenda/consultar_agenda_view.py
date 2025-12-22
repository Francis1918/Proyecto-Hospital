from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem
)

class ConsultarAgendaView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Agenda General")
        self.setFixedSize(650, 350)

        citas = self.controller.consultar_agenda()

        layout = QVBoxLayout()
        tabla = QTableWidget()

        tabla.setColumnCount(5)
        tabla.setHorizontalHeaderLabels(
            ["ID", "Paciente", "Fecha", "Hora", "Motivo"]
        )
        tabla.setRowCount(len(citas))

        for fila, cita in enumerate(citas):
            tabla.setItem(fila, 0, QTableWidgetItem(str(cita.get('id', ''))))
            tabla.setItem(fila, 1, QTableWidgetItem(cita.get('paciente', '')))
            tabla.setItem(fila, 2, QTableWidgetItem(cita.get('fecha', '')))
            tabla.setItem(fila, 3, QTableWidgetItem(cita.get('hora', '')))
            tabla.setItem(fila, 4, QTableWidgetItem(cita.get('motivo', '')))

        tabla.resizeColumnsToContents()
        layout.addWidget(tabla)
        self.setLayout(layout)
