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
        capacidad = QLineEdit(); capacidad.setPlaceholderText("Capacidad (solo sala)"); capacidad.setText("5")
        ubicacion_combo = QComboBox(); ubicacion_combo.addItems(["Planta Baja","Piso 1","Piso 2","Piso 3"])  # para sala/habitación
        # Para cama: selección de habitación destino
        hab_search = QLineEdit(); hab_search.setPlaceholderText("Buscar habitación destino...")
        hab_list = QListWidget()
        # Para habitacion: selección de sala
        sala_search = QLineEdit(); sala_search.setPlaceholderText("Buscar sala (para la habitación)...")
        sala_list = QListWidget()
        # Estado fijado de sala para habitacion
        selected_sala_id = None
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
            piso = ubicacion_combo.currentText()
            q = (sala_search.text() or "").strip().lower()
            for sid, sala in repo.salas.items():
                if (sala.ubicacion or "").strip().lower() != piso.strip().lower():
                    continue
                nombre = sala.nombre_clave or sid
                text = f"{sid} — {nombre} — {sala.ubicacion}"
                if not q or q in text.lower():
                    sala_list.addItem(text)
        sala_search.textChanged.connect(refresh_sala_list)
        refresh_sala_list()

        def fijar_sala_para_habitacion():
            nonlocal selected_sala_id
            item = sala_list.currentItem()
            if not item:
                QMessageBox.critical(dlg, "Error", "Seleccione una sala del piso elegido"); return
            selected_sala_id = item.text().split(" — ")[0]
            # Bloquear selección de sala
            sala_search.setEnabled(False); sala_list.setEnabled(False)
            # Mostrar solo la seleccionada
            sel_text = item.text()
            sala_list.clear(); sala_list.addItem(sel_text)

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
        ubicacion_combo.currentTextChanged.connect(lambda _: refresh_sala_list())
        on_tipo_changed()

        # Botón para fijar sala cuando se registra habitación
        btn_fix_sala = QPushButton("Fijar Sala")
        form.addRow(btn_fix_sala)
        btns = QHBoxLayout(); ok = QPushButton("Registrar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            from .models import Infraestructura
            t = tipo.currentText()
            # Validaciones
            if t in {"habitacion","sala"}:
                ubic = ubicacion_combo.currentText()
                rel_sala_id = None
                if t == "habitacion":
                    # Usar sala fijada o item actual
                    sel_text = sala_list.currentItem().text() if sala_list.currentItem() else None
                    sala_id = selected_sala_id or (sel_text.split(" — ")[0] if sel_text else None)
                    if not sala_id:
                        QMessageBox.critical(dlg, "Error", "Seleccione una sala para la habitación"); return
                    rel_sala_id = sala_id
                # Para sala, capacidad con default 5 si vacío
                cap_val = 5
                try:
                    cap_val = int(capacidad.text()) if capacidad.text() else 5
                except Exception:
                    cap_val = 5
                infra = Infraestructura("", t, cap_val, ubic, rel_sala_id=rel_sala_id)
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
        btn_fix_sala.clicked.connect(fijar_sala_para_habitacion)
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
        from PyQt6.QtWidgets import (
            QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout,
            QListWidget, QLabel, QListWidgetItem
        )
        dlg = QDialog(self); dlg.setWindowTitle("Autorizar Hospitalización")
        form = QFormLayout(dlg)

        # Búsqueda y listado de solicitudes pendientes con información de sala/habitación/cama si está disponible
        search = QLineEdit(); search.setPlaceholderText("Buscar por nombre o ID...")
        listw = QListWidget()
        info = QLabel("Seleccione un paciente para ver detalles")
        info.setWordWrap(True)

        # Construir lista de pacientes a autorizar (pedidos pendientes o con cama asignada)
        def build_items(q: str = ""):
            listw.clear()
            ql = (q or "").strip().lower()
            for pid in repo.listar_para_autorizar():
                pac = repo.pacientes.get(pid)
                nombre = pac.nombre if pac else pid
                display = f"{pid} — {nombre}"
                if not ql or ql in nombre.lower() or ql in pid.lower():
                    item = QListWidgetItem(display)
                    item.setData(Qt.ItemDataRole.UserRole, pid)
                    listw.addItem(item)

        def update_info():
            item = listw.currentItem()
            if not item:
                info.setText("Seleccione un paciente para ver detalles")
                return
            pid = item.data(Qt.ItemDataRole.UserRole)
            pac = repo.pacientes.get(pid)
            ped = repo.pedidos.get(pid)
            sala_id = repo.get_sala_de_paciente(pid)
            sala = repo.salas.get(sala_id) if sala_id else None
            cama_id = pac.cama_asignada if pac else None
            cama = repo.camas.get(cama_id) if cama_id else None
            hab = repo._resolve_habitacion(cama.num_habitacion) if cama else None
            sala_txt = sala_id or "—"
            sala_nombre = (sala.nombre_clave if sala and sala.nombre_clave else sala_txt)
            hab_txt = (hab.nombre_clave if hab and hab.nombre_clave else (hab.numero if hab else "—"))
            cama_txt = (cama.nombre_clave if cama and cama.nombre_clave else (cama_id or "—"))
            estado_pac = pac.estado if pac else "—"
            motivo = ped.motivo if ped else "—"
            info.setText(
                f"ID: {pid}\n"
                f"Nombre: {pac.nombre if pac else '—'}\n"
                f"Estado actual: {estado_pac}\n"
                f"Motivo del pedido: {motivo}\n"
                f"Sala: {sala_txt} — {sala_nombre}\n"
                f"Habitación: {hab_txt}\n"
                f"Cama: {cama_txt}"
            )

        search.textChanged.connect(lambda t: build_items(t))
        listw.itemSelectionChanged.connect(update_info)
        build_items()

        # Formulario y acciones
        form.addRow("Buscar", search)
        form.addRow(listw)
        form.addRow("Información", info)
        btns = QHBoxLayout(); ok = QPushButton("Autorizar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)

        def do_autorizar():
            item = listw.currentItem()
            if not item:
                QMessageBox.critical(dlg, "Error", "Seleccione un paciente de la lista"); return
            pid = item.data(Qt.ItemDataRole.UserRole)
            # Confirmación sí/no
            confirm = QMessageBox.question(
                dlg,
                "Confirmar autorización",
                f"¿Está seguro de autorizar la hospitalización de {pid}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return
            res = repo.autorizar_hospitalizacion(pid)
            if res == "OK":
                QMessageBox.information(dlg, "Éxito", "Hospitalización autorizada con éxito")
                dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", res)

        ok.clicked.connect(do_autorizar); cancel.clicked.connect(dlg.reject); dlg.exec()

    def consultar_estado_habitacion(self):
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QLabel, QListWidgetItem
        dlg = QDialog(self); dlg.setWindowTitle("Consultar Estado de Habitación")
        form = QFormLayout(dlg)
        # Búsqueda y listado: mostrar solo nombres de la habitación
        search = QLineEdit(); search.setPlaceholderText("Buscar habitación por nombre...")
        listw = QListWidget()
        info_label = QLabel("Seleccione una habitación para ver detalles")
        info_label.setWordWrap(True)
        def refresh():
            listw.clear()
            for hab in repo.buscar_habitaciones(search.text()):
                nombre = hab.nombre_clave or hab.numero
                item = QListWidgetItem(nombre)
                # Guardar el ID de la habitación en el item
                item.setData(Qt.ItemDataRole.UserRole, hab.numero)
                listw.addItem(item)
        search.textChanged.connect(refresh)
        refresh()

        def update_info():
            item = listw.currentItem()
            if not item:
                info_label.setText("Seleccione una habitación para ver detalles")
                return
            hab_id = item.data(Qt.ItemDataRole.UserRole)
            hab = repo.habitaciones.get(hab_id)
            if not hab:
                info_label.setText("Habitación no registrada")
                return
            # Resolver sala
            sala = repo.salas.get(hab.sala_id) if hab.sala_id else None
            sala_nombre = (sala.nombre_clave if sala and sala.nombre_clave else (hab.sala_id or "—"))
            sala_ubic = (sala.ubicacion if sala and sala.ubicacion else "—")
            sala_activa = ("sí" if (sala and sala.activa) else "no") if sala else "—"
            # Resolver camas vinculadas a la habitación
            camas_ids = []
            camas_disp = 0
            camas_ocup = 0
            for cid, cama in repo.camas.items():
                hmatch = repo._resolve_habitacion(cama.num_habitacion)
                if hmatch and hmatch.numero == hab.numero:
                    camas_ids.append(cama.nombre_clave or cid)
                    if cama.estado == "disponible":
                        camas_disp += 1
                    elif cama.estado == "ocupada":
                        camas_ocup += 1
            capacidad = len(camas_ids)
            camas_list = ", ".join(camas_ids) if camas_ids else "—"
            info_txt = (
                f"Nombre: {hab.nombre_clave or hab.numero}\n"
                f"ID Habitación: {hab.numero}\n"
                f"Sala: {hab.sala_id or '—'} — {sala_nombre} — {sala_ubic} (Activa: {sala_activa})\n"
                f"Ubicación: {hab.ubicacion}\n"
                f"Estado: {hab.estado}\n"
                f"Capacidad (camas): {capacidad}\n"
                f"Camas disponibles: {camas_disp}\n"
                f"Camas ocupadas: {camas_ocup}\n"
                f"Camas: {camas_list}"
            )
            info_label.setText(info_txt)

        listw.itemSelectionChanged.connect(update_info)
        # Orden del formulario
        form.addRow("Buscar", search)
        form.addRow(listw)
        form.addRow("Información", info_label)
        btns = QHBoxLayout(); cerrar = QPushButton("Cerrar"); btns.addWidget(cerrar); form.addRow(btns)
        cerrar.clicked.connect(dlg.reject); dlg.exec()

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
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QLabel
        dlg = QDialog(self); dlg.setWindowTitle("Asignar Habitación")
        form = QFormLayout(dlg)
        # Selección de paciente hospitalizado (sin sala todavía)
        paciente_search = QLineEdit(); paciente_search.setPlaceholderText("Buscar paciente hospitalizado...")
        paciente_list = QListWidget(); paciente_label = QLabel("Paciente: —")
        # Selección de sala
        sala_search = QLineEdit(); sala_search.setPlaceholderText("Buscar sala...")
        sala_list = QListWidget(); sala_label = QLabel("Sala: —")
        # Selección de habitación (cuarto) y cama
        hab_search = QLineEdit(); hab_search.setPlaceholderText("Buscar habitación (cuarto)...")
        hab_list = QListWidget()
        cama_search = QLineEdit(); cama_search.setPlaceholderText("Buscar cama disponible...")
        cama_list = QListWidget()
        # Deshabilitar cama hasta elegir habitación
        cama_search.setEnabled(False)
        cama_list.setEnabled(False)
        # Deshabilitar sala/habitacion/cama hasta fijar paciente
        sala_search.setEnabled(False); sala_list.setEnabled(False)
        hab_search.setEnabled(False); hab_list.setEnabled(False)

        # Cargar pacientes hospitalizados con sala registrada
        pacientes_ids = repo.listar_pacientes_hospitalizados_con_sala()
        def refresh_pacientes():
            paciente_list.clear()
            q = (paciente_search.text() or "").strip().lower()
            for pid in pacientes_ids:
                pac_nombre = repo.pacientes.get(pid).nombre if repo.pacientes.get(pid) else pid
                display = f"{pid} — {pac_nombre}"
                if not q or q in pac_nombre.lower() or q in pid.lower():
                    paciente_list.addItem(display)
        paciente_search.textChanged.connect(refresh_pacientes)
        refresh_pacientes()
        def refresh_salas():
            sala_list.clear()
            q = (sala_search.text() or "").lower()
            for sid, sala in repo.salas.items():
                if not sala.activa:
                    continue
                nombre = sala.nombre_clave or sid
                text = f"{sid} — {nombre} — {sala.ubicacion}"
                if q in text.lower():
                    sala_list.addItem(text)

        def refresh_habitaciones():
            hab_list.clear()
            # Filtrar por sala fijada
            sala_id = selected_sala_id
            q = (hab_search.text() or "").lower()
            for hid, hab in repo.habitaciones.items():
                if sala_id and hab.sala_id != sala_id:
                    continue
                nombre = hab.nombre_clave or hab.numero
                text = f"{hab.numero} — {nombre} — {hab.ubicacion} (Estado: {hab.estado})"
                if q in text.lower():
                    hab_list.addItem(text)

        def refresh_camas():
            cama_list.clear()
            # Filtrar camas disponibles por habitación seleccionada
            hab_item = hab_list.currentItem()
            hab_sel = None
            if hab_item:
                hab_id = hab_item.text().split(" — ")[0]
                hab_sel = repo.habitaciones.get(hab_id)
            q = (cama_search.text() or "").lower()
            for cid, cama in repo.camas.items():
                if cama.estado != "disponible":
                    continue
                hab_cama = repo._resolve_habitacion(cama.num_habitacion)
                if hab_sel and hab_cama != hab_sel:
                    continue
                nombre_base = hab_cama.nombre_clave if hab_cama and hab_cama.nombre_clave else cama.num_habitacion
                nombre = cama.nombre_clave or f"{nombre_base}"
                text = f"{cid} — {nombre}"
                if q in text.lower():
                    cama_list.addItem(text)

        selected_pid = None
        selected_sala_id = None
        selected_hab_id = None

        def fijar_paciente():
            nonlocal selected_pid
            item = paciente_list.currentItem()
            if not item:
                QMessageBox.critical(dlg, "Error", "Seleccione un paciente"); return
            selected_pid = item.text().split(" — ")[0]
            nombre = repo.pacientes.get(selected_pid).nombre if repo.pacientes.get(selected_pid) else selected_pid
            paciente_label.setText(f"Paciente: {nombre} ({selected_pid})")
            # Bloquear lista y búsqueda de pacientes y habilitar salas
            paciente_search.setEnabled(False); paciente_list.setEnabled(False)
            # Mostrar solo el seleccionado en la lista
            paciente_list.clear(); paciente_list.addItem(f"{selected_pid} — {nombre}")
            sala_search.setEnabled(True); sala_list.setEnabled(True)
            refresh_salas()

        def fijar_sala():
            nonlocal selected_sala_id
            item = sala_list.currentItem()
            if not item:
                QMessageBox.critical(dlg, "Error", "Seleccione una sala"); return
            selected_sala_id = item.text().split(" — ")[0]
            sala_label.setText(f"Sala: {selected_sala_id}")
            sala_search.setEnabled(False); sala_list.setEnabled(False)
            # Mostrar solo la seleccionada
            sel_text = item.text()
            sala_list.clear(); sala_list.addItem(sel_text)
            # habilitar habitaciones
            hab_search.setEnabled(True); hab_list.setEnabled(True)
            refresh_habitaciones()

        def fijar_habitacion():
            nonlocal selected_hab_id
            item = hab_list.currentItem()
            if not item:
                QMessageBox.critical(dlg, "Error", "Seleccione una habitación"); return
            selected_hab_id = item.text().split(" — ")[0]
            # mostrar fija
            hab_search.setEnabled(False); hab_list.setEnabled(False)
            # Mostrar solo la seleccionada
            sel_text = item.text()
            hab_list.clear(); hab_list.addItem(sel_text)
            cama_search.setEnabled(True); cama_list.setEnabled(True)
            refresh_camas()

        # evento no requerido: se usa botón 'Fijar Paciente'
        sala_search.textChanged.connect(refresh_salas)
        hab_search.textChanged.connect(refresh_habitaciones)
        cama_search.textChanged.connect(refresh_camas)

        form.addRow("Buscar Paciente", paciente_search)
        form.addRow(paciente_list)
        btn_fix_pac = QPushButton("Fijar Paciente"); form.addRow(btn_fix_pac)
        form.addRow(paciente_label)
        form.addRow("Buscar Sala", sala_search)
        form.addRow(sala_list)
        btn_fix_sala = QPushButton("Fijar Sala"); form.addRow(btn_fix_sala)
        form.addRow(sala_label)
        form.addRow("Buscar Habitación", hab_search)
        form.addRow(hab_list)
        btn_fix_hab = QPushButton("Fijar Habitación"); form.addRow(btn_fix_hab)
        form.addRow("Buscar Cama", cama_search)
        form.addRow(cama_list)
        btns = QHBoxLayout(); ok = QPushButton("Asignar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            # Validar selección
            cama_item = cama_list.currentItem()
            if not selected_pid or not selected_sala_id or not selected_hab_id or not cama_item:
                QMessageBox.critical(dlg, "Error", "Fije paciente, sala y habitación; luego seleccione una cama disponible"); return
            cama_id = cama_item.text().split(" — ")[0]
            res = repo.asignar_cama(selected_pid, selected_sala_id, cama_id)
            if res == "OK":
                QMessageBox.information(dlg, "Éxito", "Cama asignada con éxito"); dlg.accept()
            else:
                QMessageBox.critical(dlg, "Error", res)
        btn_fix_pac.clicked.connect(fijar_paciente)
        btn_fix_sala.clicked.connect(fijar_sala)
        btn_fix_hab.clicked.connect(fijar_habitacion)
        ok.clicked.connect(do); cancel.clicked.connect(dlg.reject); dlg.exec()

    def registrar_hospitalizacion_paciente(self):
        if self.rol != "JEFE":
            QMessageBox.warning(self, "Acceso", "Acción no permitida para su rol"); return
        from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QDateEdit, QTimeEdit
        from PyQt6.QtCore import QDate, QTime
        dlg = QDialog(self); dlg.setWindowTitle("Registrar Hospitalización de Paciente")
        form = QFormLayout(dlg)
        # Búsqueda y selección de paciente (por nombre) usando módulo Pacientes
        paciente_search = QLineEdit(); paciente_search.setPlaceholderText("Buscar paciente por nombre o apellido...")
        paciente_list = QListWidget()
        motivo = QLineEdit()
        # Date/Time pickers
        fecha_edit = QDateEdit(); fecha_edit.setCalendarPopup(True); fecha_edit.setDate(QDate.currentDate())
        hora_edit = QTimeEdit(); hora_edit.setTime(QTime.currentTime())
        # No seleccionar sala aquí: se asigna posteriormente en "Asignar Habitación"

        # Cargar pacientes desde el módulo Pacientes
        pacientes_cache = []
        try:
            # Intentar importar el controlador de pacientes para obtener la base en memoria
            try:
                from Pacientes.paciente_controller import PacienteController as _PC
            except Exception:
                import os, sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                from Pacientes.paciente_controller import PacienteController as _PC
            pc = _PC()
            pacientes_cache = pc.obtener_todos_pacientes()
        except Exception:
            pacientes_cache = []

        def refresh_pacientes():
            paciente_list.clear()
            q = (paciente_search.text() or "").strip().lower()
            for p in pacientes_cache:
                nombre_comp = f"{p.nombre} {p.apellido}".strip()
                display = f"{p.cc} — {nombre_comp}"
                # Excluir si ya está hospitalizado (según repositorio de hospitalización)
                try:
                    ya_hosp = repo.esta_hospitalizado_por_cc(getattr(p, "cc", None)) or repo.esta_hospitalizado_por_nombre(nombre_comp)
                except Exception:
                    ya_hosp = False
                if ya_hosp:
                    continue
                if not q or q in nombre_comp.lower() or q in (p.cc or "").lower():
                    paciente_list.addItem(display)
        paciente_search.textChanged.connect(refresh_pacientes)
        refresh_pacientes()

        # Ensamblar formulario: paciente, fecha, hora, motivo (sin sala)
        form.addRow("Buscar Paciente", paciente_search)
        form.addRow(paciente_list)
        # Fecha, hora y motivo al final
        form.addRow("Fecha", fecha_edit)
        form.addRow("Hora", hora_edit)
        form.addRow("Motivo", motivo)
        btns = QHBoxLayout(); ok = QPushButton("Registrar"); cancel = QPushButton("Cancelar"); btns.addWidget(ok); btns.addWidget(cancel); form.addRow(btns)
        def do():
            pac_item = paciente_list.currentItem()
            if not pac_item or not motivo.text():
                QMessageBox.critical(dlg, "Error", "Seleccione paciente y motive la hospitalización"); return
            # Resolver paciente: extraer cc y nombre, asegurar ID interno
            try:
                cc_sel, nombre_sel = pac_item.text().split(" — ", 1)
            except Exception:
                cc_sel, nombre_sel = None, pac_item.text()
            # Construir fecha/hora en formato ISO simple
            try:
                from datetime import datetime
                dt = datetime(
                    fecha_edit.date().year(),
                    fecha_edit.date().month(),
                    fecha_edit.date().day(),
                    hora_edit.time().hour(),
                    hora_edit.time().minute()
                )
                fecha_str = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                fecha_str = f"{fecha_edit.date().toString('yyyy-MM-dd')} {hora_edit.time().toString('HH:mm')}"
            # Asegurar paciente en el repositorio y registrar
            id_repo_pac = repo.ensure_repo_patient(cc_sel, nombre_sel)
            res = repo.registrar_hospitalizacion_sin_sala(id_repo_pac, fecha_str, motivo.text())
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
