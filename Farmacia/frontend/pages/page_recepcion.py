from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, 
    QMessageBox, QLabel
)
from Farmacia.backend.logic_farmacia import LogicaFarmacia

class WidgetRecepcion(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = LogicaFarmacia()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Recepción de Pedidos de Proveedores"))
        layout.addWidget(QLabel("Ingrese el ID del pedido que ha llegado físicamente a Farmacia."))

        group_recep = QGroupBox("Confirmar Recepción")
        form = QFormLayout()
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID del Pedido")
        
        btn_confirm = QPushButton("Confirmar Recepción & Actualizar Stock")
        btn_confirm.clicked.connect(self.procesar_recepcion)
        btn_confirm.setStyleSheet("background-color: #9f7aea; color: white; font-weight: bold;")

        form.addRow("ID Pedido:", self.input_id)
        form.addRow(btn_confirm)
        group_recep.setLayout(form)
        
        layout.addWidget(group_recep)
        layout.addStretch()
        self.setLayout(layout)

    def cargar_datos(self):
        pass # Podríamos listar pedidos pendientes de recepción aquí

    def procesar_recepcion(self):
        pid = self.input_id.text()
        if not pid.isdigit():
            QMessageBox.warning(self, "Error", "Ingrese un ID numérico válido")
            return
            
        ok, msg = self.logic.recibir_pedido(int(pid))
        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.input_id.clear()
        else:
            QMessageBox.warning(self, "Error", msg)
