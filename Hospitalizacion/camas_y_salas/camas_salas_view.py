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
        # Para habitacion: selección de sala
        sala_search = QLineEdit(); sala_search.setPlaceholderText("Buscar sala (para la habitación)...")
        sala_list = QListWidget()
        def refresh_hab_list():
            hab_list.clear()
            for hab in repo.buscar_habitaciones(hab_search.text()):
                nombre = hab.nombre_clave or hab.numero
                hab_list.addItem(f"{hab.numero} — {nombre} — {hab.ubicacion} (Estado: {hab.estado})")
        hab_search.textChanged.connect(refresh_hab_list)
        refresh_hab_list()
        def refresh_sala_list():
            sala_list.clear()
            # Mostrar salas disponibles
            for sid, sala in repo.salas.items():
                nombre = sala.nombre_clave or sid
                sala_list.addItem(f"{sid} — {nombre} — {sala.ubicacion} (Activa: {'sí' if sala.activa else 'no'})")
        sala_search.textChanged.connect(refresh_sala_list)
        refresh_sala_list()

        # Layout dinámico según tipo
        form.addRow("Tipo", tipo)
        form.addRow("Capacidad", capacidad)
        form.addRow("Ubicación", ubicacion_combo)
        # Sección cama destino (se muestra solo si tipo=cama)
        form.addRow("Habitación destino (para cama)", hab_search)
        form.addRow(hab_list)
        # Sección sala destino (se muestra solo si tipo=habitacion)
        form.addRow("Sala (para habitación)", sala_search)
        form.addRow(sala_list)

        def on_tipo_changed():
            is_cama = tipo.currentText() == "cama"
            is_hab = tipo.currentText() == "habitacion"
            capacidad.setEnabled(tipo.currentText() in {"habitacion","sala"})
            ubicacion_combo.setEnabled(tipo.currentText() in {"habitacion","sala"})
            hab_search.setEnabled(is_cama)
            hab_list.setEnabled(is_cama)
            sala_search.setEnabled(is_hab)
            sala_list.setEnabled(is_hab)
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
                rel_sala_id = None
                if t == "habitacion":
                    selected_sala = sala_list.currentItem().text() if sala_list.currentItem() else None
                    if not selected_sala:
                        QMessageBox.critical(dlg, "Error", "Seleccione una sala para la habitación"); return
                    rel_sala_id = selected_sala.split(" — ")[0]
                infra = Infraestructura("", t, int(capacidad.text()), ubic, rel_sala_id=rel_sala_id)
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
                nombre = hab.nombre_clave or hab.numero
                listw.addItem(f"{hab.numero} — {nombre} — {hab.ubicacion} (Estado: {hab.estado})")
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
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QListWidget
        dlg = QDialog(self); dlg.setWindowTitle("Asignar Habitación (Cama)")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); id_p.setPlaceholderText("ID del paciente (ej. P001)")
        sala_search = QLineEdit(); sala_search.setPlaceholderText("Buscar sala por ID, ubicación o clave...")
        sala_list = QListWidget()
        cama_search = QLineEdit(); cama_search.setPlaceholderText("Buscar cama por ID o nombre clave...")
        cama_list = QListWidget()

        def refresh_salas():
            sala_list.clear()
            for sid, sala in repo.salas.items():
                if not sala.activa:
                    continue
                nombre = sala.nombre_clave or sid
                text = f"{sid} — {nombre} — {sala.ubicacion}"
                q = (sala_search.text() or "").lower()
                if q in text.lower():
                    sala_list.addItem(text)

        def refresh_camas():
            cama_list.clear()
            # Filtrar camas disponibles; si hay una sala seleccionada, restringir por esa sala
            selected_sala_id = sala_list.currentItem().text().split(" — ")[0] if sala_list.currentItem() else None
            q = (cama_search.text() or "").lower()
            for cid, cama in repo.camas.items():
                if cama.estado != "disponible":
                    continue
                hab = repo._resolve_habitacion(cama.num_habitacion)
                if selected_sala_id and (not hab or hab.sala_id != selected_sala_id):
                    continue
                nombre_base = hab.nombre_clave if hab and hab.nombre_clave else cama.num_habitacion
                nombre = cama.nombre_clave or f"{nombre_base}"
                text = f"{cid} — {nombre}"
                if q in text.lower():
                    cama_list.addItem(text)

        sala_search.textChanged.connect(refresh_salas)
        cama_search.textChanged.connect(refresh_camas)
        sala_list.itemSelectionChanged.connect(refresh_camas)
        refresh_salas(); refresh_camas()

        form.addRow("ID Paciente", id_p)
        form.addRow("Buscar Sala", sala_search)
        form.addRow(sala_list)
        form.addRow("Buscar Cama", cama_search)
        form.addRow(cama_list)
        btns = QHBoxLayout(); ok = QPushButton("Asignar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            # Validar selección
            sala_item = sala_list.currentItem(); cama_item = cama_list.currentItem()
            if not id_p.text() or not sala_item or not cama_item:
                QMessageBox.critical(dlg, "Error", "Complete ID paciente y seleccione sala y cama disponibles"); return
            sala_id = sala_item.text().split(" — ")[0]
            cama_id = cama_item.text().split(" — ")[0]
            res = repo.asignar_cama(id_p.text(), sala_id, cama_id)
            if res == "OK":
                QMessageBox.information(dlg, "Éxito", "Cama asignada con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", res)
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def registrar_hospitalizacion_paciente(self):
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QListWidget
        dlg = QDialog(self); dlg.setWindowTitle("Registrar Hospitalización de Paciente")
        form = QFormLayout(dlg)
        id_p = QLineEdit(); fecha = QLineEdit(); motivo = QLineEdit()
        sala_search = QLineEdit(); sala_search.setPlaceholderText("Buscar sala por ID, ubicación o clave...")
        sala_list = QListWidget()
        cama_search = QLineEdit(); cama_search.setPlaceholderText("Buscar cama por ID o nombre clave...")
        cama_list = QListWidget()

        def refresh_salas():
            sala_list.clear()
            for sid, sala in repo.salas.items():
                if not sala.activa:
                    continue
                nombre = sala.nombre_clave or sid
                text = f"{sid} — {nombre} — {sala.ubicacion}"
                q = (sala_search.text() or "").lower()
                if q in text.lower():
                    sala_list.addItem(text)

        def refresh_camas():
            cama_list.clear()
            selected_sala_id = sala_list.currentItem().text().split(" — ")[0] if sala_list.currentItem() else None
            q = (cama_search.text() or "").lower()
            for cid, cama in repo.camas.items():
                if cama.estado != "disponible":
                    continue
                hab = repo._resolve_habitacion(cama.num_habitacion)
                if selected_sala_id and (not hab or hab.sala_id != selected_sala_id):
                    continue
                nombre_base = hab.nombre_clave if hab and hab.nombre_clave else cama.num_habitacion
                nombre = cama.nombre_clave or f"{nombre_base}"
                text = f"{cid} — {nombre}"
                if q in text.lower():
                    cama_list.addItem(text)

        sala_search.textChanged.connect(refresh_salas)
        sala_list.itemSelectionChanged.connect(refresh_camas)
        cama_search.textChanged.connect(refresh_camas)
        refresh_salas(); refresh_camas()

        form.addRow("ID Paciente", id_p)
        form.addRow("Fecha", fecha)
        form.addRow("Motivo", motivo)
        form.addRow("Buscar Sala", sala_search)
        form.addRow(sala_list)
        form.addRow("Buscar Cama", cama_search)
        form.addRow(cama_list)
        btns = QHBoxLayout(); ok = QPushButton("Registrar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            sala_item = sala_list.currentItem(); cama_item = cama_list.currentItem()
            if not all([id_p.text(), fecha.text(), motivo.text()]) or not sala_item or not cama_item:
                QMessageBox.critical(dlg, "Error", "Complete los datos y seleccione sala y cama disponibles"); return
            sala_id = sala_item.text().split(" — ")[0]
            cama_id = cama_item.text().split(" — ")[0]
            res = repo.registrar_hospitalizacion(id_p.text(), fecha.text(), sala_id, cama_id, motivo.text())
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
