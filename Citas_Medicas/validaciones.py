"""
Módulo de validaciones para Citas Médicas.
Centraliza todas las reglas de negocio y validaciones de datos.
"""

from typing import Tuple
from datetime import date, time


class ValidacionesCitas:
    """Centraliza validaciones para el módulo de Citas Médicas."""

    # =====================================================
    # 1. VALIDACIÓN DE CÉDULA ECUATORIANA
    # =====================================================
    @staticmethod
    def validar_cedula_ecuador(cedula: str) -> Tuple[bool, str]:
        """
        Valida una cédula ecuatoriana siguiendo el algoritmo oficial.
        
        Reglas:
        1. Debe tener exactamente 10 dígitos
        2. Los 2 primeros dígitos (provincia) deben estar entre 01 y 24
        3. El 3er dígito no debe ser mayor a 5
        4. Validar dígito verificador (10º dígito) con algoritmo módulo 10
        
        :param cedula: Número de cédula como string
        :return: (es_valida: bool, mensaje: str)
        """
        # 1. Validaciones básicas
        cedula = (cedula or "").strip()
        
        if not cedula:
            return False, "La cédula no puede estar vacía."
        
        if not cedula.isdigit():
            return False, "La cédula debe contener solo números (0-9)."
        
        if len(cedula) != 10:
            return False, f"La cédula debe tener exactamente 10 dígitos (tiene {len(cedula)})."

        # 2. Validar provincia (primeros 2 dígitos: 01-24)
        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            return False, f"Provincia inválida: {cedula[:2]}. Debe estar entre 01 y 24."

        # 3. Validar tercer dígito (0-5, no puede ser 6-9)
        tercer_digito = int(cedula[2])
        if tercer_digito > 5:
            return False, f"Dígito de tipo inválido: {tercer_digito}. Debe estar entre 0 y 5."

        # 4. Cálculo del dígito verificador (algoritmo módulo 10)
        coeficientes = [2, 1] * 5  # [2,1,2,1,2,1,2,1,2,1]
        suma = 0

        for i in range(9):
            valor = int(cedula[i]) * coeficientes[i]
            # Si el producto es > 9, restar 9
            if valor > 9:
                valor -= 9
            suma += valor

        # El dígito verificador es (10 - (suma % 10)) % 10
        digito_calculado = (10 - (suma % 10)) % 10
        digito_real = int(cedula[9])

        if digito_calculado != digito_real:
            return False, f"Cédula inválida: El dígito verificador no coincide (calculado: {digito_calculado}, recibido: {digito_real})."

        return True, "Cédula ecuatoriana válida."

    # =====================================================
    # 2. VALIDACIÓN DE CÉDULA (FORMATO GENERAL)
    # =====================================================
    @staticmethod
    def validar_cedula_formato(cedula: str) -> Tuple[bool, str]:
        """
        Valida el formato básico de cédula (sin algoritmo específico).
        Útil para búsquedas rápidas antes de aplicar validación completa.
        
        :param cedula: Número de cédula como string
        :return: (es_valida: bool, mensaje: str)
        """
        cedula = (cedula or "").strip()
        
        if not cedula:
            return False, "Debe ingresar el número de cédula."
        
        if not cedula.isdigit():
            return False, "La cédula debe contener solo números."
        
        if len(cedula) != 10:
            return False, f"La cédula debe tener exactamente 10 dígitos."
        
        return True, "Formato de cédula válido."

    # =====================================================
    # 3. VALIDACIÓN DE FECHA
    # =====================================================
    @staticmethod
    def validar_fecha_cita(fecha_obj: date, dias_minimos: int = 1) -> Tuple[bool, str]:
        """
        Valida que la fecha sea válida para agendar una cita.
        
        Reglas:
        1. La fecha debe ser posterior a hoy (configurable con dias_minimos)
        2. No puede ser fecha pasada
        
        :param fecha_obj: Objeto datetime.date
        :param dias_minimos: Número mínimo de días desde hoy (default 1)
        :return: (es_valida: bool, mensaje: str)
        """
        if not isinstance(fecha_obj, date):
            return False, "La fecha debe ser un objeto datetime.date válido."
        
        dias_diff = (fecha_obj - date.today()).days
        
        if dias_diff < dias_minimos:
            if dias_minimos == 1:
                return False, "La cita debe ser para mañana o posterior."
            else:
                return False, f"La cita debe ser con al menos {dias_minimos} días de anticipación."
        
        return True, "Fecha válida para cita."

    # =====================================================
    # 4. VALIDACIÓN DE HORA
    # =====================================================
    @staticmethod
    def validar_hora_cita(hora_obj: time) -> Tuple[bool, str]:
        """
        Valida que la hora sea válida para una cita.
        
        Reglas:
        1. La hora debe ser un objeto datetime.time válido
        2. Debe estar en rango de horario laboral (09:00 - 17:00)
        
        :param hora_obj: Objeto datetime.time
        :return: (es_valida: bool, mensaje: str)
        """
        if not isinstance(hora_obj, time):
            return False, "La hora debe ser un objeto datetime.time válido."
        
        hora_minima = time(9, 0)
        hora_maxima = time(17, 0)
        
        if hora_obj < hora_minima:
            return False, "El consultorio abre a las 09:00."
        
        if hora_obj > hora_maxima:
            return False, "El consultorio cierra a las 17:00."
        
        return True, "Hora válida para cita."

    # =====================================================
    # 5. VALIDACIÓN DE CÓDIGO DE CITA
    # =====================================================
    @staticmethod
    def validar_codigo_cita(codigo: str) -> Tuple[bool, str]:
        """
        Valida el formato de código de cita (CM-XXXXXX).
        
        Reglas:
        1. Debe comenzar con "CM-"
        2. Debe tener 6 caracteres alpanuméricos después de "CM-"
        3. Total: 9 caracteres
        
        :param codigo: Código de cita como string
        :return: (es_valida: bool, mensaje: str)
        """
        codigo = (codigo or "").strip()
        
        if not codigo:
            return False, "El código de cita no puede estar vacío."
        
        if not codigo.startswith("CM-"):
            return False, "El código debe comenzar con 'CM-'."
        
        if len(codigo) != 9:
            return False, f"El código debe tener 9 caracteres (ej: CM-ABC123)."
        
        # Validar que los últimos 6 caracteres sean alfanuméricos
        cuerpo = codigo[3:]  # Obtener los últimos 6 caracteres
        if not cuerpo.isalnum():
            return False, "El código debe contener solo letras y números después de 'CM-'."
        
        return True, "Código de cita válido."

    # =====================================================
    # 6. VALIDACIÓN DE CONSULTORIO
    # =====================================================
    @staticmethod
    def validar_consultorio(consultorio: str) -> Tuple[bool, str]:
        """
        Valida que el consultorio no esté vacío.
        
        :param consultorio: Nombre/número del consultorio
        :return: (es_valida: bool, mensaje: str)
        """
        consultorio = (consultorio or "").strip()
        
        if not consultorio:
            return False, "El consultorio no puede estar vacío."
        
        if len(consultorio) < 2:
            return False, "El consultorio debe tener al menos 2 caracteres."
        
        if len(consultorio) > 100:
            return False, "El consultorio no puede exceder 100 caracteres."
        
        return True, "Consultorio válido."

    # =====================================================
    # 7. VALIDACIÓN DE ESPECIALIDAD
    # =====================================================
    @staticmethod
    def validar_especialidad(especialidad: str, especialidades_validas: list = None) -> Tuple[bool, str]:
        """
        Valida que la especialidad sea válida.
        
        :param especialidad: Nombre de la especialidad
        :param especialidades_validas: Lista de especialidades permitidas (opcional)
        :return: (es_valida: bool, mensaje: str)
        """
        especialidad = (especialidad or "").strip()
        
        if not especialidad:
            return False, "La especialidad no puede estar vacía."
        
        if especialidades_validas:
            if especialidad not in especialidades_validas:
                return False, f"Especialidad '{especialidad}' no es válida."
        
        return True, "Especialidad válida."

    # =====================================================
    # 8. VALIDACIÓN DE ESTADO DE CITA
    # =====================================================
    @staticmethod
    def validar_estado_cita(estado: str) -> Tuple[bool, str]:
        """
        Valida que el estado sea uno de los permitidos.
        
        Estados válidos:
        - Confirmada
        - Cancelada
        - Reprogramada
        - Asistió
        - Ausente
        - Tardanza
        
        :param estado: Estado de la cita
        :return: (es_valida: bool, mensaje: str)
        """
        estados_validos = {
            "Confirmada", "Cancelada", "Reprogramada",
            "Asistió", "Ausente", "Tardanza"
        }
        
        estado = (estado or "").strip()
        
        if not estado:
            return False, "El estado de cita no puede estar vacío."
        
        if estado not in estados_validos:
            return False, f"Estado inválido: '{estado}'. Valores válidos: {', '.join(sorted(estados_validos))}."
        
        return True, "Estado de cita válido."

    # =====================================================
    # 9. VALIDACIÓN DE COMENTARIO
    # =====================================================
    @staticmethod
    def validar_comentario(comentario: str, max_caracteres: int = 500) -> Tuple[bool, str]:
        """
        Valida que el comentario sea válido.
        
        :param comentario: Texto del comentario
        :param max_caracteres: Máximo de caracteres permitidos (default 500)
        :return: (es_valida: bool, mensaje: str)
        """
        comentario = (comentario or "").strip()
        
        if len(comentario) > max_caracteres:
            return False, f"El comentario no puede exceder {max_caracteres} caracteres (tiene {len(comentario)})."
        
        return True, "Comentario válido."

    # =====================================================
    # 10. VALIDACIÓN COMPLETA DE CITA
    # =====================================================
    @staticmethod
    def validar_cita_completa(
        cc_paciente: str,
        especialidad: str,
        fecha: date,
        hora: time,
        consultorio: str = "",
        estado: str = "Confirmada",
        comentario: str = "",
        especialidades_validas: list = None
    ) -> Tuple[bool, list]:
        """
        Valida todos los campos de una cita de una sola vez.
        
        :param cc_paciente: Cédula del paciente
        :param especialidad: Especialidad médica
        :param fecha: Fecha de la cita
        :param hora: Hora de la cita
        :param consultorio: Consultorio (opcional)
        :param estado: Estado de la cita
        :param comentario: Comentario (opcional)
        :param especialidades_validas: Lista de especialidades válidas
        :return: (es_valida: bool, lista_errores: list)
        """
        errores = []
        
        # Validar cédula con algoritmo Ecuador
        ok, msg = ValidacionesCitas.validar_cedula_ecuador(cc_paciente)
        if not ok:
            errores.append(msg)
        
        # Validar especialidad
        ok, msg = ValidacionesCitas.validar_especialidad(especialidad, especialidades_validas)
        if not ok:
            errores.append(msg)
        
        # Validar fecha
        ok, msg = ValidacionesCitas.validar_fecha_cita(fecha)
        if not ok:
            errores.append(msg)
        
        # Validar hora
        ok, msg = ValidacionesCitas.validar_hora_cita(hora)
        if not ok:
            errores.append(msg)
        
        # Validar consultorio (si se proporciona)
        if consultorio:
            ok, msg = ValidacionesCitas.validar_consultorio(consultorio)
            if not ok:
                errores.append(msg)
        
        # Validar estado
        ok, msg = ValidacionesCitas.validar_estado_cita(estado)
        if not ok:
            errores.append(msg)
        
        # Validar comentario (si se proporciona)
        if comentario:
            ok, msg = ValidacionesCitas.validar_comentario(comentario)
            if not ok:
                errores.append(msg)
        
        return len(errores) == 0, errores
