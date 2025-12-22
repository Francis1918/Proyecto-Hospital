import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QFormLayout, QMessageBox, QDateEdit, QComboBox,
    QHeaderView, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt, QDate
from Farmacia.logica_farmacia import SistemaFarmacia

class VentanaFarmacia(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaFarmacia()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema Hospitalario - Módulo de Farmacia")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(self.get_styles())

        # Widget principal y Layout
        main_widget = QWidget()
        main_widget.setObjectName("central")
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        
        titulo_icon = QLabel("💊")
        titulo_icon.setStyleSheet("font-size: 32px;")
        header_layout.addWidget(titulo_icon)
        
        titulo = QLabel("Gestión de Farmacia")
        titulo.setObjectName("titulo")
        header_layout.addWidget(titulo)
        header_layout.addStretch()
        
        layout.addWidget(header)

        # Pestañas
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Crear pestañas
        self.tab_registro = QWidget()
        self.tab_pedidos_internos = QWidget()
        self.tab_pedidos_proveedores = QWidget()
        self.tab_recepcion = QWidget()
        self.tab_caducidad = QWidget()

        self.tabs.addTab(self.tab_registro, "Registros e Inventario")
        self.tabs.addTab(self.tab_pedidos_internos, "Pedidos Internos")
        self.tabs.addTab(self.tab_pedidos_proveedores, "Pedidos a Proveedores")
        self.tabs.addTab(self.tab_recepcion, "Recepción")
        self.tabs.addTab(self.tab_caducidad, "Control Caducidad")

        # Inicializar contenido de pestañas
        self.init_tab_registro()
        self.init_tab_pedidos_internos()
        self.init_tab_pedidos_proveedores()
        self.init_tab_recepcion()
        self.init_tab_caducidad()

    def get_styles(self):
        """Retorna los estilos CSS para la aplicación, consistentes con el menú principal."""
        return """
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2
                );
            }
            QWidget#central {
                background: transparent;
            }
            QFrame#header {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QLabel {
                color: #2d3748;
            }
            QLabel#titulo {
                color: #2d3748;
                font-size: 24px;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 1px solid #C2C7CB;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.7);
                color: #2d3748;
                border: 1px solid #C4C4C3;
                border-bottom-color: #C2C7CB;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 8px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #4a5568;
                border-color: #9B9B9B;
                border-bottom-color: white; 
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid gray;
                border-radius: 5px;
                margin-top: 10px;
                background-color: rgba(255, 255, 255, 0.5);
                color: #2d3748;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                color: #2d3748;
            }
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2
                );
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4c51bf, stop:1 #553c9a
                );
            }
            QLineEdit, QDateEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                color: #2d3748;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #ccc;
                color: #2d3748;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #ccc;
                font-weight: bold;
                color: #2d3748;
            }
        """

    # --- PESTAÑA 1: REGISTROS E INVENTARIO ---
    def init_tab_registro(self):
        layout = QVBoxLayout()
        
        # Grupo Proveedor
        group_prov = QGroupBox("Registrar Proveedor")
        form_prov = QFormLayout()
        self.input_prov_nombre = QLineEdit()
        self.input_prov_contacto = QLineEdit()
        self.input_prov_direccion = QLineEdit()
        btn_reg_prov = QPushButton("Registrar Proveedor")
        btn_reg_prov.clicked.connect(self.registrar_proveedor)
        
        form_prov.addRow("Nombre:", self.input_prov_nombre)
        form_prov.addRow("Contacto:", self.input_prov_contacto)
        form_prov.addRow("Dirección:", self.input_prov_direccion)
        form_prov.addRow(btn_reg_prov)
        group_prov.setLayout(form_prov)
        layout.addWidget(group_prov)

        # Grupo Medicamento
        group_med = QGroupBox("Registrar Medicamento")
        form_med = QFormLayout()
        self.input_med_nombre = QLineEdit()
        self.input_med_desc = QLineEdit()
        self.input_med_cant = QLineEdit()
        self.input_med_fecha = QDateEdit()
        self.input_med_fecha.setDisplayFormat("yyyy-MM-dd")
        self.input_med_fecha.setDate(QDate.currentDate())
        self.input_med_presentacion = QLineEdit()
        self.input_med_receta = QComboBox()
        self.input_med_receta.addItems(["Sí", "No"])
        btn_reg_med = QPushButton("Registrar Medicamento")
        btn_reg_med.clicked.connect(self.registrar_medicamento)

        form_med.addRow("Nombre:", self.input_med_nombre)
        form_med.addRow("Descripción:", self.input_med_desc)
        form_med.addRow("Cantidad Inicial:", self.input_med_cant)
        form_med.addRow("Fecha Caducidad:", self.input_med_fecha)
        form_med.addRow("Presentación:", self.input_med_presentacion)
        form_med.addRow("Requiere Receta:", self.input_med_receta)
        form_med.addRow(btn_reg_med)
        group_med.setLayout(form_med)
        layout.addWidget(group_med)

        self.tab_registro.setLayout(layout)

    def registrar_proveedor(self):
        nombre = self.input_prov_nombre.text()
        contacto = self.input_prov_contacto.text()
        direccion = self.input_prov_direccion.text()
        if nombre and contacto:
            msg = self.sistema.registrarProveedor(nombre, contacto, direccion)
            QMessageBox.information(self, "Éxito", msg)
            self.input_prov_nombre.clear()
            self.input_prov_contacto.clear()
            self.input_prov_direccion.clear()
            self.actualizar_combos_proveedores()
        else:
            QMessageBox.warning(self, "Error", "Nombre y Contacto son obligatorios")

    def registrar_medicamento(self):
        try:
            nombre = self.input_med_nombre.text()
            desc = self.input_med_desc.text()
            cant = int(self.input_med_cant.text())
            fecha = self.input_med_fecha.date().toString("yyyy-MM-dd")
            pres = self.input_med_presentacion.text()
            receta = self.input_med_receta.currentText() == "Sí"
            
            if nombre:
                msg = self.sistema.registrarMedicamento(nombre, desc, cant, fecha, pres, receta)
                QMessageBox.information(self, "Éxito", msg)
                self.input_med_nombre.clear()
                self.input_med_desc.clear()
                self.input_med_cant.clear()
                self.actualizar_tablas_inventario()
            else:
                QMessageBox.warning(self, "Error", "El nombre es obligatorio")
        except ValueError:
            QMessageBox.warning(self, "Error", "La cantidad debe ser un número entero")

    # --- PESTAÑA 2: PEDIDOS INTERNOS ---
    def init_tab_pedidos_internos(self):
        layout = QVBoxLayout()
        
        group_pedido = QGroupBox("Nuevo Pedido Interno (Medicamentos)")
        form = QFormLayout()
        self.input_pi_solicitante = QLineEdit()
        self.input_pi_depto = QLineEdit()
        self.input_pi_items = QLineEdit()
        self.input_pi_items.setPlaceholderText("Ej: Paracetamol:10, Ibuprofeno:5")
        btn_pi = QPushButton("Crear Pedido Interno")
        btn_pi.clicked.connect(self.crear_pedido_interno)
        
        form.addRow("Solicitante (Médico/Enfermero):", self.input_pi_solicitante)
        form.addRow("Departamento:", self.input_pi_depto)
        form.addRow("Items (Nombre:Cant, ...):", self.input_pi_items)
        form.addRow(btn_pi)
        group_pedido.setLayout(form)
        layout.addWidget(group_pedido)

        self.table_pedidos_internos = QTableWidget()
        self.table_pedidos_internos.setColumnCount(5)
        self.table_pedidos_internos.setHorizontalHeaderLabels(["ID", "Fecha", "Solicitante", "Depto", "Estado"])
        self.table_pedidos_internos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(QLabel("Listado de Pedidos Internos:"))
        layout.addWidget(self.table_pedidos_internos)

        self.tab_pedidos_internos.setLayout(layout)

    def crear_pedido_interno(self):
        solicitante = self.input_pi_solicitante.text()
        depto = self.input_pi_depto.text()
        items_str = self.input_pi_items.text()
        
        if solicitante and items_str:
            items = []
            try:
                for part in items_str.split(','):
                    nombre, cant = part.split(':')
                    items.append({'nombre_medicamento': nombre.strip(), 'cantidad': int(cant.strip())})
                
                msg = self.sistema.elaborarPedidoMedicamentos(solicitante, depto, items)
                QMessageBox.information(self, "Éxito", msg)
                self.actualizar_tabla_pedidos_internos()
            except ValueError:
                QMessageBox.warning(self, "Error", "Formato de items incorrecto. Use: Nombre:Cantidad")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")

    def actualizar_tabla_pedidos_internos(self):
        pedidos = self.sistema.consultarPedidosMedicamentos()
        self.table_pedidos_internos.setRowCount(len(pedidos))
        for i, p in enumerate(pedidos):
            self.table_pedidos_internos.setItem(i, 0, QTableWidgetItem(str(p.id_pedido)))
            self.table_pedidos_internos.setItem(i, 1, QTableWidgetItem(str(p.fecha_creacion)))
            self.table_pedidos_internos.setItem(i, 2, QTableWidgetItem(p.solicitante))
            self.table_pedidos_internos.setItem(i, 3, QTableWidgetItem(p.departamento))
            self.table_pedidos_internos.setItem(i, 4, QTableWidgetItem(p.estado))

    # --- PESTAÑA 3: PEDIDOS A PROVEEDORES ---
    def init_tab_pedidos_proveedores(self):
        layout = QVBoxLayout()
        
        group_pp = QGroupBox("Nuevo Pedido a Proveedor")
        form = QFormLayout()
        self.combo_proveedores = QComboBox()
        self.input_pp_items = QLineEdit()
        self.input_pp_items.setPlaceholderText("Ej: Paracetamol:500")
        btn_pp = QPushButton("Generar Pedido a Proveedor")
        btn_pp.clicked.connect(self.crear_pedido_proveedor)
        
        form.addRow("Proveedor:", self.combo_proveedores)
        form.addRow("Items (Nombre:Cant):", self.input_pp_items)
        form.addRow(btn_pp)
        group_pp.setLayout(form)
        layout.addWidget(group_pp)

        self.table_pedidos_prov = QTableWidget()
        self.table_pedidos_prov.setColumnCount(5)
        self.table_pedidos_prov.setHorizontalHeaderLabels(["ID", "Fecha", "Proveedor", "Items", "Estado"])
        self.table_pedidos_prov.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(QLabel("Pedidos a Proveedores:"))
        layout.addWidget(self.table_pedidos_prov)
        
        # Botones de acción
        hbox = QHBoxLayout()
        btn_del = QPushButton("Eliminar Seleccionado")
        btn_del.clicked.connect(self.eliminar_pedido_proveedor)
        hbox.addWidget(btn_del)
        layout.addLayout(hbox)

        self.tab_pedidos_proveedores.setLayout(layout)

    def actualizar_combos_proveedores(self):
        self.combo_proveedores.clear()
        for p in self.sistema.proveedores:
            self.combo_proveedores.addItem(p.nombre, p.id_proveedor)

    def crear_pedido_proveedor(self):
        idx = self.combo_proveedores.currentIndex()
        if idx == -1:
            QMessageBox.warning(self, "Error", "Seleccione un proveedor")
            return
            
        id_prov = self.combo_proveedores.itemData(idx)
        items_str = self.input_pp_items.text()
        
        if items_str:
            items = []
            try:
                for part in items_str.split(','):
                    nombre, cant = part.split(':')
                    items.append({'nombre': nombre.strip(), 'cantidad': int(cant.strip())})
                
                msg = self.sistema.elaborarPedidoDeMedicamentosAProveedor(id_prov, items)
                QMessageBox.information(self, "Éxito", msg)
                self.actualizar_tabla_pedidos_proveedores()
            except ValueError:
                QMessageBox.warning(self, "Error", "Formato incorrecto")
        else:
             QMessageBox.warning(self, "Error", "Ingrese items")

    def actualizar_tabla_pedidos_proveedores(self):
        pedidos = self.sistema.pedidos_proveedores_medicamentos
        self.table_pedidos_prov.setRowCount(len(pedidos))
        for i, p in enumerate(pedidos):
            self.table_pedidos_prov.setItem(i, 0, QTableWidgetItem(str(p.id_pedido)))
            self.table_pedidos_prov.setItem(i, 1, QTableWidgetItem(str(p.fecha_creacion)))
            self.table_pedidos_prov.setItem(i, 2, QTableWidgetItem(p.proveedor.nombre))
            items_str = ", ".join([f"{x['nombre']}:{x['cantidad']}" for x in p.items])
            self.table_pedidos_prov.setItem(i, 3, QTableWidgetItem(items_str))
            self.table_pedidos_prov.setItem(i, 4, QTableWidgetItem(p.estado))

    def eliminar_pedido_proveedor(self):
        row = self.table_pedidos_prov.currentRow()
        if row >= 0:
            id_pedido = int(self.table_pedidos_prov.item(row, 0).text())
            try:
                msg = self.sistema.eliminarPedidoDeProveedor(id_pedido)
                QMessageBox.information(self, "Info", msg)
                self.actualizar_tabla_pedidos_proveedores()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "Seleccione un pedido")

    # --- PESTAÑA 4: RECEPCIÓN ---
    def init_tab_recepcion(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.input_recep_id = QLineEdit()
        btn_recep = QPushButton("Registrar Recepción")
        btn_recep.clicked.connect(self.registrar_recepcion)
        
        form.addRow("ID Pedido a recibir:", self.input_recep_id)
        form.addRow(btn_recep)
        layout.addLayout(form)
        
        self.tab_recepcion.setLayout(layout)

    def registrar_recepcion(self):
        try:
            id_pedido = int(self.input_recep_id.text())
            msg = self.sistema.registrarRecepcionPedido(id_pedido)
            QMessageBox.information(self, "Resultado", msg)
            self.actualizar_tabla_pedidos_proveedores()
            self.actualizar_tablas_inventario()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    # --- PESTAÑA 5: CADUCIDAD ---
    def init_tab_caducidad(self):
        layout = QVBoxLayout()
        
        hbox_filter = QHBoxLayout()
        self.combo_cad_filtro = QComboBox()
        self.combo_cad_filtro.addItems(["Próximos (30 días)", "Vencidos", "Todos"])
        btn_check = QPushButton("Consultar")
        btn_check.clicked.connect(self.consultar_caducidad)
        
        hbox_filter.addWidget(QLabel("Filtro:"))
        hbox_filter.addWidget(self.combo_cad_filtro)
        hbox_filter.addWidget(btn_check)
        layout.addLayout(hbox_filter)
        
        self.table_caducidad = QTableWidget()
        self.table_caducidad.setColumnCount(3)
        self.table_caducidad.setHorizontalHeaderLabels(["Producto", "Fecha Caducidad", "Días Restantes"])
        self.table_caducidad.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_caducidad)
        
        self.tab_caducidad.setLayout(layout)

    def consultar_caducidad(self):
        filtro_map = {
            "Próximos (30 días)": "proximos",
            "Vencidos": "vencidos",
            "Todos": "todos"
        }
        filtro_txt = self.combo_cad_filtro.currentText()
        filtro_val = filtro_map.get(filtro_txt, "proximos")
        
        lista = self.sistema.consultarCaducidad(tipo="todos", filtro=filtro_val)
        self.table_caducidad.setRowCount(len(lista))
        hoy = QDate.currentDate().toPyDate()
        
        for i, med in enumerate(lista):
            fecha_cad = datetime.datetime.strptime(med.fecha_caducidad, "%Y-%m-%d").date()
            dias = (fecha_cad - hoy).days
            
            self.table_caducidad.setItem(i, 0, QTableWidgetItem(med.nombre))
            self.table_caducidad.setItem(i, 1, QTableWidgetItem(med.fecha_caducidad))
            self.table_caducidad.setItem(i, 2, QTableWidgetItem(str(dias)))

    # --- HELPERS ---
    def actualizar_tablas_inventario(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    ventana = VentanaFarmacia()
    ventana.show()
    sys.exit(app.exec())
