from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QGroupBox
)
from PyQt6.QtCore import pyqtSignal
from ..paciente_controller import PacienteController


class ActualizarDatosDialog(QDialog):
    """
    Diálogo para actualizar datos del paciente.
    Implementa los casos de uso:
    - actualizarDirección
    - actualizarTeléfono
    - actualizarE-mail
    - actualizarTeléfonoDeReferencia
    """

    datos_actualizados = pyqtSignal(str)

    def __init__(self, controller: PacienteController, cc_paciente: str, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.cc_paciente = cc_paciente
        self.paciente = None
        self.init_ui()
        self.cargar_datos_actuales()

    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle(f"Actualizar Datos - Paciente {self.cc_paciente}")
        self.setModal(True)
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout(self)

        # Información del paciente
        info_label = QLabel(f"Actualizando datos del paciente con CC: {self.cc_paciente}")
        info_label.setStyleSheet("font-weight: bold; font-size: 12pt; margin-bottom: 10px;")
        layout.addWidget(info_label)

        # Grupo: Datos de Contacto
        group_contacto = QGroupBox("Información de Contacto")
        form_contacto = QFormLayout()

        # Dirección
        lbl_direccion = QLabel("Dirección:")
        self.txt_direccion = QLineEdit()
        self.txt_direccion.setPlaceholderText("Nueva dirección del paciente")
        btn_actualizar_dir = QPushButton("Actualizar")
        btn_actualizar_dir.clicked.connect(self.actualizar_direccion)

        hbox_dir = QHBoxLayout()
        hbox_dir.addWidget(self.txt_direccion)
        hbox_dir.addWidget(btn_actualizar_dir)
        form_contacto.addRow(lbl_direccion, hbox_dir)

        # Teléfono
        lbl_telefono = QLabel("Teléfono:")
        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("Nuevo teléfono del paciente")
        btn_actualizar_tel = QPushButton("Actualizar")
        btn_actualizar_tel.clicked.connect(self.actualizar_telefono)

        hbox_tel = QHBoxLayout()
        hbox_tel.addWidget(self.txt_telefono)
        hbox_tel.addWidget(btn_actualizar_tel)
        form_contacto.addRow(lbl_telefono, hbox_tel)

        # Email
        lbl_email = QLabel("Email:")
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("Nuevo email del paciente")
        btn_actualizar_email = QPushButton("Actualizar")
        btn_actualizar_email.clicked.connect(self.actualizar_email)

        hbox_email = QHBoxLayout()
        hbox_email.addWidget(self.txt_email)
        hbox_email.addWidget(btn_actualizar_email)
        form_contacto.addRow(lbl_email, hbox_email)

        # Teléfono de Referencia
        lbl_tel_ref = QLabel("Teléfono Referencia:")
        self.txt_telefono_ref = QLineEdit()
        self.txt_telefono_ref.setPlaceholderText("Nuevo teléfono de referencia")
        btn_actualizar_tel_ref = QPushButton("Actualizar")
        btn_actualizar_tel_ref.clicked.connect(self.actualizar_telefono_ref)

        hbox_tel_ref = QHBoxLayout()
        hbox_tel_ref.addWidget(self.txt_telefono_ref)
        hbox_tel_ref.addWidget(btn_actualizar_tel_ref)
        form_contacto.addRow(lbl_tel_ref, hbox_tel_ref)

        group_contacto.setLayout(form_contacto)
        layout.addWidget(group_contacto)

        # Grupo: Datos Actuales
        self.group_actuales = QGroupBox("Datos Actuales del Paciente")
        self.form_actuales = QFormLayout()

        self.lbl_dir_actual = QLabel("-")
        self.form_actuales.addRow("Dirección actual:", self.lbl_dir_actual)

        self.lbl_tel_actual = QLabel("-")
        self.form_actuales.addRow("Teléfono actual:", self.lbl_tel_actual)

        self.lbl_email_actual = QLabel("-")
        self.form_actuales.addRow("Email actual:", self.lbl_email_actual)

        self.lbl_tel_ref_actual = QLabel("-")
        self.form_actuales.addRow("Tel. Ref. actual:", self.lbl_tel_ref_actual)

        self.group_actuales.setLayout(self.form_actuales)
        layout.addWidget(self.group_actuales)

        layout.addStretch()

        # Botones de acción
        buttons_layout = QHBoxLayout()

        btn_actualizar_todo = QPushButton("Actualizar Todo")
        btn_actualizar_todo.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        btn_actualizar_todo.clicked.connect(self.actualizar_todo)
        buttons_layout.addWidget(btn_actualizar_todo)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("background-color: #9E9E9E; color: white; padding: 8px;")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)

        layout.addLayout(buttons_layout)

    def cargar_datos_actuales(self):
        """Carga los datos actuales del paciente."""
        self.paciente = self.controller.consultar_paciente(self.cc_paciente)

        if self.paciente:
            self.lbl_dir_actual.setText(self.paciente.direccion)
            self.lbl_tel_actual.setText(self.paciente.telefono)
            self.lbl_email_actual.setText(self.paciente.email)
            self.lbl_tel_ref_actual.setText(
                self.paciente.telefono_referencia or "No registrado"
            )

            # Pre-llenar los campos con los datos actuales
            self.txt_direccion.setText(self.paciente.direccion)
            self.txt_telefono.setText(self.paciente.telefono)
            self.txt_email.setText(self.paciente.email)
            if self.paciente.telefono_referencia:
                self.txt_telefono_ref.setText(self.paciente.telefono_referencia)

    def actualizar_direccion(self):
        """Actualiza la dirección del paciente."""
        nueva_direccion = self.txt_direccion.text().strip()

        if not nueva_direccion:
            QMessageBox.warning(self, "Advertencia", "Ingrese una dirección válida")
            return

        exito, mensaje = self.controller.actualizar_direccion(
            self.cc_paciente, nueva_direccion
        )

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.lbl_dir_actual.setText(nueva_direccion)
            self.datos_actualizados.emit(self.cc_paciente)
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def actualizar_telefono(self):
        """Actualiza el teléfono del paciente."""
        nuevo_telefono = self.txt_telefono.text().strip()

        if not nuevo_telefono:
            QMessageBox.warning(self, "Advertencia", "Ingrese un teléfono válido")
            return

        exito, mensaje = self.controller.actualizar_telefono(
            self.cc_paciente, nuevo_telefono
        )

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.lbl_tel_actual.setText(nuevo_telefono)
            self.datos_actualizados.emit(self.cc_paciente)
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def actualizar_email(self):
        """Actualiza el email del paciente."""
        nuevo_email = self.txt_email.text().strip()

        if not nuevo_email:
            QMessageBox.warning(self, "Advertencia", "Ingrese un email válido")
            return

        exito, mensaje = self.controller.actualizar_email(
            self.cc_paciente, nuevo_email
        )

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.lbl_email_actual.setText(nuevo_email)
            self.datos_actualizados.emit(self.cc_paciente)
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def actualizar_telefono_ref(self):
        """Actualiza el teléfono de referencia del paciente."""
        nuevo_telefono_ref = self.txt_telefono_ref.text().strip()

        exito, mensaje = self.controller.actualizar_telefono_referencia(
            self.cc_paciente, nuevo_telefono_ref
        )

        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.lbl_tel_ref_actual.setText(nuevo_telefono_ref or "No registrado")
            self.datos_actualizados.emit(self.cc_paciente)
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def actualizar_todo(self):
        """Actualiza todos los campos a la vez."""
        respuesta = QMessageBox.question(
            self, "Confirmar",
            "¿Desea actualizar todos los campos modificados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            errores = []

            # Actualizar dirección
            if self.txt_direccion.text().strip():
                exito, msg = self.controller.actualizar_direccion(
                    self.cc_paciente, self.txt_direccion.text().strip()
                )
                if not exito:
                    errores.append(f"Dirección: {msg}")

            # Actualizar teléfono
            if self.txt_telefono.text().strip():
                exito, msg = self.controller.actualizar_telefono(
                    self.cc_paciente, self.txt_telefono.text().strip()
                )
                if not exito:
                    errores.append(f"Teléfono: {msg}")

            # Actualizar email
            if self.txt_email.text().strip():
                exito, msg = self.controller.actualizar_email(
                    self.cc_paciente, self.txt_email.text().strip()
                )
                if not exito:
                    errores.append(f"Email: {msg}")

            # Actualizar teléfono de referencia
            if self.txt_telefono_ref.text().strip():
                exito, msg = self.controller.actualizar_telefono_referencia(
                    self.cc_paciente, self.txt_telefono_ref.text().strip()
                )
                if not exito:
                    errores.append(f"Tel. Referencia: {msg}")

            if errores:
                QMessageBox.warning(self, "Errores", "\n".join(errores))
            else:
                QMessageBox.information(self, "Éxito",
                                        "Todos los datos fueron actualizados correctamente")
                self.cargar_datos_actuales()
                self.datos_actualizados.emit(self.cc_paciente)