from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox
)
from .repository import repo_orden

class ActualizarOrdenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Actualizar Orden Médica")
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Selección de orden por ID
        self.combo_ordenes = QComboBox()
        self.refresh_combo()
        self.combo_ordenes.currentIndexChanged.connect(self.cargar_datos)

        self.descripcion = QLineEdit()

        form.addRow("Seleccionar Orden", self.combo_ordenes)
        form.addRow("Nueva Descripción", self.descripcion)
        layout.addLayout(form)

        btn = QPushButton("Actualizar")
        btn.clicked.connect(self.actualizar)
        layout.addWidget(btn)
        
        # Cargar datos iniciales si hay
        self.cargar_datos()

    def refresh_combo(self):
        self.combo_ordenes.clear()
        todas = repo_orden.buscar_todas()
        for o in todas:
            # Solo mostrar activas si se desea, o todas. Para actualizar, mejor todas.
            self.combo_ordenes.addItem(f"{o.id_orden} - {o.id_paciente}", o.id_orden)

    def cargar_datos(self):
        idx = self.combo_ordenes.currentIndex()
        if idx < 0: return
        id_orden = self.combo_ordenes.itemData(idx)
        orden = repo_orden.buscar_por_id(id_orden)
        if orden:
            self.descripcion.setText(orden.descripcion)

    def actualizar(self):
        idx = self.combo_ordenes.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Error", "Seleccione una orden")
            return
        
        id_orden = self.combo_ordenes.itemData(idx)
        nueva_desc = self.descripcion.text().strip()
        
        if not nueva_desc:
            QMessageBox.warning(self, "Error", "La descripción no puede estar vacía")
            return

        if repo_orden.actualizar_orden(id_orden, nueva_desc):
            QMessageBox.information(self, "Éxito", "Orden actualizada correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar la orden")
