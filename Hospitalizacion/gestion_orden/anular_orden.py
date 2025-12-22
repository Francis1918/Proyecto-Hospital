from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QPushButton, QMessageBox, QLabel
)
from .repository import repo_orden

class AnularOrdenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anular Orden Médica")
        self.resize(400, 150)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.combo_ordenes = QComboBox()
        self.refresh_combo()
        
        self.info_label = QLabel("Seleccione una orden para anular")
        self.combo_ordenes.currentIndexChanged.connect(self.mostrar_info)

        form.addRow("Seleccionar Orden", self.combo_ordenes)
        layout.addLayout(form)
        layout.addWidget(self.info_label)

        btn = QPushButton("Anular Orden")
        btn.setStyleSheet("background-color: #e53e3e; color: white; font-weight: bold;")
        btn.clicked.connect(self.anular)
        layout.addWidget(btn)
        
        self.mostrar_info()

    def refresh_combo(self):
        self.combo_ordenes.clear()
        todas = repo_orden.buscar_todas()
        for o in todas:
            if o.estado == "Activa":
                self.combo_ordenes.addItem(f"{o.id_orden} - {o.id_paciente}", o.id_orden)

    def mostrar_info(self):
        idx = self.combo_ordenes.currentIndex()
        if idx < 0: 
            self.info_label.setText("No hay órdenes activas.")
            return
        id_orden = self.combo_ordenes.itemData(idx)
        orden = repo_orden.buscar_por_id(id_orden)
        if orden:
            self.info_label.setText(f"Descripción: {orden.descripcion}")

    def anular(self):
        idx = self.combo_ordenes.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Error", "Seleccione una orden")
            return
        
        id_orden = self.combo_ordenes.itemData(idx)
        
        confirm = QMessageBox.question(
            self, "Confirmar", 
            f"¿Está seguro de anular la orden {id_orden}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            if repo_orden.anular_orden(id_orden):
                QMessageBox.information(self, "Éxito", "Orden anulada correctamente")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo anular la orden")
