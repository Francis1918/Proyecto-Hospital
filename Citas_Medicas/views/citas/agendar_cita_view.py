from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QMessageBox, QLineEdit, QFrame, QDateEdit, QTimeEdit
)
from PyQt6.QtCore import Qt, QDate, QTime

try:
    from Citas_Medicas.services import validaciones
except Exception:
    from services import validaciones


class AgendarCitaView(QWidget):
    """Formulario para que un paciente agende una cita.

    - Usa `PacienteController` pasado como `controller`.
    - Valida datos y delega la creación de la cita al `CitaController`.
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setObjectName("agendar_view")
        self.setWindowTitle("Agendar Cita")
        # Dimensiones mejoradas para mayor legibilidad y consistencia con el menú
        self.setFixedSize(520, 440)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 18, 20, 18)
        main_layout.setSpacing(14)

        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        titulo = QLabel("Agendar Cita")
        titulo.setStyleSheet("font-size:20px; font-weight:700; color: #2d3748;")
        header_layout.addWidget(titulo)
        main_layout.addWidget(header)

        form_frame = QFrame()
        form_frame.setObjectName("form")
        form_layout = QFormLayout(form_frame)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)

        self.txt_cedula = QLineEdit()
        # botón para consultar paciente por cédula
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setToolTip("Buscar paciente por cédula")
        self.btn_buscar.clicked.connect(self.buscar_paciente)

        # Campos informativos del paciente (solo visual)
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setEnabled(False)
        self.txt_apellido = QLineEdit()
        self.txt_apellido.setEnabled(False)

        self.date_fecha = QDateEdit()
        self.date_fecha.setDisplayFormat("yyyy-MM-dd")
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setDate(QDate.currentDate())

        self.time_hora = QTimeEdit()
        self.time_hora.setDisplayFormat("HH:mm")
        self.time_hora.setTime(QTime.currentTime())

        self.txt_motivo = QLineEdit()

        # Mejorar tamaños de controles para accesibilidad
        for w in (self.txt_cedula, self.txt_nombre, self.txt_apellido, self.txt_motivo):
            w.setMinimumHeight(34)
        self.date_fecha.setMinimumHeight(34)
        self.time_hora.setMinimumHeight(34)

        # cédula con botón de búsqueda
        cedula_row = QFrame()
        cedula_layout = QHBoxLayout(cedula_row)
        cedula_layout.setContentsMargins(0, 0, 0, 0)
        cedula_layout.setSpacing(8)
        cedula_layout.addWidget(self.txt_cedula)
        cedula_layout.addWidget(self.btn_buscar)
        form_layout.addRow("Cédula / ID:", cedula_row)

        # campos informativos (solo lectura)
        form_layout.addRow("Nombres:", self.txt_nombre)
        form_layout.addRow("Apellidos:", self.txt_apellido)

        form_layout.addRow("Fecha:", self.date_fecha)
        form_layout.addRow("Hora:", self.time_hora)
        form_layout.addRow("Motivo:", self.txt_motivo)

        main_layout.addWidget(form_frame)

        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 10, 0, 0)
        btn_layout.addStretch()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("secondary")
        btn_cancel.clicked.connect(self.close)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_guardar = QPushButton("Agendar")
        btn_guardar.setObjectName("primary")
        btn_guardar.clicked.connect(self.guardar_cita)
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_guardar)
        main_layout.addWidget(btn_frame)

        # Estilos profesionales coherentes con el menú (paleta azul-gris)
        self.setStyleSheet("""
            QWidget#agendar_view { background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #f7f9ff, stop:1 #eef2ff); }
            QFrame#header { background: transparent; padding: 6px 4px; }
            QLabel { font-family: 'Segoe UI', Arial, sans-serif; }
            QLabel[role='subtitle'] { color: #718096; font-size: 13px; }

            QFrame#form { background: rgba(255,255,255,0.98); border-radius: 10px; padding: 16px; }

            QLineEdit, QDateEdit, QTimeEdit {
                border: 1px solid #d1d5db; border-radius: 8px; padding: 6px 8px; background: white; font-size: 13px; color: #2d3748;
            }
            QLineEdit:disabled { background: #f5f7fa; color: #4a5568 }

            QPushButton#primary {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #667eea, stop:1 #764ba2);
                color: white; border: none; border-radius: 10px; padding: 10px 18px; font-weight: 700;
            }
            QPushButton#primary:hover { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #5a67d8, stop:1 #6b46c1); }

            QPushButton#secondary {
                background: transparent; color: #374151; border: 1px solid #c7d2fe; border-radius: 10px; padding: 8px 14px;
            }
            QPushButton#secondary:hover { background: rgba(103, 86, 255, 0.05); }

        """)

    def guardar_cita(self):
        cedula = self.txt_cedula.text().strip()
        fecha = self.date_fecha.date().toString("yyyy-MM-dd")
        hora = self.time_hora.time().toString("HH:mm")
        motivo = self.txt_motivo.text().strip() or "Consulta general"

        # Validaciones mínimas
        if not cedula or not fecha or not hora:
            QMessageBox.warning(self, "Campos vacíos", "Por favor complete todos los campos obligatorios.")
            return

        if not validaciones.validar_cedula(cedula):
            QMessageBox.warning(self, "Cédula inválida", "El formato de la cédula es inválido.")
            return

        if not validaciones.validar_fecha(fecha):
            QMessageBox.warning(self, "Fecha inválida", "Formato de fecha inválido (YYYY-MM-DD).")
            return

        if not validaciones.validar_hora(hora):
            QMessageBox.warning(self, "Hora inválida", "Formato de hora inválido (HH:MM).")
            return
        # Asegurar que se consultó el paciente y existe (consulta informativa según requisitos)
        if not getattr(self, '_paciente_encontrado', None):
            # Intentar consultar automáticamente antes de agendar
            try:
                if self.controller:
                    paciente = self.controller.consultar_paciente(cedula)
                    if paciente:
                        self.txt_nombre.setText(paciente.nombre)
                        self.txt_apellido.setText(paciente.apellido)
                        self._paciente_encontrado = paciente
            except Exception:
                pass

        if not getattr(self, '_paciente_encontrado', None):
            QMessageBox.warning(self, "Paciente no encontrado", "Debe buscar y seleccionar un paciente válido antes de agendar.")
            return

        # Delegar a controller y controlar errores de negocio
        try:
            nueva = None
            if self.controller is None:
                raise RuntimeError("Controlador no disponible")
            # Delegamos al controller (PacienteController) la creación de la cita
            nueva = self.controller.agendar_cita(cedula, fecha, hora, motivo)
        except ValueError as ve:
            QMessageBox.warning(self, "No se pudo agendar", str(ve))
            return
        except Exception as e:
            QMessageBox.critical(self, "Error interno", f"Ocurrió un error inesperado: {e}")
            return

        # Éxito
        QMessageBox.information(self, "Cita agendada", f"Cita registrada con ID {nueva.id_cita}\nFecha: {fecha} {hora}")
        self.close()

    def buscar_paciente(self):
        """Consulta el paciente usando el `PacienteController` pasado como `controller`.

        - Si se encuentra, muestra nombre y apellido en campos deshabilitados.
        - Si no, muestra un QMessageBox de error.
        """
        cedula = self.txt_cedula.text().strip()
        if not cedula:
            QMessageBox.warning(self, "Cédula vacía", "Ingrese la cédula del paciente antes de buscar.")
            return

        try:
            paciente = None
            if self.controller:
                paciente = self.controller.consultar_paciente(cedula)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al consultar paciente: {e}")
            return

        if not paciente:
            QMessageBox.information(self, "No encontrado", "Paciente no registrado en el sistema.")
            # limpiar campos informativos
            self.txt_nombre.setText("")
            self.txt_apellido.setText("")
            self._paciente_encontrado = None
            return

        # Mostrar datos personales SOLO de forma informativa
        self.txt_nombre.setText(paciente.nombre)
        self.txt_apellido.setText(paciente.apellido)
        self._paciente_encontrado = paciente
