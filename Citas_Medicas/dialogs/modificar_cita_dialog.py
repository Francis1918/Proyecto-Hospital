from datetime import date, time, timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout
)

from ..citas_controller import CitasMedicasController
from ..validaciones import ValidacionesCitas
from ..dialogos_estilizados import (
    mostrar_error_codigo_no_encontrado,
    mostrar_confirmacion_modificar_cita,
    mostrar_exito_cita_modificada,
    mostrar_error_lista_validacion,
    mostrar_error_fecha_invalida_dialog
)
from core.theme import get_sheet, AppPalette


class ModificarCitaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Modificar Cita Médica")
        self.setModal(True)
        self.setMinimumWidth(520)
        self._cita_codigo = None
        # Aplicar hoja de estilos global para tema consistente
        self.setStyleSheet(get_sheet())
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("✏️ Modificar Cita")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.edt_codigo = QLineEdit()
        self.edt_codigo.setPlaceholderText("Ej: CM-ABC123")
        form.addRow("Código:", self.edt_codigo)

        self.lbl_info = QLabel("-")
        self.lbl_info.setWordWrap(True)
        form.addRow("Cita actual:", self.lbl_info)

        self.date_nueva = QDateEdit()
        self.date_nueva.setCalendarPopup(True)
        self.date_nueva.setMinimumDate(date.today() + timedelta(days=1))
        self.date_nueva.dateChanged.connect(self._refrescar_horas)
        form.addRow("Nueva fecha:", self.date_nueva)

        self.cmb_hora = QComboBox()
        form.addRow("Nueva hora:", self.cmb_hora)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cargar = QPushButton("Cargar")
        btn_cargar.clicked.connect(self._cargar)
        btns.addWidget(btn_cargar)

        self.btn_guardar = QPushButton("Guardar cambios")
        self.btn_guardar.clicked.connect(self._guardar)
        self.btn_guardar.setEnabled(False)
        btns.addWidget(self.btn_guardar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns.addWidget(btn_cerrar)

        layout.addLayout(btns)

    def _cargar(self):
        codigo = (self.edt_codigo.text() or "").strip()
        
        # Validar formato del código
        ok, msg = ValidacionesCitas.validar_codigo_cita(codigo)
        if not ok:
            mostrar_error_lista_validacion("❌ Código Inválido", [msg], self)
            self.btn_guardar.setEnabled(False)
            return
        
        cita = self.controller.consultar_cita_por_codigo(codigo)
        if not cita:
            mostrar_error_codigo_no_encontrado(codigo, self)
            self.lbl_info.setText("-")
            self.btn_guardar.setEnabled(False)
            self._cita_codigo = None
            return

        self._cita_codigo = cita.codigo
        self.lbl_info.setText(
            f"{cita.nombre_paciente} | {cita.especialidad} | {cita.medico} | "
            f"{cita.fecha.isoformat()} {cita.hora.strftime('%H:%M')} | Estado: {cita.estado}"
        )

        self.date_nueva.setDate(cita.fecha)
        self._refrescar_horas()

        idx = self.cmb_hora.findText(cita.hora.strftime("%H:%M"))
        if idx >= 0:
            self.cmb_hora.setCurrentIndex(idx)

        self.btn_guardar.setEnabled(True)

    def _refrescar_horas(self):
        if not self._cita_codigo:
            return
        cita = self.controller.consultar_cita_por_codigo(self._cita_codigo)
        if not cita:
            return

        qd = self.date_nueva.date()
        nueva_fecha = date(qd.year(), qd.month(), qd.day())

        self.cmb_hora.clear()
        horas = self.controller.obtener_horarios_disponibles(cita.id_medico, nueva_fecha)

        # permitir la hora original si misma fecha
        if nueva_fecha == cita.fecha and cita.hora not in horas:
            horas = sorted(horas + [cita.hora])

        for h in horas:
            self.cmb_hora.addItem(h.strftime("%H:%M"), h)

        if not horas:
            self.cmb_hora.addItem("(Sin horarios disponibles)", None)

    def _guardar(self):
        if not self._cita_codigo:
            mostrar_error_lista_validacion(
                "❌ Error",
                ["No hay cita cargada. Use el botón 'Cargar' primero."],
                self
            )
            return

        qd = self.date_nueva.date()
        nueva_fecha = date(qd.year(), qd.month(), qd.day())
        
        # Validar fecha
        ok, msg = ValidacionesCitas.validar_fecha_cita(nueva_fecha)
        if not ok:
            mostrar_error_fecha_invalida_dialog(msg, self)
            return

        hora_data = self.cmb_hora.currentData()
        if not isinstance(hora_data, time):
            mostrar_error_lista_validacion(
                "❌ Horario Inválido",
                ["Seleccione un horario válido."],
                self
            )
            return

        # Obtener la cita actual para confirmación
        cita_actual = self.controller.consultar_cita_por_codigo(self._cita_codigo)
        if not cita_actual:
            mostrar_error_lista_validacion(
                "❌ Error",
                ["La cita no fue encontrada en la base de datos."],
                self
            )
            return

        # Solicitar confirmación
        resp = mostrar_confirmacion_modificar_cita(
            codigo=self._cita_codigo,
            paciente=cita_actual.nombre_paciente,
            nueva_fecha=nueva_fecha.strftime('%d/%m/%Y'),
            nueva_hora=hora_data.strftime('%H:%M'),
            parent=self
        )
        
        # IMPORTANTE: Usar la comparación correcta de PyQt6
        if resp != QMessageBox.StandardButton.Yes:
            return

        # 2. Realizar la modificación en la base de datos
        ok, msg, _ = self.controller.modificar_cita(self._cita_codigo, nueva_fecha, hora_data)
        
        if not ok:
            mostrar_error_lista_validacion("❌ Error al Modificar", [msg], self)
            return

        # 3. ÉXITO: Mostrar mensaje y CERRAR el diálogo actual
        mostrar_exito_cita_modificada(
            codigo=self._cita_codigo,
            nueva_fecha=nueva_fecha.strftime('%d/%m/%Y'),
            nueva_hora=hora_data.strftime('%H:%M'),
            parent=self
        )
        
        # Esta línea es la más importante para evitar que salgan más ventanas
        self.accept()
