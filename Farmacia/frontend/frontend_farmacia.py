import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import QSize, Qt
from Medicos.frontend import theme 

# Ajuste de path para importar módulos hermanos/padres si es necesario
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(current_dir, "..", "..")
if root_path not in sys.path:
    sys.path.append(root_path)

# Importamos páginas - Usando ruta absoluta desde root para evitar líos de 'package'
from Farmacia.frontend.pages.page_registro import WidgetRegistro
from Farmacia.frontend.pages.page_pedidos_internos import WidgetPedidosInternos
from Farmacia.frontend.pages.page_pedidos_proveedores import WidgetPedidosProveedores
from Farmacia.frontend.pages.page_recepcion import WidgetRecepcion
from Farmacia.frontend.pages.page_caducidad import WidgetCaducidad

class VentanaFarmacia(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Hospitalario - Módulo de Farmacia")
        self.resize(1100, 750)
        
        # Aplicar tema
        self.setStyleSheet(theme.get_sheet())

        self.initUI()

    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")
        header_layout = QHBoxLayout(header)
        title = QLabel("💊  Gestión de Farmacia")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d3748;")
        header_layout.addWidget(title)
        layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #C2C7CB; background: white; border-radius: 5px; }
            QTabBar::tab { background: #E2E8F0; padding: 10px; border-radius: 4px; margin-right: 2px; }
            QTabBar::tab:selected { background: white; font-weight: bold; }
        """)

        # Instanciar páginas
        self.page_registro = WidgetRegistro()
        self.page_pedidos_int = WidgetPedidosInternos()
        self.page_pedidos_prov = WidgetPedidosProveedores()
        self.page_recepcion = WidgetRecepcion()
        self.page_caducidad = WidgetCaducidad()

        # Agregar tabs
        self.tabs.addTab(self.page_registro, "Registros e Inventario")
        self.tabs.addTab(self.page_pedidos_int, "Pedidos Internos")
        self.tabs.addTab(self.page_pedidos_prov, "Pedidos a Proveedores")
        self.tabs.addTab(self.page_recepcion, "Recepción")
        self.tabs.addTab(self.page_caducidad, "Control Caducidad")
        
        # Conectar señales entre pestañas si es necesario
        self.page_registro.inventario_actualizado.connect(self.actualizar_todo)
        self.page_pedidos_prov.pedido_creado.connect(self.actualizar_recepcion)

        layout.addWidget(self.tabs)

    def actualizar_todo(self):
        # Refrescar listados que dependan del inventario
        self.page_caducidad.cargar_datos()

    def actualizar_recepcion(self):
        self.page_recepcion.cargar_datos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = VentanaFarmacia()
    win.show()
    sys.exit(app.exec())
