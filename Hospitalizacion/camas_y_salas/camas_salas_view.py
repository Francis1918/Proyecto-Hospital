from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from .repository import repo

class CamasSalasView(QMainWindow):
    def __init__(self, rol: str, parent=None):
        super().__init__(parent)
        self.rol = rol  # 'JEFE' o 'MEDICO'
        self.padre = parent
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

        acciones_jefe = [
            ("Registrar Infraestructura", self.registrar_infraestructura),
            ("Consultar Estado Habitación", self.consultar_estado_habitacion),
            ("Actualizar Estado Habitación", self.actualizar_estado_habitacion),
            ("Asignar Habitación", self.asignar_habitacion),
            ("Registrar Hospitalización de Paciente", self.registrar_hospitalizacion_paciente),
            ("Autorizar Hospitalización", self.autorizar_hospitalizacion),
        ]
        acciones_medico = [
            ("Registrar Pedido de Hospitalización", self.registrar_pedido_hosp),
            ("Consultar Estado de Paciente", self.consultar_estado_paciente),
            ("Autorizar Alta de Paciente", self.autorizar_alta_paciente),
        ]
        acciones = acciones_jefe if self.rol == "JEFE" else acciones_medico
        for i, (texto, fn) in enumerate(acciones):
            btn = QPushButton(texto); btn.setProperty("class","menu_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor); btn.clicked.connect(fn)
            grid.addWidget(btn, i//2, i%2)

        layout.addWidget(container)

        # Botón de regreso
        btn_back = QPushButton("Regresar")
        btn_back.setProperty("class", "menu_btn")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        # Abrir maximizado
        try:
            self.setWindowState(self.windowState() | Qt.WindowState.WindowMaximized)
        except Exception:
            pass

    # Handlers con login y formularios rápidos via QMessageBox + inputs simples
    def registrar_infraestructura(self):
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QListWidget
        dlg = QDialog(self); dlg.setWindowTitle("Registrar Infraestructura")
        form = QFormLayout(dlg)
        tipo = QComboBox(); tipo.addItems(["habitacion","sala","cama"])  # orden habitual
        capacidad = QLineEdit(); capacidad.setPlaceholderText("Capacidad (solo sala/habitación)")
        ubicacion_combo = QComboBox(); ubicacion_combo.addItems(["Planta Baja","Piso 1","Piso 2","Piso 3"])  # para sala/habitación
        # Para cama: selección de habitación destino
        hab_search = QLineEdit(); hab_search.setPlaceholderText("Buscar habitación destino...")
        hab_list = QListWidget()
        def refresh_hab_list():
            hab_list.clear()
            for hab in repo.buscar_habitaciones(hab_search.text()):
                hab_list.addItem(f"{hab.numero} — {hab.ubicacion} (Estado: {hab.estado})")
        hab_search.textChanged.connect(refresh_hab_list)
        refresh_hab_list()

        # Layout dinámico según tipo
        form.addRow("Tipo", tipo)
        form.addRow("Capacidad", capacidad)
        form.addRow("Ubicación", ubicacion_combo)
        # Sección cama destino (se muestra solo si tipo=cama)
        form.addRow("Habitación destino (para cama)", hab_search)
        form.addRow(hab_list)

        def on_tipo_changed():
            is_cama = tipo.currentText() == "cama"
            capacidad.setEnabled(tipo.currentText() in {"habitacion","sala"})
            ubicacion_combo.setEnabled(tipo.currentText() in {"habitacion","sala"})
            hab_search.setEnabled(is_cama)
            hab_list.setEnabled(is_cama)
        tipo.currentTextChanged.connect(lambda _: on_tipo_changed())
        on_tipo_changed()

        btns = QHBoxLayout(); ok = QPushButton("Registrar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            from .models import Infraestructura
            t = tipo.currentText()
            # Validaciones
            if t in {"habitacion","sala"}:
                try:
                    _ = int(capacidad.text())
                except Exception:
                    QMessageBox.critical(dlg, "Error", "Error: Capacidad inválida"); return
                ubic = ubicacion_combo.currentText()
                infra = Infraestructura("", t, int(capacidad.text()), ubic)
                assigned_id = repo.registrar_infraestructura(infra)
                if assigned_id:
                    QMessageBox.information(dlg, "Éxito", f"Infraestructura registrada con éxito. ID: {assigned_id}"); dlg.accept()
                else:
                    QMessageBox.critical(dlg, "Error", "No se pudo registrar la infraestructura")
            else:  # cama
                # Obtener habitación seleccionada
                selected = hab_list.currentItem().text() if hab_list.currentItem() else None
                if not selected:
                    QMessageBox.critical(dlg, "Error", "Seleccione una habitación destino"); return
                hab_id = selected.split(" — ")[0]
                infra = Infraestructura("", t, 0, hab_id)
                assigned_id = repo.registrar_infraestructura(infra)
                if assigned_id:
                    QMessageBox.information(dlg, "Éxito", f"Cama registrada con éxito. ID: {assigned_id}"); dlg.accept()
                else:
                    QMessageBox.critical(dlg, "Error", "No se pudo registrar la cama")
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def registrar_pedido_hosp(self):
        if self.rol != "MEDICO":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
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
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
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
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
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
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QListWidget
        dlg = QDialog(self); dlg.setWindowTitle("Actualizar Estado de Habitación")
        form = QFormLayout(dlg)
        search = QLineEdit(); search.setPlaceholderText("Buscar habitación por ID o ubicación...")
        listw = QListWidget()
        def refresh():
            listw.clear()
            for hab in repo.buscar_habitaciones(search.text()):
                listw.addItem(f"{hab.numero} — {hab.ubicacion} (Estado: {hab.estado})")
        search.textChanged.connect(refresh)
        refresh()
        estado = QComboBox(); estado.addItems(["disponible","ocupada","mantenimiento"]) 
        form.addRow("Buscar", search)
        form.addRow(listw)
        form.addRow("Nuevo Estado", estado)
        btns = QHBoxLayout(); ok = QPushButton("Actualizar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            item = listw.currentItem()
            if not item:
                QMessageBox.critical(dlg, "Error", "Seleccione una habitación de la lista"); return
            hab_id = item.text().split(" — ")[0]
            if repo.actualizar_estado_habitacion(hab_id, estado.currentText()):
                QMessageBox.information(dlg, "Éxito", "Estado de habitación actualizado con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", "No se pudo actualizar el estado de la habitación")
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def asignar_habitacion(self):
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
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
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
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
        if self.rol != "MEDICO":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
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
        if self.rol != "MEDICO":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
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

    def go_back(self):
        # Reabrir Hospitalización (padre) y cerrar esta vista
        try:
            if self.padre is not None:
                self.padre.show()
                try:
                    self.padre.showMaximized()
                except Exception:
                    pass
                self.padre.raise_()
                self.padre.activateWindow()
        except Exception:
            pass
        self.close()
