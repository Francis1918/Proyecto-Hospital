# Medicos/backend/logic_medicos.py

import math
import re
from .backend_medicos import GestorMedicos

class LogicaMedicos:
    def __init__(self):
        self.db = GestorMedicos()
        self.datos_cache = []
        self.pagina_actual = 1
        self.total_paginas = 1
        self.filas_por_pagina = 20

    def _validar_cedula_ecuador(self, cedula):
        """
        Aplica el algoritmo de validación de cédula ecuatoriana.
        Retorna True si es válida, False si no lo es.
        """
        # 1. Validación básica: Longitud y numérico
        if not cedula.isdigit() or len(cedula) != 10:
            return False

        # 2. Validación de Provincia (dos primeros dígitos)
        # Rango válido: 01 a 24 (Provincias) y 30 (Ecuatorianos en el exterior)
        provincia = int(cedula[0:2])
        if not ((1 <= provincia <= 24) or provincia == 30):
            return False

        # 3. Validación del Tercer Dígito (Tipo de persona)
        # Menor a 6 para personas naturales
        tercer_digito = int(cedula[2])
        if tercer_digito >= 6:
            return False

        # 4. Algoritmo Módulo 10
        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        suma = 0

        # Recorremos los primeros 9 dígitos
        for i in range(9):
            valor = int(cedula[i]) * coeficientes[i]
            if valor >= 10:
                valor -= 9
            suma += valor

        # Cálculo del dígito verificador
        residuo = suma % 10
        digito_calculado = 0 if residuo == 0 else (10 - residuo)
        
        digito_verificador = int(cedula[9])

        return digito_calculado == digito_verificador

    def _validar_comun(self, cedula, nombres, apellidos, especialidad, tel1, tel2, estado):
        # 1. Campos vacíos
        if not cedula or not nombres or not apellidos or not tel1 or not especialidad or not estado:
            return False, "Por favor complete todos los campos obligatorios."

        # 2. VALIDACIÓN ESTRICTA DE CÉDULA ECUATORIANA
        if not self._validar_cedula_ecuador(cedula):
            return False, "La Cédula ingresada no es válida (Algoritmo Ecuador)."

        # 3. Validación de Nombres (Solo letras)
        patron_texto = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
        if not re.match(patron_texto, nombres):
            return False, "El nombre contiene caracteres inválidos."
        if not re.match(patron_texto, apellidos):
            return False, "El apellido contiene caracteres inválidos."

        if "Seleccione" in especialidad or "Seleccione" in estado:
            return False, "Seleccione opciones válidas."
            
        # 4. Validación Teléfonos
        if not tel1.isdigit(): 
            return False, "Teléfono 1 debe ser numérico."
        if len(tel1) > 10: 
            return False, "Teléfono 1 excede los 10 dígitos."
            
        if tel2:
            if not tel2.isdigit(): return False, "Teléfono 2 solo números."
            if len(tel2) > 10: return False, "Teléfono 2 excede 10 dígitos."

        return True, ""

    def crear_medico(self, *args):
        # args: (cedula, nombres, apellidos, esp, tel1, tel2, dir, est)
        es_valido, msg = self._validar_comun(*args[:6], args[-1])
        return (False, msg) if not es_valido else self.db.registrar_medico(*args)

    def modificar_medico(self, id_medico, *args):
        es_valido, msg = self._validar_comun(*args[:6], args[-1])
        return (False, msg) if not es_valido else self.db.actualizar_medico(id_medico, *args)

    # ... Resto de métodos (eliminar, paginación, etc.) siguen igual ...
    def eliminar_medico(self, id_medico):
        return self.db.eliminar_medico(id_medico)

    def actualizar_busqueda(self, buscar="", filtro_esp="", filtro_est=""):
        self.datos_cache = self.db.obtener_medicos(buscar, filtro_esp, filtro_est)
        total_items = len(self.datos_cache)
        self.total_paginas = 1 if total_items == 0 else math.ceil(total_items / self.filas_por_pagina)
        self.pagina_actual = 1

    def obtener_pagina_actual_items(self):
        inicio = (self.pagina_actual - 1) * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        return self.datos_cache[inicio:fin]

    def cambiar_pagina(self, delta):
        nueva_pagina = self.pagina_actual + delta
        if 1 <= nueva_pagina <= self.total_paginas:
            self.pagina_actual = nueva_pagina
            return True
        return False

    def get_info_paginacion(self):
        return self.pagina_actual, self.total_paginas

    def obtener_todos_sin_paginar(self):
        return self.datos_cache