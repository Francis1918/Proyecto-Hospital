from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
try:
    from .evolucion_widget import EvolucionWidget
    from .cuidados_widget import CuidadosWidget
except Exception:
    import os, sys
    # Asegurarnos de que la raíz del proyecto esté en sys.path para que
    # las importaciones absolutas como 'Hospitalizacion...' resuelvan
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    if root not in sys.path:
        sys.path.insert(0, root)
    from Hospitalizacion.evolucion_cuidados.evolucion_widget import EvolucionWidget
    from Hospitalizacion.evolucion_cuidados.cuidados_widget import CuidadosWidget

class EvolucionCuidadosView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        
        self.tab_evolucion = EvolucionWidget()
        self.tab_cuidados = CuidadosWidget()
        
        # En la UI sí podemos usar tildes
        self.tabs.addTab(self.tab_evolucion, "Evolución Médica")
        self.tabs.addTab(self.tab_cuidados, "Cuidados de Enfermería")
        
        self.main_layout.addWidget(self.tabs)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Prueba Evolución y Cuidados")
    win.setCentralWidget(EvolucionCuidadosView(win))
    win.show()
    sys.exit(app.exec())