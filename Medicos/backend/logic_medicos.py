# Medicos/backend/logic_medicos.py

import math # Necesario para calcular páginas
from .backend_medicos import GestorMedicos

class LogicaMedicos:
    def __init__(self):
        self.db = GestorMedicos()
        
        # --- ESTADO DE LA PAGINACIÓN ---
        self.datos_cache = []       # Guardamos aquí la lista filtrada completa
        self.pagina_actual = 1
        self.total_paginas = 1
        self.filas_por_pagina = 20  # Configuración centralizada

    # ... (Los métodos de crear, modificar, eliminar siguen IGUAL) ...
    def _validar_comun(self, nombres, apellidos, especialidad, tel1, tel2, estado):
        # (Tu código de validación existente...)
        if not nombres or not apellidos or not tel1 or not especialidad or not estado:
            return False, "Por favor complete todos los campos obligatorios."
        if "Seleccione" in especialidad or "Seleccione" in estado:
            return False, "Seleccione opciones válidas."
        if not tel1.isdigit(): return False, "Teléfono 1 solo números."
        if tel2 and not tel2.isdigit(): return False, "Teléfono 2 solo números."
        return True, ""

    def crear_medico(self, *args):
        es_valido, msg = self._validar_comun(*args[:5], args[-1])
        return (False, msg) if not es_valido else self.db.registrar_medico(*args)

    def modificar_medico(self, id_medico, *args):
        es_valido, msg = self._validar_comun(*args[:5], args[-1])
        return (False, msg) if not es_valido else self.db.actualizar_medico(id_medico, *args)

    def eliminar_medico(self, id_medico):
        return self.db.eliminar_medico(id_medico)

    # --- NUEVOS MÉTODOS DE PAGINACIÓN Y DATOS ---

    def actualizar_busqueda(self, buscar="", filtro_esp="", filtro_est=""):
        self.datos_cache = self.db.obtener_medicos(buscar, filtro_esp, filtro_est)
        
        total_items = len(self.datos_cache)
        if total_items == 0:
            self.total_paginas = 1
        else:
            self.total_paginas = math.ceil(total_items / self.filas_por_pagina)
            
        self.pagina_actual = 1

    def obtener_pagina_actual_items(self):
        """Retorna solo la sub-lista (slice) correspondiente a la página actual."""
        inicio = (self.pagina_actual - 1) * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        return self.datos_cache[inicio:fin]

    def cambiar_pagina(self, delta):
        """
        Intenta mover la página (adelante o atrás).
        Retorna True si cambió, False si estaba en el límite.
        """
        nueva_pagina = self.pagina_actual + delta
        if 1 <= nueva_pagina <= self.total_paginas:
            self.pagina_actual = nueva_pagina
            return True
        return False

    def get_info_paginacion(self):
        """Retorna (pagina_actual, total_paginas) para la UI."""
        return self.pagina_actual, self.total_paginas

    def obtener_todos_sin_paginar(self):
        """Utilidad para exportar CSV o buscar ID específico sin paginación."""
        return self.datos_cache