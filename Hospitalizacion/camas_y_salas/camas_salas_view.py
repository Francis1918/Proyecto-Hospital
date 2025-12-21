from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from .auth import require_login
from .repository import repo

class CamasSalasView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def get_styles(self):
        return """
            QMainWindow { background-color: #e8f4fc; }
            QWidget#central { background-color: #e8f4fc; }
            QLabel#titulo { color: #1a365d; font-size: 26px; font-weight: bold; padding: 12px; }
            QFrame#menu_container { background-color: rgba(255,255,255,0.95); border-radius: 12px; padding: 16px; }
            QPushButton.menu_btn { background-color: #3182ce; color: white; border: none; border-radius: 8px; padding: 16px; font-size: 14px; font-weight: bold; min-height: 56px; min-width: 220px; }
            QPushButton.menu_btn:hover { background-color: #2c5282; }
            QPushButton.menu_btn:pressed { background-color: #1a365d; }
        """

    def init_ui(self):
        self.setWindowTitle("Gestión de Camas y Salas")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(self.get_styles())
        central = QWidget(); central.setObjectName("central")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20); layout.setContentsMargins(40,20,40,20)

        titulo = QLabel("Camas y Salas")
        titulo.setObjectName("titulo"); titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        container = QFrame(); container.setObjectName("menu_container")
        grid = QGridLayout(container); grid.setSpacing(16); grid.setContentsMargins(16,16,16,16)

        acciones = [
            ("Registrar Infraestructura (JEFE)", self.registrar_infraestructura),
            ("Consultar Estado Habitación (JEFE)", self.consultar_estado_habitacion),
            ("Actualizar Estado Habitación (JEFE)", self.actualizar_estado_habitacion),
            ("Asignar Habitación (JEFE)", self.asignar_habitacion),
            ("Registrar Hospitalización Paciente (JEFE)", self.registrar_hospitalizacion_paciente),
            ("Registrar Pedido Hospitalización (MEDICO)", self.registrar_pedido_hosp),
            ("Autorizar Hospitalización (JEFE)", self.autorizar_hospitalizacion),
            ("Consultar Estado Paciente (MEDICO)", self.consultar_estado_paciente),
            ("Autorizar Alta Paciente (MEDICO)", self.autorizar_alta_paciente),
        ]
        for i, (texto, fn) in enumerate(acciones):
            btn = QPushButton(texto); btn.setProperty("class","menu_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor); btn.clicked.connect(fn)
            grid.addWidget(btn, i//2, i%2)

        layout.addWidget(container)

    # Handlers con login y formularios rápidos via QMessageBox + inputs simples
    def registrar_infraestructura(self):
        if not require_login("JEFE", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Registrar Infraestructura")
        form = QFormLayout(dlg)
        nombre = QLineEdit(); tipo = QComboBox(); tipo.addItems(["sala","habitacion","cama"])
        capacidad = QLineEdit(); ubicacion = QLineEdit()
        form.addRow("Nombre", nombre); form.addRow("Tipo", tipo); form.addRow("Capacidad", capacidad); form.addRow("Ubicación", ubicacion)
        btns = QHBoxLayout(); ok = QPushButton("Registrar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            if not nombre.text() or not capacidad.text() or not ubicacion.text():
                QMessageBox.critical(dlg, "Error", "Error: Datos incompletos o inválidos"); return
            try:
                cap = int(capacidad.text())
            except ValueError:
                QMessageBox.critical(dlg, "Error", "Error: Datos incompletos o inválidos"); return
            from .models import Infraestructura
            ok_reg = repo.registrar_infraestructura(Infraestructura(nombre.text(), tipo.currentText(), cap, ubicacion.text()))
            if ok_reg:
                QMessageBox.information(dlg, "Éxito", "Infraestructura registrada con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", "No se pudo registrar la infraestructura")
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def registrar_pedido_hosp(self):
        if not require_login("MEDICO", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Registrar Pedido de Hospitalización")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); motivo = QLineEdit(); form.addRow("ID Paciente", id_p); form.addRow("Motivo", motivo)
        btns = QHBoxLayout(); ok = QPushButton("Registrar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            if not id_p.text() or not motivo.text():
                QMessageBox.critical(dlg, "Error", "Error: Datos incompletos o inválidos"); return
            if repo.registrar_pedido(id_p.text(), motivo.text()):
                QMessageBox.information(dlg, "Éxito", "Pedido de hospitalización registrado con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", "No se pudo registrar el pedido de hospitalización")
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def autorizar_hospitalizacion(self):
        if not require_login("JEFE", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Autorizar Hospitalización")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); form.addRow("ID Paciente", id_p)
        btns = QHBoxLayout(); ok = QPushButton("Autorizar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            res = repo.autorizar_hospitalizacion(id_p.text())
            if res == "OK":
                QMessageBox.information(dlg, "Éxito", "Hospitalización autorizada con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", res)
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def consultar_estado_habitacion(self):
        if not require_login("JEFE", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Consultar Estado de Habitación")
        form = QFormLayout(dlg)
        num = QLineEdit(); form.addRow("Número de Habitación", num)
        btns = QHBoxLayout(); ok = QPushButton("Consultar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            estado = repo.consultar_estado_habitacion(num.text())
            if estado is None:
                QMessageBox.critical(dlg, "Error", "Habitación no registrada")
            else:
                QMessageBox.information(dlg, "Resultado", f"Estado: {estado}"); dlg.accept()
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def actualizar_estado_habitacion(self):
        if not require_login("JEFE", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Actualizar Estado de Habitación")
        form = QFormLayout(dlg)
        num = QLineEdit(); estado = QComboBox(); estado.addItems(["disponible","ocupada","mantenimiento"]) 
        form.addRow("Número de Habitación", num); form.addRow("Nuevo Estado", estado)
        btns = QHBoxLayout(); ok = QPushButton("Actualizar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            if repo.actualizar_estado_habitacion(num.text(), estado.currentText()):
                QMessageBox.information(dlg, "Éxito", "Estado de habitación actualizado con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", "No se pudo actualizar el estado de la habitación")
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def asignar_habitacion(self):
        if not require_login("JEFE", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Asignar Habitación (Cama)")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); sala = QLineEdit(); id_cama = QLineEdit()
        form.addRow("ID Paciente", id_p); form.addRow("Sala", sala); form.addRow("ID Cama", id_cama)
        btns = QHBoxLayout(); ok = QPushButton("Asignar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            res = repo.asignar_cama(id_p.text(), sala.text(), id_cama.text())
            if res == "OK":
                QMessageBox.information(dlg, "Éxito", "Cama asignada con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", res)
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def registrar_hospitalizacion_paciente(self):
        if not require_login("JEFE", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Registrar Hospitalización de Paciente")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); fecha = QLineEdit(); sala = QLineEdit(); id_cama = QLineEdit(); motivo = QLineEdit()
        form.addRow("ID Paciente", id_p); form.addRow("Fecha", fecha); form.addRow("Sala", sala); form.addRow("ID Cama", id_cama); form.addRow("Motivo", motivo)
        btns = QHBoxLayout(); ok = QPushButton("Registrar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            if not all([id_p.text(), fecha.text(), sala.text(), id_cama.text(), motivo.text()]):
                QMessageBox.critical(dlg, "Error", "Error: Datos incompletos o inválidos"); return
            res = repo.registrar_hospitalizacion(id_p.text(), fecha.text(), sala.text(), id_cama.text(), motivo.text())
            if res == "OK":
                QMessageBox.information(dlg, "Éxito", "Hospitalización registrada con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", res)
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def consultar_estado_paciente(self):
        if not require_login("MEDICO", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Consultar Estado de Paciente")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); form.addRow("ID Paciente", id_p)
        btns = QHBoxLayout(); ok = QPushButton("Consultar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            estado = repo.consultar_estado_paciente(id_p.text())
            if estado is None:
                QMessageBox.critical(dlg, "Error", "Paciente no registrado")
            else:
                QMessageBox.information(dlg, "Resultado", f"Estado: {estado}"); dlg.accept()
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def autorizar_alta_paciente(self):
        if not require_login("MEDICO", self):
            QMessageBox.warning(self, "Acceso", "Credenciales incorrectas"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout
        dlg = QDialog(self); dlg.setWindowTitle("Autorizar Alta de Paciente")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); form.addRow("ID Paciente", id_p)
        btns = QHBoxLayout(); ok = QPushButton("Autorizar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            res = repo.autorizar_alta(id_p.text())
            if res == "OK":
                QMessageBox.information(dlg, "Éxito", "Alta del paciente autorizada con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", res)
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()
