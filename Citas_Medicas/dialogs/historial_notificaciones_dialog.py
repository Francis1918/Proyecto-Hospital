from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QVBoxLayout
)

from ..citas_controller import CitasMedicasController


class HistorialNotificacionesDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Historial de Notificaciones")
        self.setModal(True)
        self.setMinimumWidth(820)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("📩 Historial de Notificaciones")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        btns = QHBoxLayout()
        btn_refrescar = QPushButton("Refrescar")
        btn_refrescar.clicked.connect(self._cargar)
        btns.addWidget(btn_refrescar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns.addWidget(btn_cerrar)
        layout.addLayout(btns)

        self.tabla = QTableWidget(0, 6) 
        self.tabla.setHorizontalHeaderLabels(["Fecha/Hora", "Tipo", "Nombre Destinatario", "ID/Cédula", "Canal", "Mensaje"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tabla)

        self._cargar()

    def _cargar(self):
        items = self.controller.obtener_historial_notificaciones()
        self.tabla.setRowCount(0)

        for n in items:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # Extraemos los datos del objeto
            vals = [
                n.enviada_en.strftime("%Y-%m-%d %H:%M"),
                getattr(n, 'tipo_usuario', 'N/A'),
                getattr(n, 'nombre_destinatario', 'No encontrado'),
                n.destinatario,
                n.canal,
                n.mensaje
            ]
            
            for col, v in enumerate(vals):
                item = QTableWidgetItem(str(v))
                # Opcional: Color según el tipo
                if col == 1: # Columna Tipo
                    if v == 'Médico': item.setForeground(Qt.GlobalColor.blue)
                    if v == 'Paciente': item.setForeground(Qt.GlobalColor.darkGreen)
                
                self.tabla.setItem(row, col, item)
