from typing import Optional, List
from .paciente import Paciente


class PacienteController:
    """
    Controlador que implementa todos los casos de uso del diagrama UML.
    Maneja la lógica de negocio y la comunicación con la base de datos.
    """

    def __init__(self, db_connection=None):
        """
        Inicializa el controlador.
        db_connection: Conexión a la base de datos (ajustar según tu implementación)
        """
        self.db = db_connection
        # Almacenamiento en memoria (temporal, hasta que se implemente BD)
        self._pacientes_memoria: dict[str, Paciente] = {}  # cc -> Paciente
        self._anamnesis_memoria: dict[str, dict] = {}  # cc -> datos_anamnesis

    def registrar_paciente(self, paciente: Paciente) -> tuple[bool, str]:
        """
        Caso de uso: registrarPaciente
        Registra un nuevo paciente en el sistema.
        """
        es_valido, mensaje = paciente.validar_datos()
        if not es_valido:
            return False, mensaje

        try:
            # Verificar si el paciente ya existe
            if self.consultar_paciente(paciente.cc):
                return False, "El paciente con esta cédula ya existe"

            # Guardar en memoria (temporal)
            self._pacientes_memoria[paciente.cc] = paciente

            # Aquí iría la lógica para guardar en la base de datos
            # if self.db:
            #     self.db.insert('pacientes', paciente.to_dict())

            return True, "Paciente registrado exitosamente"
        except Exception as e:
            return False, f"Error al registrar paciente: {str(e)}"

    def registrar_anamnesis(self, cc_paciente: str, datos_anamnesis: dict) -> tuple[bool, str]:
        """
        Caso de uso: registrarAnamnesis (include de registrarPaciente)
        Registra la anamnesis del paciente.
        """
        try:
            # Verificar que el paciente existe
            paciente = self.consultar_paciente(cc_paciente)
            if not paciente:
                return False, "El paciente no existe"

            # Guardar en memoria (temporal)
            self._anamnesis_memoria[cc_paciente] = datos_anamnesis

            # Aquí iría la lógica para guardar la anamnesis
            # if self.db:
            #     self.db.insert('anamnesis', datos_anamnesis)

            return True, "Anamnesis registrada exitosamente"
        except Exception as e:
            return False, f"Error al registrar anamnesis: {str(e)}"

    def crear_historia_clinica(self, cc_paciente: str) -> tuple[bool, str]:
        """
        Caso de uso: crearHistoriaClinica (include de registrarPaciente)
        Crea la historia clínica del paciente.
        """
        try:
            paciente = self.consultar_paciente(cc_paciente)
            if not paciente:
                return False, "El paciente no existe"

            # Aquí iría la lógica para crear la historia clínica
            # self.db.insert('historia_clinica', {...})

            return True, "Historia clínica creada exitosamente"
        except Exception as e:
            return False, f"Error al crear historia clínica: {str(e)}"

    def actualizar_direccion(self, cc_paciente: str, nueva_direccion: str) -> tuple[bool, str]:
        """
        Caso de uso: actualizarDirección
        Actualiza la dirección del paciente.
        """
        try:
            if not nueva_direccion:
                return False, "La dirección no puede estar vacía"

            # Verificar que el paciente existe en memoria
            if cc_paciente not in self._pacientes_memoria:
                return False, "El paciente no existe"

            # Actualizar en memoria
            self._pacientes_memoria[cc_paciente].direccion = nueva_direccion

            # Aquí iría la lógica para actualizar en la base de datos
            # if self.db:
            #     self.db.update('pacientes', {'direccion': nueva_direccion}, {'cc': cc_paciente})

            return True, "Dirección actualizada exitosamente"
        except Exception as e:
            return False, f"Error al actualizar dirección: {str(e)}"

    def actualizar_telefono(self, cc_paciente: str, nuevo_telefono: str) -> tuple[bool, str]:
        """
        Caso de uso: actualizarTeléfono
        Actualiza el teléfono del paciente.
        """
        try:
            if not nuevo_telefono or len(nuevo_telefono) < 7:
                return False, "El teléfono debe tener al menos 7 dígitos"

            # Verificar que el paciente existe en memoria
            if cc_paciente not in self._pacientes_memoria:
                return False, "El paciente no existe"

            # Actualizar en memoria
            self._pacientes_memoria[cc_paciente].telefono = nuevo_telefono

            # Aquí iría la lógica para actualizar en la base de datos
            # if self.db:
            #     self.db.update('pacientes', {'telefono': nuevo_telefono}, {'cc': cc_paciente})

            return True, "Teléfono actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar teléfono: {str(e)}"

    def actualizar_email(self, cc_paciente: str, nuevo_email: str) -> tuple[bool, str]:
        """
        Caso de uso: actualizarE-mail
        Actualiza el email del paciente.
        """
        try:
            if nuevo_email and '@' not in nuevo_email:
                return False, "El email no es válido"

            # Verificar que el paciente existe en memoria
            if cc_paciente not in self._pacientes_memoria:
                return False, "El paciente no existe"

            # Actualizar en memoria
            self._pacientes_memoria[cc_paciente].email = nuevo_email

            # Aquí iría la lógica para actualizar en la base de datos
            # if self.db:
            #     self.db.update('pacientes', {'email': nuevo_email}, {'cc': cc_paciente})

            return True, "Email actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar email: {str(e)}"

    def actualizar_telefono_referencia(self, cc_paciente: str, nuevo_telefono_ref: str) -> tuple[bool, str]:
        """
        Caso de uso: actualizarTeléfonoDeReferencia
        Actualiza el teléfono de referencia del paciente.
        """
        try:
            # Verificar que el paciente existe en memoria
            if cc_paciente not in self._pacientes_memoria:
                return False, "El paciente no existe"

            # Actualizar en memoria
            self._pacientes_memoria[cc_paciente].telefono_referencia = nuevo_telefono_ref

            # Aquí iría la lógica para actualizar en la base de datos
            # if self.db:
            #     self.db.update('pacientes', {'telefono_referencia': nuevo_telefono_ref}, {'cc': cc_paciente})

            return True, "Teléfono de referencia actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar teléfono de referencia: {str(e)}"

    def consultar_paciente(self, cc_paciente: str) -> Optional[Paciente]:
        """
        Caso de uso: consultarPaciente
        Consulta un paciente por su cédula.
        """
        try:
            # Buscar en memoria primero
            if cc_paciente in self._pacientes_memoria:
                return self._pacientes_memoria[cc_paciente]

            # Aquí iría la lógica para consultar en la base de datos
            # if self.db:
            #     resultado = self.db.query('pacientes', {'cc': cc_paciente})
            #     if resultado:
            #         return Paciente.from_dict(resultado)

            return None
        except Exception as e:
            print(f"Error al consultar paciente: {str(e)}")
            return None

    def consultar_paciente_por_codigo(self, codigo_unico: str) -> Optional[Paciente]:
        """
        Consulta un paciente por su código único.
        """
        try:
            # Buscar en memoria por código único
            for paciente in self._pacientes_memoria.values():
                if paciente.num_unic == codigo_unico:
                    return paciente

            # Aquí iría la lógica para consultar en la base de datos
            # if self.db:
            #     resultado = self.db.query('pacientes', {'num_unic': codigo_unico})
            #     if resultado:
            #         return Paciente.from_dict(resultado)

            return None
        except Exception as e:
            print(f"Error al consultar paciente por código: {str(e)}")
            return None

    def consultar_telefono_referencia(self, cc_paciente: str) -> Optional[str]:
        """
        Caso de uso: consultarTeléfonoDeReferencia (extend de consultarPaciente)
        Consulta el teléfono de referencia del paciente.
        """
        paciente = self.consultar_paciente(cc_paciente)
        return paciente.telefono_referencia if paciente else None

    def consultar_direccion_paciente(self, cc_paciente: str) -> Optional[str]:
        """
        Caso de uso: consultarDirecciónDePaciente (extend de consultarPaciente)
        Consulta la dirección del paciente.
        """
        paciente = self.consultar_paciente(cc_paciente)
        return paciente.direccion if paciente else None

    def consultar_telefono_paciente(self, cc_paciente: str) -> Optional[str]:
        """
        Caso de uso: consultarTeléfonoDePaciente (extend de consultarPaciente)
        Consulta el teléfono del paciente.
        """
        paciente = self.consultar_paciente(cc_paciente)
        return paciente.telefono if paciente else None

    def consultar_anamnesis(self, cc_paciente: str) -> Optional[dict]:
        """
        Caso de uso: consultarAnamnesis (extend de consultarPaciente)
        Consulta la anamnesis del paciente.
        """
        try:
            # Buscar en memoria primero
            if cc_paciente in self._anamnesis_memoria:
                return self._anamnesis_memoria[cc_paciente]

            # Aquí iría la lógica para consultar la anamnesis
            # if self.db:
            #     return self.db.query('anamnesis', {'cc_paciente': cc_paciente})

            return None
        except Exception as e:
            print(f"Error al consultar anamnesis: {str(e)}")
            return None

    def listar_pacientes(self) -> List[Paciente]:
        """
        Lista todos los pacientes registrados.
        """
        try:
            # Retornar pacientes de memoria
            pacientes = list(self._pacientes_memoria.values())

            # Aquí iría la lógica para listar todos los pacientes
            # if self.db:
            #     resultados = self.db.query_all('pacientes')
            #     return [Paciente.from_dict(r) for r in resultados]

            return pacientes
        except Exception as e:
            print(f"Error al listar pacientes: {str(e)}")
            return []