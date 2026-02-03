from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QMessageBox, QPushButton, QSpinBox, QVBoxLayout
)

from ..citas_controller import CitasMedicasController


class RegistrarAgendaDialog(QDialog):
    def __init__(self, controller: CitasMedicasController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Registrar Agenda del Médico")
        self.setModal(True)
        self.setMinimumWidth(520)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("🧩 Registrar/Actualizar Agenda del Médico")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.cmb_medico = QComboBox()
        # Llenado correcto usando el ID oculto (userData)
        medicos = self.controller.obtener_todos_medicos()
        for m in medicos:
            # Mostramos nombre y especialidad, guardamos el ID
            texto = f"{m['nombre_completo']} ({m['especialidad']})"
            self.cmb_medico.addItem(texto, m['id']) 
        
        self.cmb_medico.currentIndexChanged.connect(self._cargar_actual)
        form.addRow("Médico:", self.cmb_medico)

        self.spin_inicio = QSpinBox()
        self.spin_inicio.setRange(0, 23)
        form.addRow("Hora inicio (0-23):", self.spin_inicio)

        self.spin_fin = QSpinBox()
        self.spin_fin.setRange(1, 24)
        form.addRow("Hora fin (1-24):", self.spin_fin)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self._guardar)
        btns.addWidget(btn_guardar)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.reject)
        btns.addWidget(btn_cerrar)

        layout.addLayout(btns)

        self._cargar_actual(self.cmb_medico.currentText())

    def _cargar_actual(self, medico: str):
        inicio, fin = self.controller.obtener_agenda_medico(medico)
        self.spin_inicio.setValue(inicio)
        self.spin_fin.setValue(fin)

    def _guardar(self):
        id_medico = self.cmb_medico.currentData() 
        if id_medico is None: return
        inicio = int(self.spin_inicio.value())
        fin = int(self.spin_fin.value())
        ok, msg = self.controller.registrar_agenda_medico(id_medico, inicio, fin)
        if not ok:
            QMessageBox.warning(self, "Agenda", msg)
            return

        QMessageBox.information(self, "Agenda", msg)
        self.accept()
