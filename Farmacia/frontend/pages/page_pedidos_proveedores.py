from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import pyqtSignal
from Farmacia.backend.logic_farmacia import LogicaFarmacia

class WidgetPedidosProveedores(QWidget):
    pedido_creado = pyqtSignal() # Señal para actualizar recepción

    def __init__(self):
        super().__init__()
        self.logic = LogicaFarmacia()
        self.items_actuales = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # --- CREAR PEDIDO ---
        group_crear = QGroupBox("Nuevo Pedido a Proveedor")
        layout_crear = QVBoxLayout()
        form_crear = QFormLayout()

        self.combo_prov = QComboBox()
        # Llenar proveedores al inicio y tal vez con un botón refresh?
        self.btn_reload_prov = QPushButton("↻")
        self.btn_reload_prov.setFixedSize(30, 25)
        self.btn_reload_prov.clicked.connect(self.cargar_proveedores)
        
        hbox_prov = QHBoxLayout()
        hbox_prov.addWidget(self.combo_prov)
        hbox_prov.addWidget(self.btn_reload_prov)
        
        form_crear.addRow("Seleccionar Proveedor:", hbox_prov)
        layout_crear.addLayout(form_crear)

        # Agregar Items
        hbox_item = QHBoxLayout()
        self.input_item_nom = QLineEdit()
        self.input_item_nom.setPlaceholderText("Nombre Producto")
        self.input_item_cant = QLineEdit()
        self.input_item_cant.setPlaceholderText("Cantidad")
        self.input_item_cant.setFixedWidth(80)
        btn_add_item = QPushButton("+")
        btn_add_item.clicked.connect(self.agregar_item_lista)
        
        hbox_item.addWidget(self.input_item_nom)
        hbox_item.addWidget(self.input_item_cant)
        hbox_item.addWidget(btn_add_item)
        layout_crear.addLayout(hbox_item)

        # Tabla temporal
        self.tabla_items = QTableWidget()
        self.tabla_items.setColumnCount(2)
        self.tabla_items.setHorizontalHeaderLabels(["Item", "Cant"])
        self.tabla_items.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_items.setFixedHeight(100)
        layout_crear.addWidget(self.tabla_items)

        btn_enviar = QPushButton("Generar Orden de Compra")
        btn_enviar.clicked.connect(self.enviar_pedido)
        btn_enviar.setStyleSheet("background-color: #667eea; color: white; font-weight: bold;")
        layout_crear.addWidget(btn_enviar)

        group_crear.setLayout(layout_crear)
        layout.addWidget(group_crear)

        # --- LISTADO HISTÓRICO ---
        layout.addWidget(QLabel("Pedidos a Proveedores (Enviados):"))
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(5)
        self.tabla_historial.setHorizontalHeaderLabels(["ID", "Fecha", "Proveedor", "Estado", "Detalle"])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla_historial)

        btn_refresh = QPushButton("Actualizar Lista")
        btn_refresh.clicked.connect(self.cargar_historial)
        layout.addWidget(btn_refresh)

        self.setLayout(layout)
        self.cargar_proveedores()
        self.cargar_historial()

    def cargar_proveedores(self):
        self.combo_prov.clear()
        provs = self.logic.obtener_proveedores() # [(id, nom, ...), ...]
        for p in provs:
            self.combo_prov.addItem(p[1], p[0]) # Texto=Nombre, Data=ID

    def agregar_item_lista(self):
        nom = self.input_item_nom.text()
        cant = self.input_item_cant.text()
        if nom and cant.isdigit():
            self.items_actuales.append({"nombre": nom, "cantidad": int(cant)})
            self.actualizar_tabla_items()
            self.input_item_nom.clear()
            self.input_item_cant.clear()
            self.input_item_nom.setFocus()
        else:
            QMessageBox.warning(self, "Error", "Nombre e items válidos requeridos")

    def actualizar_tabla_items(self):
        self.tabla_items.setRowCount(len(self.items_actuales))
        for i, item in enumerate(self.items_actuales):
            self.tabla_items.setItem(i, 0, QTableWidgetItem(item['nombre']))
            self.tabla_items.setItem(i, 1, QTableWidgetItem(str(item['cantidad'])))

    def enviar_pedido(self):
        idx = self.combo_prov.currentIndex()
        if idx == -1:
            QMessageBox.warning(self, "Error", "Seleccione proveedor")
            return

        id_prov = self.combo_prov.itemData(idx)
        
        ok, msg = self.logic.crear_pedido_proveedor(id_prov, self.items_actuales)
        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.items_actuales = []
            self.actualizar_tabla_items()
            self.cargar_historial()
            self.pedido_creado.emit() # Avisar a recepcion
        else:
            QMessageBox.warning(self, "Error", msg)

    def cargar_historial(self):
        pedidos = self.logic.consultar_pedidos()
        # Filtramos SOLO solicitante Farmacia
        pedidos_prov = [p for p in pedidos if p['solicitante'] == "Farmacia"]
        
        self.tabla_historial.setRowCount(len(pedidos_prov))
        for i, p in enumerate(pedidos_prov):
            self.tabla_historial.setItem(i, 0, QTableWidgetItem(str(p['id'])))
            self.tabla_historial.setItem(i, 1, QTableWidgetItem(str(p['fecha'])))
            self.tabla_historial.setItem(i, 2, QTableWidgetItem(p['referencia'])) # Aquí guardamos "Proveedor: Nombre"
            self.tabla_historial.setItem(i, 3, QTableWidgetItem(p['estado']))
            self.tabla_historial.setItem(i, 4, QTableWidgetItem(p['items']))
