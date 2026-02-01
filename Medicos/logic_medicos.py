# logic_medicos.py
from backend_medicos import GestorMedicos

class LogicaMedicos:
    def __init__(self):
        self.db = GestorMedicos()

    def _validar_comun(self, nombres, apellidos, especialidad, tel1, tel2, estado):
        """
        Valida las reglas de negocio. Retorna (True, "") o (False, "Mensaje de error").
        """
        # 1. Campos vacíos obligatorios
        if not nombres or not apellidos or not tel1 or not especialidad or not estado:
            return False, "Por favor complete todos los campos obligatorios (Nombres, Apellidos, Teléfono, Especialidad)."

        # 2. Validar Selecciones de ComboBox
        if "Seleccione" in especialidad:
            return False, "Debe seleccionar una especialidad válida."
        
        if "Seleccione" in estado:
            return False, "Debe seleccionar un estado válido."

        # 3. Validar Teléfonos (Solo números)
        if not tel1.isdigit():
            return False, "El Teléfono 1 debe contener solo números."
        
        if tel2 and not tel2.isdigit():
            return False, "El Teléfono 2 debe contener solo números."

        return True, ""

    def crear_medico(self, nombres, apellidos, especialidad, tel1, tel2, direccion, estado):
        # 1. Pasamos validación
        es_valido, msg = self._validar_comun(nombres, apellidos, especialidad, tel1, tel2, estado)
        if not es_valido:
            return False, msg

        # 2. Si pasa, guardamos en BD
        return self.db.registrar_medico(nombres, apellidos, especialidad, tel1, tel2, direccion, estado)

    def modificar_medico(self, id_medico, nombres, apellidos, especialidad, tel1, tel2, direccion, estado):
        # 1. Pasamos validación
        es_valido, msg = self._validar_comun(nombres, apellidos, especialidad, tel1, tel2, estado)
        if not es_valido:
            return False, msg

        # 2. Si pasa, actualizamos en BD
        return self.db.actualizar_medico(id_medico, nombres, apellidos, especialidad, tel1, tel2, direccion, estado)

    def eliminar_medico(self, id_medico):
        return self.db.eliminar_medico(id_medico)

    def obtener_todos(self, buscar="", filtro_esp=""):
        return self.db.obtener_medicos(buscar, filtro_esp)