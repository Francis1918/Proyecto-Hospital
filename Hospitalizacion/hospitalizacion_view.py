from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QFrame, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
try:
    from .camas_y_salas import CamasSalasView
except ImportError:
    # Permitir ejecutar este archivo directamente agregando el directorio padre al sys.path
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from Hospitalizacion.camas_y_salas import CamasSalasView


class HospitalizacionView(QMainWindow):
    """
    Submenú del módulo Hospitalización.
    Contiene accesos a:
    - Gestión de camas y salas
    - Visitas y restricciones
    - Gestión de admisión y alta
    - Gestión de orden, evolución y cuidados
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.padre = parent
        # Mantener referencias a subventanas para evitar GC y cierre inmediato
        self.ventanas_abiertas = {}
        self.init_ui()

    def get_styles(self):
        """Estilos QSS para la vista de hospitalización."""
        return """
            QMainWindow {
                background-color: #e8f4fc;
            }
            QWidget#central {
                background-color: #e8f4fc;
            }
            QLabel#titulo {
                color: #1a365d;
                font-size: 28px;
                font-weight: bold;
                padding: 16px;
            }
            QFrame#menu_container {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 24px;
            }
            QPushButton.menu_btn {
                background-color: #3182ce;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 20px;
                font-size: 14px;
                font-weight: bold;
                min-height: 70px;
                min-width: 220px;
            }
            QPushButton.menu_btn:hover {
                background-color: #2c5282;
            }
            QPushButton.menu_btn:pressed {
                background-color: #1a365d;
            }
            QPushButton#btn_salir {
                background-color: #e53e3e;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 16px;
                font-size: 14px;
                font-weight: bold;
                min-height: 60px;
                min-width: 180px;
            }
            QPushButton#btn_salir:hover {
                background-color: #c53030;
            }
        """

    def init_ui(self):
        self.setWindowTitle("Hospitalización - Submódulo")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self.get_styles())

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel("Hospitalización")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        container = QFrame()
        container.setObjectName("menu_container")
        grid = QGridLayout(container)
        grid.setSpacing(20)
        grid.setContentsMargins(20, 20, 20, 20)

        botones = [
            ("Gestión de camas y salas", self.abrir_camas_salas),
            ("Visitas y restricciones", self.abrir_visitas_restricciones),
            ("Gestión de admisión y alta", self.abrir_admision_alta),
            ("Gestión de orden", self.abrir_orden_evolucion_cuidados),
        ]

        for i, (texto, handler) in enumerate(botones):
            btn = QPushButton(texto)
            btn.setProperty("class", "menu_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(handler)
            row = i // 2
            col = i % 2
            grid.addWidget(btn, row, col)

        layout.addWidget(container)

        # Botón salir/cerrar submódulo
        btn_salir = QPushButton("Cerrar Hospitalización")
        btn_salir.setObjectName("btn_salir")
        btn_salir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_salir.clicked.connect(self.close)
        layout.addWidget(btn_salir, alignment=Qt.AlignmentFlag.AlignCenter)

    # Handlers provisionales
    def abrir_camas_salas(self):
        # Solicitar login y abrir vista con rol
        try:
            from .camas_y_salas.auth import authenticate_role
        except ImportError:
            import os, sys
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from Hospitalizacion.camas_y_salas.auth import authenticate_role

        rol = authenticate_role(self)
        if not rol:
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas")
            return

        # Cerrar cualquier otra ventana del módulo (solo una a la vez)
        for k, v in list(self.ventanas_abiertas.items()):
            try:
                if v.isVisible():
                    v.close()
            except Exception:
                pass
            self.ventanas_abiertas.pop(k, None)

        key = f"camas_salas_{rol.lower()}"
        self.ventanas_abiertas[key] = CamasSalasView(rol, parent=self)
        self.ventanas_abiertas[key].setWindowTitle(f"Camas y Salas - {rol}")
        w = self.ventanas_abiertas[key]
        w.show()
        try:
            w.showMaximized()
        except Exception:
            pass
        w.raise_()
        w.activateWindow()
        # Ocultar Hospitalización mientras la subvista está abierta
        self.hide()

    def abrir_visitas_restricciones(self):
        from Visitas.visitas_view import VisitasView  # Importa la nueva ventana

        visitas_window = VisitasView(self)
        visitas_window.exec()

    def abrir_admision_alta(self):
        QMessageBox.information(self, "Hospitalización", "Gestión de admisión y alta - En desarrollo.")

    def abrir_orden_evolucion_cuidados(self):
        # Solicitar login y abrir vista con rol
        try:
            from .camas_y_salas.auth import authenticate_role
        except ImportError:
            import os, sys
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from Hospitalizacion.camas_y_salas.auth import authenticate_role
            
        try:
             from .gestion_orden.orden_view import GestionOrdenView
        except ImportError:
            import os, sys
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from Hospitalizacion.gestion_orden.orden_view import GestionOrdenView

        rol = authenticate_role(self)
        if not rol:
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas")
            return

        # Cerrar cualquier otra ventana del módulo (solo una a la vez)
        for k, v in list(self.ventanas_abiertas.items()):
            try:
                if v.isVisible():
                    v.close()
            except Exception:
                pass
            self.ventanas_abiertas.pop(k, None)

        key = f"gestion_orden_{rol.lower()}"
        self.ventanas_abiertas[key] = GestionOrdenView(rol, parent=self)
        self.ventanas_abiertas[key].setWindowTitle(f"Gestión de Orden Médica - {rol}")
        w = self.ventanas_abiertas[key]
        w.show()
        try:
            w.showMaximized()
        except Exception:
            pass
        w.raise_()
        w.activateWindow()
        # Ocultar Hospitalización mientras la subvista está abierta
        self.hide()

    def closeEvent(self, event):
        """Al cerrar Hospitalización, volver al menú principal (padre)."""
        try:
            if self.padre is not None:
                self.padre.show()
                self.padre.raise_()
                self.padre.activateWindow()
        except Exception:
            pass
        event.accept()

if __name__ == "__main__":
    # Runner opcional para pruebas rápidas de esta vista
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = HospitalizacionView()
    w.show()
    sys.exit(app.exec())
