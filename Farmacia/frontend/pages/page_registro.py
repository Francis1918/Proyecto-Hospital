from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, 
    QDateEdit, QComboBox, QMessageBox, QTabWidget
)
from PyQt6.QtCore import QDate, pyqtSignal
from Farmacia.backend.logic_farmacia import LogicaFarmacia

class WidgetRegistro(QWidget):
    inventario_actualizado = pyqtSignal() # Señal para avisar a otros widgets

    def __init__(self):
        super().__init__()
        self.logic = LogicaFarmacia()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # --- SECCIÓN PROVEEDORES ---
        group_prov = QGroupBox("Registrar Proveedor")
        form_prov = QFormLayout()
        self.input_prov_nombre = QLineEdit()
        self.input_prov_contacto = QLineEdit()
        self.input_prov_tel = QLineEdit()
        self.input_prov_direccion = QLineEdit()
        btn_reg_prov = QPushButton("Registrar Proveedor")
        btn_reg_prov.clicked.connect(self.registrar_proveedor)
        btn_reg_prov.setStyleSheet("background-color: #48bb78; color: white; font-weight: bold;")
        
        form_prov.addRow("Nombre:", self.input_prov_nombre)
        form_prov.addRow("Contacto:", self.input_prov_contacto)
        form_prov.addRow("Teléfono:", self.input_prov_tel)
        form_prov.addRow("Dirección:", self.input_prov_direccion)
        form_prov.addRow(btn_reg_prov)
        group_prov.setLayout(form_prov)
        layout.addWidget(group_prov)

        # --- SECCIÓN INVENTARIO ---
        group_med = QGroupBox("Registrar Producto en Inventario")
        form_med = QFormLayout()
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Medicamento", "Insumo"])
        self.combo_tipo.currentIndexChanged.connect(self.cambiar_formulario)

        self.input_med_nombre = QLineEdit()
        self.input_med_desc = QLineEdit()
        self.input_med_stock = QLineEdit()
        self.input_med_stock.setPlaceholderText("Cantidad inicial")
        
        self.input_med_fecha = QDateEdit()
        self.input_med_fecha.setDisplayFormat("yyyy-MM-dd")
        self.input_med_fecha.setDate(QDate.currentDate())
        
        # Campos específicos
        self.input_med_presentacion = QLineEdit() # Solo medicamento
        self.input_med_receta = QComboBox() 
        self.input_med_receta.addItems(["No", "Sí"])
        
        self.input_insumo_material = QLineEdit() # Solo insumo

        btn_reg_med = QPushButton("Registrar Producto")
        btn_reg_med.clicked.connect(self.registrar_producto)
        btn_reg_med.setStyleSheet("background-color: #4299e1; color: white; font-weight: bold;")

        form_med.addRow("Tipo:", self.combo_tipo)
        form_med.addRow("Nombre:", self.input_med_nombre)
        form_med.addRow("Descripción:", self.input_med_desc)
        form_med.addRow("Stock Inicial:", self.input_med_stock)
        form_med.addRow("Fecha Caducidad:", self.input_med_fecha)
        
        # Filas dinámicas (las guardamos para ocultar/mostrar)
        self.row_pres = form_med.addRow("Presentación:", self.input_med_presentacion)
        self.row_receta = form_med.addRow("Requiere Receta:", self.input_med_receta)
        self.row_mat = form_med.addRow("Tipo Material:", self.input_insumo_material)
        
        form_med.addRow(btn_reg_med)
        group_med.setLayout(form_med)
        layout.addWidget(group_med)

        self.setLayout(layout)
        self.cambiar_formulario() # Ajustar visibilidad inicial

    def cambiar_formulario(self):
        es_med = self.combo_tipo.currentText() == "Medicamento"
        self.input_med_presentacion.setVisible(es_med)
        self.input_med_receta.setVisible(es_med)
        
        # Etiquetas (labels) asociadas en FormLayout son trickies de ocultar
        # Accedemos al label del widget
        self.input_med_presentacion.parentWidget().layout().labelForField(self.input_med_presentacion).setVisible(es_med)
        self.input_med_receta.parentWidget().layout().labelForField(self.input_med_receta).setVisible(es_med)

        self.input_insumo_material.setVisible(not es_med)
        self.input_insumo_material.parentWidget().layout().labelForField(self.input_insumo_material).setVisible(not es_med)

    def registrar_proveedor(self):
        nombre = self.input_prov_nombre.text()
        contacto = self.input_prov_contacto.text()
        tel = self.input_prov_tel.text()
        direc = self.input_prov_direccion.text()
        
        ok, msg = self.logic.registrar_proveedor(nombre, contacto, tel, direc)
        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.input_prov_nombre.clear()
            self.input_prov_contacto.clear()
            self.input_prov_tel.clear()
            self.input_prov_direccion.clear()
        else:
            QMessageBox.warning(self, "Error", msg)

    def registrar_producto(self):
        tipo = self.combo_tipo.currentText()
        nombre = self.input_med_nombre.text()
        desc = self.input_med_desc.text()
        stock = self.input_med_stock.text()
        fecha = self.input_med_fecha.date().toString("yyyy-MM-dd")
        
        if tipo == "Medicamento":
            pres = self.input_med_presentacion.text()
            receta = self.input_med_receta.currentText() == "Sí"
            ok, msg = self.logic.registrar_medicamento(nombre, desc, stock, fecha, pres, receta)
        else:
            mat = self.input_insumo_material.text()
            ok, msg = self.logic.registrar_insumo(nombre, desc, stock, fecha, mat)

        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.input_med_nombre.clear()
            self.input_med_desc.clear()
            self.input_med_stock.clear()
            self.inventario_actualizado.emit()
        else:
            QMessageBox.warning(self, "Error", msg)
