from PyQt6.QtWidgets import QInputDialog, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .buscar_paciente import buscar_paciente
from .datos_simulados import pacientes
from .repository import repo_visitas
from datetime import datetime

class VisitasView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visitas y Restricciones")
        self.setMinimumSize(400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Campo para ingresar la cédula del paciente
        self.label_cedula_paciente = QLabel("Ingrese la cédula del paciente:")
        layout.addWidget(self.label_cedula_paciente)

        self.input_cedula_paciente = QLineEdit()
        layout.addWidget(self.input_cedula_paciente)

        # Botón para buscar paciente
        self.btn_buscar_paciente = QPushButton("Buscar Paciente")
        self.btn_buscar_paciente.clicked.connect(self.buscar_paciente)
        layout.addWidget(self.btn_buscar_paciente)

        # Resultado de la búsqueda
        self.resultado_paciente_label = QLabel("")
        layout.addWidget(self.resultado_paciente_label)

        # Campo para ingresar la cédula del visitante
        self.label_cedula_visitante = QLabel("Ingrese la cédula del visitante:")
        layout.addWidget(self.label_cedula_visitante)

        self.input_cedula_visitante = QLineEdit()
        layout.addWidget(self.input_cedula_visitante)

        # Botón para registrar permiso
        self.btn_registrar_permiso = QPushButton("Registrar Permiso de Visita")
        self.btn_registrar_permiso.clicked.connect(self.registrar_permiso)
        layout.addWidget(self.btn_registrar_permiso)

        # Resultado del registro
        self.resultado_registro_label = QLabel("")
        layout.addWidget(self.resultado_registro_label)

        # Botón para listar permisos
        self.btn_listar_permisos = QPushButton("Listar Permisos de Visita")
        self.btn_listar_permisos.clicked.connect(self.listar_permisos)
        layout.addWidget(self.btn_listar_permisos)

        # Botón para registrar restricción
        self.btn_registrar_restriccion = QPushButton("Registrar Restricción de Visita")
        self.btn_registrar_restriccion.clicked.connect(self.registrar_restriccion)
        layout.addWidget(self.btn_registrar_restriccion)

        # Botón para consultar permisos y restricciones
        self.btn_consultar_permisos_restricciones = QPushButton("Consultar Permisos y Restricciones")
        self.btn_consultar_permisos_restricciones.clicked.connect(self.consultar_permisos_restricciones)
        layout.addWidget(self.btn_consultar_permisos_restricciones)

    def buscar_paciente(self):
        cedula = self.input_cedula_paciente.text().strip()
        if not cedula:
            QMessageBox.warning(self, "Error", "Debe ingresar una cédula.")
            return

        paciente = buscar_paciente(cedula)
        if paciente:
            if paciente["estado_clinico"] in ["Aislamiento", "Restringido"]:
                QMessageBox.warning(
                    self,
                    "Restricción",
                    f"El paciente {paciente['nombre']} no puede recibir visitas debido a su estado clínico: {paciente['estado_clinico']}."
                )
            else:
                self.resultado_paciente_label.setText(
                    f"Paciente encontrado:\nNombre: {paciente['nombre']}\nEstado Clínico: {paciente['estado_clinico']}\nHabitación: {paciente['habitacion']}\nCama: {paciente['cama']}"
                )
        else:
            self.resultado_paciente_label.setText("Paciente no registrado.")

    def registrar_permiso(self):
        cedula_paciente = self.input_cedula_paciente.text().strip()
        cedula_visitante = self.input_cedula_visitante.text().strip()

        if not cedula_paciente or not cedula_visitante:
            QMessageBox.warning(self, "Error", "Debe ingresar la cédula del paciente y del visitante.")
            return

        if cedula_paciente == cedula_visitante:
            QMessageBox.warning(self, "Error", "La cédula del paciente y del visitante no pueden ser iguales.")
            return

        # Verificar si el visitante ya existe en repositorio
        visitante = repo_visitas.obtener_visitante(cedula_visitante)
        if visitante:
            if visitante["restriccion"]:
                QMessageBox.warning(
                    self,
                    "Restricción",
                    f"El visitante {visitante['nombre']} tiene prohibido el ingreso."
                )
                return
        else:
            # Registrar nuevo visitante
            nombre, ok_nombre = QInputDialog.getText(self, "Nuevo Visitante", "Ingrese el nombre del visitante:")
            apellidos, ok_apellidos = QInputDialog.getText(self, "Nuevo Visitante", "Ingrese los apellidos del visitante:")

            # Validar nombres y apellidos
            if not ok_nombre or not ok_apellidos or not nombre or not apellidos:
                QMessageBox.warning(self, "Error", "Debe ingresar nombre y apellidos del visitante.")
                return

            if not nombre.replace(" ", "").isalpha() or not apellidos.replace(" ", "").isalpha():
                QMessageBox.warning(self, "Error", "El nombre y los apellidos solo pueden contener letras.")
                return

            repo_visitas.registrar_visitante(cedula_visitante, nombre, apellidos, restriccion=False)

        # Registrar permiso de visita
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        ok = repo_visitas.registrar_permiso(cedula_paciente, cedula_visitante)
        if ok:
            self.resultado_registro_label.setText("Permiso registrado con éxito.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo registrar el permiso en la BD.")

    def listar_permisos(self):
        permisos = repo_visitas.listar_permisos()
        if not permisos:
            QMessageBox.information(self, "Permisos de Visita", "No hay permisos registrados.")
            return
        permisos_texto = "\n".join([
            f"Paciente: {p['cedula_paciente']}, Visitante: {p['cedula_visitante']}, Fecha: {p['fecha']}, Hora: {p['hora']}"
            for p in permisos
        ])
        QMessageBox.information(self, "Permisos de Visita", permisos_texto)

    def registrar_restriccion(self):
        cedula_paciente = self.input_cedula_paciente.text().strip()
        if not cedula_paciente:
            QMessageBox.warning(self, "Error", "Debe ingresar la cédula del paciente.")
            return

        # Verificar si el paciente existe
        paciente = next((p for p in pacientes if p["cedula"] == cedula_paciente), None)
        if not paciente:
            QMessageBox.warning(self, "Error", "Paciente no encontrado.")
            return

        # Ingresar la cédula del visitante restringido
        cedula_visitante, ok_cedula = QInputDialog.getText(self, "Visitante Restringido", "Ingrese la cédula del visitante:")
        if not ok_cedula or not cedula_visitante:
            QMessageBox.warning(self, "Error", "Debe ingresar la cédula del visitante.")
            return

        # Validar formato de la cédula del visitante
        if not cedula_visitante.isdigit() or len(cedula_visitante) != 10:
            QMessageBox.warning(self, "Error", "Formato de cédula del visitante incorrecto.")
            return

        if cedula_paciente == cedula_visitante:
            QMessageBox.warning(self, "Error", "La cédula del paciente y del visitante no pueden ser iguales.")
            return

        # Verificar si el visitante está en la lista negra
        visitante = next((v for v in visitantes if v["cedula"] == cedula_visitante), None)
        if visitante and visitante["restriccion"]:
            QMessageBox.warning(self, "Error", f"El visitante {visitante['nombre']} está en la lista negra y tiene una restricción global.")
            return

        # Validar si la restricción ya existe
        if any(r["cedula"] == cedula_visitante for r in paciente["restricciones"]):
            QMessageBox.warning(self, "Error", "Esta persona ya tiene una restricción vigente.")
            return

        # Ingresar el motivo de la restricción
        motivo, ok_motivo = QInputDialog.getText(self, "Motivo de Restricción", "Ingrese el motivo de la restricción:")
        if not ok_motivo or not motivo:
            QMessageBox.warning(self, "Error", "Debe ingresar un motivo válido.")
            return

        # Registrar la restricción
        paciente["restricciones"].append({"cedula": cedula_visitante, "motivo": motivo})
        QMessageBox.information(self, "Restricción", "Restricción de visita aplicada exitosamente.")

    def consultar_permisos_restricciones(self):
        cedula_paciente = self.input_cedula_paciente.text().strip()

        # Validar formato de la cédula
        if not cedula_paciente.isdigit() or len(cedula_paciente) != 10:
            QMessageBox.warning(self, "Error", "Formato de cédula incorrecto.")
            return

        # Verificar si el paciente existe
        paciente = next((p for p in pacientes if p["cedula"] == cedula_paciente), None)
        if not paciente:
            QMessageBox.warning(self, "Error", "Paciente no registrado en el sistema actual.")
            return

        # Consultar permisos de visita
        permisos = [p for p in permisos_visita if p["cedula_paciente"] == cedula_paciente]
        permisos_texto = "\n".join([
            f"Visitante: {p['cedula_visitante']}, Fecha: {p['fecha']}, Hora: {p['hora']}"
            for p in permisos
        ]) if permisos else "No hay permisos registrados."

        # Consultar restricciones
        restricciones = paciente["restricciones"]
        restricciones_texto = "\n".join([
            f"Visitante: {r['cedula']}, Motivo: {r['motivo']}"
            for r in restricciones
        ]) if restricciones else "No hay restricciones registradas."

        # Mostrar resultados
        if not permisos and not restricciones:
            QMessageBox.information(
                self,
                "Permisos y Restricciones",
                "El paciente no tiene permisos ni restricciones registradas hasta el momento."
            )
        else:
            QMessageBox.information(
                self,
                "Permisos y Restricciones",
                f"Permisos de Visita:\n{permisos_texto}\n\nRestricciones:\n{restricciones_texto}"
            )