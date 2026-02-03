from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QTextEdit, QTabWidget, QWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt
from ..paciente_controller import PacienteController


class ConsultarPacienteDialog(QDialog):
    """
    Diálogo para consultar pacientes con tabla y búsqueda.
    """

    def __init__(self, controller: PacienteController, cc_paciente: str = None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.cc_paciente = cc_paciente
        self.pacientes_lista = []
        self.init_ui()
        self.cargar_pacientes()

        if self.cc_paciente:
            self.txt_buscar.setText(self.cc_paciente)
            self.filtrar_pacientes()

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Consultar Pacientes")
        self.setModal(True)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Título
        titulo = QLabel("Consultar Pacientes")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Sección de búsqueda
        group_busqueda = QGroupBox("Buscar Paciente")
        busqueda_layout = QHBoxLayout()
        busqueda_layout.setSpacing(15)

        # Combo para tipo de búsqueda
        busqueda_layout.addWidget(QLabel("Buscar por:"))
        self.cmb_tipo_busqueda = QComboBox()
        self.cmb_tipo_busqueda.addItems(["Todo", "Cédula", "Nombre", "Apellido"])
        busqueda_layout.addWidget(self.cmb_tipo_busqueda)

        # Campo de búsqueda
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Ingrese el término de búsqueda...")
        self.txt_buscar.textChanged.connect(self.filtrar_pacientes)
        busqueda_layout.addWidget(self.txt_buscar)

        # Botón limpiar
        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_busqueda)
        busqueda_layout.addWidget(btn_limpiar)

        group_busqueda.setLayout(busqueda_layout)
        layout.addWidget(group_busqueda)

        # Tabla de pacientes
        group_tabla = QGroupBox("Pacientes Registrados")
        tabla_layout = QVBoxLayout()

        self.tabla_pacientes = QTableWidget()
        self.tabla_pacientes.setColumnCount(5)
        self.tabla_pacientes.setHorizontalHeaderLabels([
            "Cédula", "Nombre", "Apellido", "Teléfono", "Email"
        ])
        self.tabla_pacientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_pacientes.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla_pacientes.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_pacientes.doubleClicked.connect(self.abrir_detalle_paciente)

        # Ajustar columnas
        header = self.tabla_pacientes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        tabla_layout.addWidget(self.tabla_pacientes)

        # Botones de acción de la tabla
        botones_tabla_layout = QHBoxLayout()

        btn_ver_detalle = QPushButton("Ver Detalles del Paciente Seleccionado")
        btn_ver_detalle.clicked.connect(self.abrir_detalle_paciente)
        botones_tabla_layout.addWidget(btn_ver_detalle)

        btn_eliminar = QPushButton("Eliminar Paciente Seleccionado")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #e53e3e;
                color: white;
            }
            QPushButton:hover {
                background-color: #c53030;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_paciente)
        botones_tabla_layout.addWidget(btn_eliminar)

        tabla_layout.addLayout(botones_tabla_layout)

        group_tabla.setLayout(tabla_layout)
        layout.addWidget(group_tabla)

        # Botón cerrar
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("btn_cerrar")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)
        layout.addLayout(buttons_layout)

    def cargar_pacientes(self):
        """Carga todos los pacientes en la tabla."""
        self.pacientes_lista = self.controller.obtener_todos_pacientes()
        self.mostrar_pacientes(self.pacientes_lista)

    def mostrar_pacientes(self, pacientes):
        """Muestra la lista de pacientes en la tabla."""
        self.tabla_pacientes.setRowCount(0)

        for paciente in pacientes:
            row = self.tabla_pacientes.rowCount()
            self.tabla_pacientes.insertRow(row)

            self.tabla_pacientes.setItem(row, 0, QTableWidgetItem(paciente.cc))
            self.tabla_pacientes.setItem(row, 1, QTableWidgetItem(paciente.nombre))
            self.tabla_pacientes.setItem(row, 2, QTableWidgetItem(paciente.apellido))
            self.tabla_pacientes.setItem(row, 3, QTableWidgetItem(paciente.telefono or ""))
            self.tabla_pacientes.setItem(row, 4, QTableWidgetItem(paciente.email or ""))

    def filtrar_pacientes(self):
        """Filtra los pacientes según el criterio de búsqueda."""
        texto = self.txt_buscar.text().strip().lower()
        tipo = self.cmb_tipo_busqueda.currentText()

        if not texto:
            self.mostrar_pacientes(self.pacientes_lista)
            return

        pacientes_filtrados = []
        for paciente in self.pacientes_lista:
            if tipo == "Cédula":
                if texto in paciente.cc.lower():
                    pacientes_filtrados.append(paciente)
            elif tipo == "Nombre":
                if texto in paciente.nombre.lower():
                    pacientes_filtrados.append(paciente)
            elif tipo == "Apellido":
                if texto in paciente.apellido.lower():
                    pacientes_filtrados.append(paciente)
            else:  # Todo
                if (texto in paciente.cc.lower() or
                    texto in paciente.nombre.lower() or
                    texto in paciente.apellido.lower()):
                    pacientes_filtrados.append(paciente)

        self.mostrar_pacientes(pacientes_filtrados)

    def limpiar_busqueda(self):
        """Limpia el campo de búsqueda y muestra todos los pacientes."""
        self.txt_buscar.clear()
        self.cmb_tipo_busqueda.setCurrentIndex(0)
        self.mostrar_pacientes(self.pacientes_lista)

    def eliminar_paciente(self):
        """Elimina el paciente seleccionado de la tabla."""
        row = self.tabla_pacientes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente de la tabla")
            return

        cc = self.tabla_pacientes.item(row, 0).text()
        nombre = self.tabla_pacientes.item(row, 1).text()
        apellido = self.tabla_pacientes.item(row, 2).text()

        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar al paciente?\n\n"
            f"Nombre: {nombre} {apellido}\n"
            f"Cédula: {cc}\n\n"
            f"Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            exito, mensaje = self.controller.eliminar_paciente(cc)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.cargar_pacientes()
                self.filtrar_pacientes()
            else:
                QMessageBox.warning(self, "Error", mensaje)

    def abrir_detalle_paciente(self):
        """Abre la ventana de detalle del paciente seleccionado."""
        row = self.tabla_pacientes.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente de la tabla")
            return

        cc = self.tabla_pacientes.item(row, 0).text()
        paciente = self.controller.consultar_paciente(cc)

        if paciente:
            dialogo = DetallePacienteDialog(self.controller, paciente, self)
            dialogo.exec()
            # Refrescar la tabla por si hubo cambios
            self.cargar_pacientes()
            self.filtrar_pacientes()


class DetallePacienteDialog(QDialog):
    """
    Diálogo para mostrar el detalle completo de un paciente.
    """

    def __init__(self, controller: PacienteController, paciente, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.paciente = paciente
        self.init_ui()
        self.cargar_datos_paciente()


    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Detalle del Paciente")
        self.setModal(True)
        self.setMinimumSize(700, 600)
        self.setStyleSheet(self.get_styles())

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Información del paciente en la parte superior
        self.lbl_info_paciente = QLabel("")
        self.lbl_info_paciente.setObjectName("info_paciente")
        self.lbl_info_paciente.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_info_paciente)

        # Pestañas de información
        self.tabs = QTabWidget()

        # Pestaña 1: Datos Personales
        tab_datos = self.crear_tab_datos_personales()
        self.tabs.addTab(tab_datos, "Datos Personales")

        # Pestaña 2: Información de Contacto
        tab_contacto = self.crear_tab_contacto()
        self.tabs.addTab(tab_contacto, "Información de Contacto")

        # Pestaña 3: Anamnesis
        tab_anamnesis = self.crear_tab_anamnesis()
        self.tabs.addTab(tab_anamnesis, "Anamnesis")

        # Pestaña 4: Historia Clínica
        tab_historia = self.crear_tab_historia_clinica()
        self.tabs.addTab(tab_historia, "Historia Clínica")

        layout.addWidget(self.tabs)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)


        btn_imprimir = QPushButton("Imprimir Información")
        btn_imprimir.clicked.connect(self.imprimir_informacion)
        buttons_layout.addWidget(btn_imprimir)

        btn_exportar = QPushButton("Exportar a PDF")
        btn_exportar.clicked.connect(self.exportar_pdf)
        buttons_layout.addWidget(btn_exportar)

        buttons_layout.addStretch()

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("btn_cerrar")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)

        layout.addLayout(buttons_layout)

    def crear_tab_datos_personales(self) -> QWidget:
        """Crea la pestaña de datos personales."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group = QGroupBox("Información Personal")
        form = QFormLayout()

        self.lbl_cc = QLabel("-")
        form.addRow("Cédula:", self.lbl_cc)

        self.lbl_nombre = QLabel("-")
        form.addRow("Nombre:", self.lbl_nombre)

        self.lbl_apellido = QLabel("-")
        form.addRow("Apellido:", self.lbl_apellido)

        self.lbl_fecha_nacimiento = QLabel("-")
        form.addRow("Fecha de Nacimiento:", self.lbl_fecha_nacimiento)

        self.lbl_fecha_registro = QLabel("-")
        form.addRow("Fecha de Registro:", self.lbl_fecha_registro)

        group.setLayout(form)
        layout.addWidget(group)
        layout.addStretch()

        return widget

    def crear_tab_contacto(self) -> QWidget:
        """Crea la pestaña de información de contacto."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Grupo: Contacto Principal
        group_principal = QGroupBox("Contacto Principal")
        form_principal = QFormLayout()

        self.lbl_direccion = QLabel("-")
        self.lbl_direccion.setWordWrap(True)
        form_principal.addRow("Dirección:", self.lbl_direccion)

        self.lbl_telefono = QLabel("-")
        form_principal.addRow("Teléfono:", self.lbl_telefono)

        self.lbl_email = QLabel("-")
        form_principal.addRow("Email:", self.lbl_email)

        group_principal.setLayout(form_principal)
        layout.addWidget(group_principal)

        # Grupo: Contacto de Referencia
        group_referencia = QGroupBox("Contacto de Referencia")
        form_referencia = QFormLayout()

        self.lbl_telefono_ref = QLabel("-")
        form_referencia.addRow("Teléfono de Referencia:", self.lbl_telefono_ref)

        group_referencia.setLayout(form_referencia)
        layout.addWidget(group_referencia)

        # Botones de consulta específica
        buttons_layout = QHBoxLayout()

        btn_consultar_dir = QPushButton("Consultar Solo Dirección")
        btn_consultar_dir.clicked.connect(self.consultar_direccion)
        buttons_layout.addWidget(btn_consultar_dir)

        btn_consultar_tel = QPushButton("Consultar Solo Teléfono")
        btn_consultar_tel.clicked.connect(self.consultar_telefono)
        buttons_layout.addWidget(btn_consultar_tel)

        btn_consultar_tel_ref = QPushButton("Consultar Tel. Referencia")
        btn_consultar_tel_ref.clicked.connect(self.consultar_telefono_referencia)
        buttons_layout.addWidget(btn_consultar_tel_ref)

        layout.addLayout(buttons_layout)
        layout.addStretch()

        return widget

    def crear_tab_anamnesis(self) -> QWidget:
        """Crea la pestaña de anamnesis."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Información de Anamnesis")
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 11pt;")
        layout.addWidget(lbl_titulo)

        self.txt_anamnesis = QTextEdit()
        self.txt_anamnesis.setReadOnly(True)
        layout.addWidget(self.txt_anamnesis)

        btn_actualizar_anamnesis = QPushButton("Registrar/Actualizar Anamnesis")
        btn_actualizar_anamnesis.clicked.connect(self.abrir_dialogo_anamnesis)
        layout.addWidget(btn_actualizar_anamnesis)

        return widget

    def crear_tab_historia_clinica(self) -> QWidget:
        """Crea la pestaña de historia clínica."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Grupo: Información de Historia Clínica
        group_historia = QGroupBox("Historia Clínica")
        form_historia = QFormLayout()

        self.lbl_num_historia = QLabel("-")
        self.lbl_num_historia.setStyleSheet("color: #3182ce; font-weight: bold;")
        form_historia.addRow("N° Historia Clínica:", self.lbl_num_historia)

        self.lbl_fecha_creacion_hc = QLabel("-")
        form_historia.addRow("Fecha de Creación:", self.lbl_fecha_creacion_hc)

        self.lbl_estado_hc = QLabel("-")
        form_historia.addRow("Estado:", self.lbl_estado_hc)

        group_historia.setLayout(form_historia)
        layout.addWidget(group_historia)

        # Botones de acción
        buttons_layout = QHBoxLayout()

        btn_crear_hc = QPushButton("Crear Historia Clínica")
        btn_crear_hc.clicked.connect(self.crear_historia_clinica)
        buttons_layout.addWidget(btn_crear_hc)

        btn_ver_completa = QPushButton("Ver Historia Clínica Completa")
        btn_ver_completa.clicked.connect(self.editar_observaciones_hc)
        buttons_layout.addWidget(btn_ver_completa)

        layout.addLayout(buttons_layout)
        layout.addStretch()

        return widget

    def cargar_datos_paciente(self):
        """Carga todos los datos del paciente en la interfaz."""
        # Info superior
        self.lbl_info_paciente.setText(
            f"Paciente: {self.paciente.nombre} {self.paciente.apellido} - CC: {self.paciente.cc}"
        )

        # Datos personales
        self.lbl_cc.setText(self.paciente.cc)
        self.lbl_nombre.setText(self.paciente.nombre)
        self.lbl_apellido.setText(self.paciente.apellido)

        if self.paciente.fecha_nacimiento:
            fecha_nac = self.paciente.fecha_nacimiento.strftime("%d/%m/%Y")
            self.lbl_fecha_nacimiento.setText(fecha_nac)
        else:
            self.lbl_fecha_nacimiento.setText("No registrada")

        self.lbl_fecha_registro.setText(str(self.paciente.fecha_registro))

        # Contacto
        self.lbl_direccion.setText(self.paciente.direccion or "No registrada")
        self.lbl_telefono.setText(self.paciente.telefono or "No registrado")
        self.lbl_email.setText(self.paciente.email or "No registrado")
        self.lbl_telefono_ref.setText(self.paciente.telefono_referencia or "No registrado")

        # Anamnesis
        self.cargar_anamnesis()

        # Historia Clínica
        self.cargar_historia_clinica()

    def cargar_anamnesis(self):
        """Carga la anamnesis del paciente."""
        anamnesis = self.controller.consultar_anamnesis(self.paciente.cc)

        if anamnesis:
            texto = f"""
            MOTIVO DE CONSULTA:
            {anamnesis.get('motivo_consulta', 'No registrado')}

            ENFERMEDAD ACTUAL:
            {anamnesis.get('enfermedad_actual', 'No registrado')}

            ANTECEDENTES PERSONALES:
            {anamnesis.get('antecedentes_personales', 'No registrado')}

            ANTECEDENTES FAMILIARES:
            {anamnesis.get('antecedentes_familiares', 'No registrado')}

            ALERGIAS:
            {anamnesis.get('alergias', 'No registrado')}
            """
            self.txt_anamnesis.setText(texto.strip())
        else:
            self.txt_anamnesis.setText(
                "No hay información de anamnesis registrada para este paciente.\n\n"
                "Use el botón 'Registrar/Actualizar Anamnesis' para agregar la información."
            )

    def consultar_direccion(self):
        """Consulta solo la dirección del paciente."""
        direccion = self.controller.consultar_direccion_paciente(self.paciente.cc)
        QMessageBox.information(self, "Dirección del Paciente", f"Dirección: {direccion}")

    def consultar_telefono(self):
        """Consulta solo el teléfono del paciente."""
        telefono = self.controller.consultar_telefono_paciente(self.paciente.cc)
        QMessageBox.information(self, "Teléfono del Paciente", f"Teléfono: {telefono}")

    def consultar_telefono_referencia(self):
        """Consulta solo el teléfono de referencia del paciente."""
        telefono_ref = self.controller.consultar_telefono_referencia(self.paciente.cc)
        QMessageBox.information(
            self, "Teléfono de Referencia",
            f"Teléfono de Referencia: {telefono_ref or 'No registrado'}"
        )

    def abrir_dialogo_anamnesis(self):
        """Abre el diálogo para registrar o actualizar la anamnesis."""
        from .registrar_anamnesis_dialog import RegistrarAnamnesisDilaog
        dialogo = RegistrarAnamnesisDilaog(self.controller, self)

        # Pre-llenar la cédula y buscar automáticamente
        dialogo.txt_cc.setText(self.paciente.cc)
        dialogo.buscar_paciente()

        # Si ya existe anamnesis, cargar los datos
        anamnesis_existente = self.controller.consultar_anamnesis(self.paciente.cc)
        if anamnesis_existente:
            dialogo.txt_motivo_consulta.setText(anamnesis_existente.get('motivo_consulta', ''))
            dialogo.txt_enfermedad_actual.setText(anamnesis_existente.get('enfermedad_actual', ''))
            dialogo.txt_antecedentes_personales.setText(anamnesis_existente.get('antecedentes_personales', ''))
            dialogo.txt_antecedentes_familiares.setText(anamnesis_existente.get('antecedentes_familiares', ''))
            dialogo.txt_alergias.setText(anamnesis_existente.get('alergias', ''))

        if dialogo.exec():
            self.cargar_anamnesis()

    def cargar_historia_clinica(self):
        """Carga la historia clínica del paciente."""
        historia = self.controller.consultar_historia_clinica(self.paciente.cc)

        if historia:
            self.lbl_num_historia.setText(historia.get('numero_historia', '-'))
            fecha_creacion = historia.get('fecha_creacion', None)
            if fecha_creacion:
                self.lbl_fecha_creacion_hc.setText(fecha_creacion.strftime("%d/%m/%Y %H:%M"))
            else:
                self.lbl_fecha_creacion_hc.setText("-")
            self.lbl_estado_hc.setText(historia.get('estado', '-'))
        else:
            self.lbl_num_historia.setText("No registrada")
            self.lbl_fecha_creacion_hc.setText("-")
            self.lbl_estado_hc.setText("-")

    def crear_historia_clinica(self):
        """Crea la historia clínica del paciente."""
        # Verificar si ya existe
        historia = self.controller.consultar_historia_clinica(self.paciente.cc)
        if historia:
            QMessageBox.information(self, "Información", "El paciente ya tiene una historia clínica registrada.")
            return

        respuesta = QMessageBox.question(
            self,
            "Crear Historia Clínica",
            f"¿Desea crear la historia clínica para el paciente {self.paciente.nombre} {self.paciente.apellido}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            exito, mensaje = self.controller.crear_historia_clinica(self.paciente.cc)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.cargar_historia_clinica()
            else:
                QMessageBox.warning(self, "Error", mensaje)

    def editar_observaciones_hc(self):
        """Abre el diálogo de historia clínica para ver/editar."""
        historia = self.controller.consultar_historia_clinica(self.paciente.cc)
        if not historia:
            QMessageBox.warning(self, "Advertencia", "El paciente no tiene historia clínica. Debe crearla primero.")
            return

        from .historia_clinica_dialog import HistoriaClinicaDialog
        dialogo = HistoriaClinicaDialog(self.controller, self, paciente=self.paciente)
        dialogo.exec()

        # Recargar datos después de cerrar
        self.cargar_historia_clinica()

    def imprimir_informacion(self):
        """Imprime la información del paciente."""
        QMessageBox.information(self, "Imprimir", "Función de impresión en desarrollo")

    def exportar_pdf(self):
        """Exporta la información del paciente a PDF."""
        QMessageBox.information(self, "Exportar PDF", "Función de exportación a PDF en desarrollo")
#fin  