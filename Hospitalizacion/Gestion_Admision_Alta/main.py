import sys
from PyQt6.QtWidgets import QApplication
from controller import HospitalController
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Inicialización basada en MDJ [cite: 1]
    controller = HospitalController()
    window = MainWindow(controller)
    window.show()
    
    sys.exit(app.exec())