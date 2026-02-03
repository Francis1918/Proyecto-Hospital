import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import QSize, Qt
from core import theme
from core.utils import get_icon 

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
        # Aplicar tema
        self.setStyleSheet(theme.get_sheet())

        self.initUI()

    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.AppPalette.white_01}; 
                border-radius: 8px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Icono Representativo (Caja/Paquete para farmacia)
        icon_lbl = QLabel()
        icon_pixmap = get_icon("pill.svg", color=theme.AppPalette.Primary, size=40).pixmap(40, 40)
        icon_lbl.setPixmap(icon_pixmap)
        
        # Títulos
        title_container = QWidget()
        title_container.setStyleSheet("background: transparent;")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        
        lbl_titulo = QLabel("Gestión de Farmacia")
        lbl_titulo.setObjectName("h1") # Estilo grande y negrita
        
        lbl_sub = QLabel("Control de inventario, recepción de pedidos y caducidad de insumos.")
        lbl_sub.setStyleSheet(f"color: {theme.AppPalette.black_02}; font-size: 14px;")
        
        title_layout.addWidget(lbl_titulo)
        title_layout.addWidget(lbl_sub)

        # Ensamblaje Header
        header_layout.addWidget(icon_lbl)
        header_layout.addSpacing(15)
        header_layout.addWidget(title_container)
        header_layout.addStretch()

        layout.addWidget(header_frame)

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
