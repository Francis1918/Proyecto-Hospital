from typing import Optional, List
from datetime import date
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
        # Importar función de conexión
        from core.database import crear_conexion
        self.crear_conexion = crear_conexion
        
        # Ya no usamos almacenamiento en memoria
        # Los datos ahora se leen directamente de la base de datos



    def registrar_paciente(self, paciente: Paciente) -> tuple[bool, str]:
        """
        Caso de uso: registrarPaciente
        Registra un nuevo paciente en el sistema.
        """
        # Si recibimos un diccionario, convertirlo a Paciente
        if isinstance(paciente, dict):
            try:
                paciente = Paciente(**paciente)
            except Exception as e:
                return False, f"Error en los datos: {str(e)}"

        es_valido, mensaje = paciente.validar_datos()
        if not es_valido:
            return False, mensaje

        try:
            # Verificar si el paciente ya existe
            if self.consultar_paciente(paciente.cc):
                return False, "El paciente con esta cédula ya existe"

            # Guardar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pacientes (dni, nombres, apellidos, direccion, telefono, email, telefono_referencia)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (paciente.cc, paciente.nombre, paciente.apellido, paciente.direccion, 
                  paciente.telefono, paciente.email, paciente.telefono_referencia))
            
            conn.commit()
            conn.close()

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

            # Convertir dict a texto si es necesario
            if isinstance(datos_anamnesis, dict):
                anamnesis_texto = "\n".join([f"{k}: {v}" for k, v in datos_anamnesis.items()])
            else:
                anamnesis_texto = str(datos_anamnesis)

            # Guardar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pacientes SET anamnesis = ? WHERE dni = ?
            """, (anamnesis_texto, cc_paciente))
            
            conn.commit()
            conn.close()

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

            # Crear historia clínica con datos iniciales
            from datetime import datetime
            numero_historia = f"HC-{cc_paciente}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            historia_texto = f"Historia Clínica: {numero_historia}\nFecha Creación: {datetime.now()}\nEstado: Activa"

            # Actualizar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pacientes SET historia_clinica = ? WHERE dni = ?
            """, (historia_texto, cc_paciente))
            
            conn.commit()
            conn.close()

            return True, f"Historia clínica {numero_historia} creada exitosamente"
        except Exception as e:
            return False, f"Error al crear historia clínica: {str(e)}"

    def consultar_historia_clinica(self, cc_paciente: str) -> Optional[dict]:
        """
        Consulta la historia clínica del paciente.
        """
        try:
            conn = self.crear_conexion()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute("SELECT historia_clinica FROM pacientes WHERE dni = ?", (cc_paciente,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado and resultado[0]:
                return {'historia_clinica': resultado[0]}
            return None
        except Exception as e:
            print(f"Error al consultar historia clínica: {str(e)}")
            return None

    def actualizar_historia_clinica(self, cc_paciente: str, datos: dict) -> tuple[bool, str]:
        """
        Actualiza la historia clínica del paciente.
        """
        try:
            # Verificar que el paciente existe
            if not self.consultar_paciente(cc_paciente):
                return False, "El paciente no tiene historia clínica"

            # Convertir datos a texto si es necesario
            if isinstance(datos, dict):
                historia_texto = "\n".join([f"{k}: {v}" for k, v in datos.items()])
            else:
                historia_texto = str(datos)
            
            # Actualizar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pacientes SET historia_clinica = ? WHERE dni = ?
            """, (historia_texto, cc_paciente))
            
            conn.commit()
            conn.close()

            return True, "Historia clínica actualizada exitosamente"
        except Exception as e:
            return False, f"Error al actualizar historia clínica: {str(e)}"

    def actualizar_direccion(self, cc_paciente: str, nueva_direccion: str) -> tuple[bool, str]:
        """
        Caso de uso: actualizarDirección
        Actualiza la dirección del paciente.
        """
        try:
            if not nueva_direccion:
                return False, "La dirección no puede estar vacía"

            # Verificar que el paciente existe
            if not self.consultar_paciente(cc_paciente):
                return False, "El paciente no existe"

            # Actualizar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pacientes SET direccion = ? WHERE dni = ?
            """, (nueva_direccion, cc_paciente))
            
            conn.commit()
            conn.close()

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

            # Verificar que el paciente existe
            if not self.consultar_paciente(cc_paciente):
                return False, "El paciente no existe"

            # Actualizar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pacientes SET telefono = ? WHERE dni = ?
            """, (nuevo_telefono, cc_paciente))
            
            conn.commit()
            conn.close()

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

            # Verificar que el paciente existe
            if not self.consultar_paciente(cc_paciente):
                return False, "El paciente no existe"

            # Actualizar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pacientes SET email = ? WHERE dni = ?
            """, (nuevo_email, cc_paciente))
            
            conn.commit()
            conn.close()

            return True, "Email actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar email: {str(e)}"

    def actualizar_telefono_referencia(self, cc_paciente: str, nuevo_telefono_ref: str) -> tuple[bool, str]:
        """
        Caso de uso: actualizarTeléfonoDeReferencia
        Actualiza el teléfono de referencia del paciente.
        """
        try:
            # Verificar que el paciente existe
            if not self.consultar_paciente(cc_paciente):
                return False, "El paciente no existe"

            # Actualizar en la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pacientes SET telefono_referencia = ? WHERE dni = ?
            """, (nuevo_telefono_ref, cc_paciente))
            
            conn.commit()
            conn.close()

            return True, "Teléfono de referencia actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar teléfono de referencia: {str(e)}"

    def eliminar_paciente(self, cc_paciente: str) -> tuple[bool, str]:
        """
        Elimina un paciente del sistema.
        """
        try:
            # Verificar que el paciente existe
            if not self.consultar_paciente(cc_paciente):
                return False, "El paciente no existe"

            # Eliminar de la base de datos
            conn = self.crear_conexion()
            if not conn:
                return False, "Error de conexión a la base de datos"
            
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pacientes WHERE dni = ?", (cc_paciente,))
            
            conn.commit()
            conn.close()

            return True, "Paciente eliminado exitosamente"
        except Exception as e:
            return False, f"Error al eliminar paciente: {str(e)}"

    def consultar_paciente(self, cc_paciente: str) -> Optional[Paciente]:
        """
        Caso de uso: consultarPaciente
        Consulta un paciente por su cédula.
        """
        try:
            conn = self.crear_conexion()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT dni, nombres, apellidos, direccion, telefono, email, telefono_referencia
                FROM pacientes WHERE dni = ?
            """, (cc_paciente,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                return Paciente(
                    cc=resultado[0],
                    nombre=resultado[1],
                    apellido=resultado[2],
                    direccion=resultado[3],
                    telefono=resultado[4],
                    email=resultado[5],
                    telefono_referencia=resultado[6]
                )
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

    def obtener_todos_pacientes(self) -> List[Paciente]:
        """
        Obtiene la lista de todos los pacientes registrados.
        """
        try:
            conn = self.crear_conexion()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT dni, nombres, apellidos, direccion, telefono, email, telefono_referencia
                FROM pacientes
            """)
            
            resultados = cursor.fetchall()
            conn.close()
            
            pacientes = []
            for row in resultados:
                pacientes.append(Paciente(
                    cc=row[0],
                    nombre=row[1],
                    apellido=row[2],
                    direccion=row[3],
                    telefono=row[4],
                    email=row[5],
                    telefono_referencia=row[6]
                ))
            return pacientes
        except Exception as e:
            print(f"Error al obtener pacientes: {str(e)}")
            return []

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
            conn = self.crear_conexion()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute("SELECT anamnesis FROM pacientes WHERE dni = ?", (cc_paciente,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado and resultado[0]:
                # Convertir texto a dict si es posible
                anamnesis_texto = resultado[0]
                if anamnesis_texto:
                    return {'anamnesis': anamnesis_texto}
            return None
        except Exception as e:
            print(f"Error al consultar anamnesis: {str(e)}")
            return None

    def listar_pacientes(self) -> List[Paciente]:
        """
        Lista todos los pacientes registrados.
        """
        # Usa el mismo método que obtener_todos_pacientes
        return self.obtener_todos_pacientes()