from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox, QHBoxLayout
)
from Farmacia.backend.logic_farmacia import LogicaFarmacia

class WidgetPedidosInternos(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = LogicaFarmacia()
        self.items_actuales = [] # Lista temporal para el pedido en curso
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # --- CREAR PEDIDO ---
        group_crear = QGroupBox("Nuevo Pedido Interno")
        layout_crear = QVBoxLayout()
        form_crear = QFormLayout()

        self.input_solicitante = QLineEdit()
        self.input_depto = QLineEdit()
        
        form_crear.addRow("Solicitante:", self.input_solicitante)
        form_crear.addRow("Departamento:", self.input_depto)
        layout_crear.addLayout(form_crear)

        # Agregar Items
        hbox_item = QHBoxLayout()
        self.input_item_nom = QLineEdit()
        self.input_item_nom.setPlaceholderText("Nombre Medicamento/Insumo")
        self.input_item_cant = QLineEdit()
        self.input_item_cant.setPlaceholderText("Cantidad")
        self.input_item_cant.setFixedWidth(80)
        btn_add_item = QPushButton("+")
        btn_add_item.clicked.connect(self.agregar_item_lista)
        
        hbox_item.addWidget(self.input_item_nom)
        hbox_item.addWidget(self.input_item_cant)
        hbox_item.addWidget(btn_add_item)
        layout_crear.addLayout(hbox_item)

        # Tabla temporal de items
        self.tabla_items = QTableWidget()
        self.tabla_items.setColumnCount(2)
        self.tabla_items.setHorizontalHeaderLabels(["Item", "Cant"])
        self.tabla_items.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_items.setFixedHeight(100)
        layout_crear.addWidget(self.tabla_items)

        btn_enviar = QPushButton("Crear Pedido")
        btn_enviar.clicked.connect(self.enviar_pedido)
        btn_enviar.setStyleSheet("background-color: #ed8936; color: white; font-weight: bold;")
        layout_crear.addWidget(btn_enviar)

        group_crear.setLayout(layout_crear)
        layout.addWidget(group_crear)

        # --- LISTADO HISTÓRICO ---
        layout.addWidget(QLabel("Historial de Pedidos Internos:"))
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(5)
        self.tabla_historial.setHorizontalHeaderLabels(["ID", "Fecha", "Solicitante", "Estado", "Detalle"])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla_historial)

        btn_refresh = QPushButton("Actualizar Lista")
        btn_refresh.clicked.connect(self.cargar_historial)
        layout.addWidget(btn_refresh)

        self.setLayout(layout)
        self.cargar_historial()

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
        sol = self.input_solicitante.text()
        dep = self.input_depto.text()
        
        ok, msg = self.logic.crear_pedido_interno(sol, dep, self.items_actuales)
        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.items_actuales = []
            self.actualizar_tabla_items()
            self.input_solicitante.clear()
            self.input_depto.clear()
            self.cargar_historial()
        else:
            QMessageBox.warning(self, "Error", msg)

    def cargar_historial(self):
        # Filtramos o mostramos todos? De momento todos los pedidos que no sean a proveedores
        # PERO logic.consultar_pedidos devuelve TODOS. 
        # La tabla pedidos_farmacia tiene campo 'solicitante'. Si es 'Farmacia' es pedido a proveedor (segunda logica).
        # Ajustemos Logica si es necesario o filtramos aquí.
        # En logic_farmacia.py: crear_pedido_proveedor pone solicitante="Farmacia".
        
        pedidos = self.logic.consultar_pedidos()
        # Filtramos lo que NO sea solicitante Farmacia (eso es a proveedores)
        pedidos_internos = [p for p in pedidos if p['solicitante'] != "Farmacia"]
        
        self.tabla_historial.setRowCount(len(pedidos_internos))
        for i, p in enumerate(pedidos_internos):
            self.tabla_historial.setItem(i, 0, QTableWidgetItem(str(p['id'])))
            self.tabla_historial.setItem(i, 1, QTableWidgetItem(str(p['fecha'])))
            self.tabla_historial.setItem(i, 2, QTableWidgetItem(p['solicitante']))
            self.tabla_historial.setItem(i, 3, QTableWidgetItem(p['estado']))
            self.tabla_historial.setItem(i, 4, QTableWidgetItem(p['items']))
