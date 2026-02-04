from typing import Optional, List
from datetime import date
from .paciente import Paciente
from core.database import crear_conexion


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
        self._historias_clinicas: dict[str, dict] = {}  # cc -> historia_clinica





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

            # Guardar en memoria (temporal)
            self._pacientes_memoria[paciente.cc] = paciente

            # Persistir en base de datos integrada (hospital.db)
            try:
                conn = crear_conexion()
                if conn:
                    cur = conn.cursor()
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO pacientes (
                            dni, nombres, apellidos, fecha_nacimiento, direccion, telefono, email, telefono_referencia, historia_clinica, anamnesis
                        ) VALUES (?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            paciente.cc,
                            paciente.nombre,
                            paciente.apellido,
                            paciente.fecha_nacimiento, # Insertar fecha
                            paciente.direccion,
                            paciente.telefono,
                            paciente.email,
                            paciente.telefono_referencia or "",
                            "",
                            ""
                        )
                    )
                    conn.commit()
                    conn.close()
            except Exception:
                # No interrumpir si DB falla; se mantiene en memoria
                pass

            return True, "Paciente registrado exitosamente"
        except Exception as e:
            return False, f"Error al registrar paciente: {str(e)}"

    def registrar_anamnesis(self, cc_paciente: str, datos_anamnesis: dict) -> tuple[bool, str]:
        """
        Caso de uso: registrarAnamnesis (include de registrarPaciente)
        Registra la anamnesis del paciente.
        """
        try:
            import json
            # Verificar que el paciente existe
            paciente = self.consultar_paciente(cc_paciente)
            if not paciente:
                return False, "El paciente no existe"

            # Guardar en memoria (temporal)
            self._anamnesis_memoria[cc_paciente] = datos_anamnesis

            # Persistir en base de datos
            try:
                conn = crear_conexion()
                if conn:
                    # Serializar a JSON string (Crucial para multilínea y caracteres especiales)
                    json_anamnesis = json.dumps(datos_anamnesis, ensure_ascii=False)
                    
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE pacientes SET anamnesis = ? WHERE dni = ?",
                        (json_anamnesis, cc_paciente)
                    )
                    conn.commit()
                    conn.close()
            except Exception as e:
                print(f"Error DB Anamnesis: {e}")
                # No retornamos False aquí para mantener consistencia con memoria si DB falla
            
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

            # Verificar si ya tiene historia clínica
            if cc_paciente in self._historias_clinicas:
                return False, "El paciente ya tiene historia clínica"

            # Crear historia clínica con datos iniciales
            from datetime import datetime
            numero_historia = f"HC-{cc_paciente}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            historia = {
                'numero_historia': numero_historia,
                'cc_paciente': cc_paciente,
                'fecha_creacion': datetime.now(),
                'estado': 'Activa',
                'observaciones': '',
                'consultas': [],
                'diagnosticos': [],
                'tratamientos': []
            }

            # Guardar en memoria
            self._historias_clinicas[cc_paciente] = historia

            # Persistencia en Base de Datos (Historia Clínica)
            try:
                conn = crear_conexion()
                if conn:
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE pacientes SET historia_clinica = ? WHERE dni = ?",
                        (numero_historia, cc_paciente)
                    )
                    conn.commit()
                    conn.close()
            except Exception as e:
                print(f"Error persistiendo HC: {e}")
                # No fallamos la operación global si falla la DB, para mantener UX, pero se loguea.

            return True, f"Historia clínica {numero_historia} creada exitosamente"
        except Exception as e:
            return False, f"Error al crear historia clínica: {str(e)}"

    def consultar_historia_clinica(self, cc_paciente: str) -> Optional[dict]:
        """
        Consulta la historia clínica del paciente.
        """
        try:
            if cc_paciente in self._historias_clinicas:
                return self._historias_clinicas[cc_paciente]
            return None
        except Exception as e:
            print(f"Error al consultar historia clínica: {str(e)}")
            return None

    def actualizar_historia_clinica(self, cc_paciente: str, datos: dict) -> tuple[bool, str]:
        """
        Actualiza la historia clínica del paciente.
        """
        try:
            if cc_paciente not in self._historias_clinicas:
                return False, "El paciente no tiene historia clínica"

            # Actualizar los campos proporcionados
            for key, value in datos.items():
                if key in self._historias_clinicas[cc_paciente]:
                    self._historias_clinicas[cc_paciente][key] = value

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

    def eliminar_paciente(self, cc_paciente: str) -> tuple[bool, str]:
        """
        Elimina un paciente del sistema (Memoria y BD).
        """
        try:
            deleted = False
            
            # 1. Eliminar de memoria
            if cc_paciente in self._pacientes_memoria:
                del self._pacientes_memoria[cc_paciente]
                deleted = True

            if cc_paciente in self._anamnesis_memoria:
                del self._anamnesis_memoria[cc_paciente]

            if cc_paciente in self._historias_clinicas:
                del self._historias_clinicas[cc_paciente]

            # 2. Eliminar de base de datos (Cascada Manual)
            try:
                conn = crear_conexion()
                if conn:
                    cur = conn.cursor()
                    
                    # a) Obtener ID numérico (PK) necesario para otras tablas
                    cur.execute("SELECT id FROM pacientes WHERE dni = ?", (cc_paciente,))
                    row = cur.fetchone()
                    
                    if row:
                        paciente_id = row[0]
                        
                        # b) Borrar Tablas Hijas (nivel 3 - detalles)
                        # Necesitamos IDs de consultas para borrar recetas/ordenes
                        cur.execute("SELECT id FROM consultas WHERE paciente_id = ?", (paciente_id,))
                        consultas_ids = [r[0] for r in cur.fetchall()]
                        
                        if consultas_ids:
                            ids_str = ','.join(map(str, consultas_ids))
                            cur.execute(f"DELETE FROM recetas WHERE consulta_id IN ({ids_str})")
                            cur.execute(f"DELETE FROM ordenes_servicio WHERE consulta_id IN ({ids_str})")

                        # c) Borrar Tablas Hijas (nivel 2)
                        cur.execute("DELETE FROM entregas WHERE paciente_id = ?", (paciente_id,))
                        cur.execute("DELETE FROM hospitalizaciones WHERE paciente_id = ?", (paciente_id,))
                        cur.execute("DELETE FROM consultas WHERE paciente_id = ?", (paciente_id,))
                    
                    # d) Borrar Citas (referencian al DNI)
                    cur.execute("DELETE FROM citas WHERE cc_paciente = ?", (cc_paciente,))
                    
                    # e) Borrar Paciente (Padre)
                    cur.execute("DELETE FROM pacientes WHERE dni = ?", (cc_paciente,))
                    
                    if cur.rowcount > 0:
                        deleted = True
                        
                    conn.commit()
                    conn.close()
            except Exception as db_err:
                print(f"Error borrando de BD: {db_err}")
                if not deleted: # Si no se borró de memoria ni de BD
                     return False, f"Error DB: {str(db_err)}"

            if deleted:
                return True, "Paciente eliminado exitosamente"
            else:
                return False, "El paciente no existe o ya fue eliminado"
                
        except Exception as e:
            return False, f"Error al eliminar paciente: {str(e)}"

    def consultar_paciente(self, cc_paciente: str) -> Optional[Paciente]:
        """
        Caso de uso: consultarPaciente
        Consulta un paciente por su cédula (Memoria -> BD).
        """
        try:
            # 1. Buscar en memoria
            if cc_paciente in self._pacientes_memoria:
                return self._pacientes_memoria[cc_paciente]

            # 2. Buscar en base de datos
            try:
                conn = crear_conexion()
                if conn:
                    cur = conn.cursor()
                    # Nota: Asumiendo columnas estándar. Ajustar si fecha_nacimiento falta en DB
                    row = cur.execute(
                        "SELECT dni, nombres, apellidos, direccion, telefono, email, telefono_referencia FROM pacientes WHERE dni = ?", 
                        (cc_paciente,)
                    ).fetchone()
                    conn.close()
                    
                    if row:
                        paciente = Paciente(
                            cc=row[0],
                            nombre=row[1] or "",
                            apellido=row[2] or "",
                            direccion=row[3] or "",
                            telefono=row[4] or "",
                            email=row[5] or "",
                            telefono_referencia=row[6] or None
                            # Fecha nacimiento no parece estar en la tabla pacientes según registrar_paciente
                        )
                        # Cachear en memoria
                        self._pacientes_memoria[paciente.cc] = paciente
                        return paciente
            except Exception as e:
                print(f"Error consultando DB: {e}")

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
            # Cargar desde BD si disponible y fusionar con memoria
            pacientes: dict[str, Paciente] = dict(self._pacientes_memoria)
            try:
                conn = crear_conexion()
                if conn:
                    cur = conn.cursor()
                    rows = cur.execute(
                        "SELECT dni, nombres, apellidos, direccion, telefono, email, telefono_referencia FROM pacientes"
                    ).fetchall()
                    for dni, nombres, apellidos, direccion, telefono, email, tel_ref in rows:
                        if dni not in pacientes:
                            pacientes[dni] = Paciente(
                                cc=dni,
                                nombre=nombres or "",
                                apellido=apellidos or "",
                                direccion=direccion or "",
                                telefono=telefono or "",
                                email=email or "",
                                telefono_referencia=tel_ref or None
                            )
                    conn.close()
            except Exception:
                pass
            return list(pacientes.values())
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
            import json
            # Buscar en memoria primero
            if cc_paciente in self._anamnesis_memoria:
                return self._anamnesis_memoria[cc_paciente]

            # Buscar en Base de Datos
            try:
                conn = crear_conexion()
                if conn:
                    cur = conn.cursor()
                    row = cur.execute("SELECT anamnesis FROM pacientes WHERE dni = ?", (cc_paciente,)).fetchone()
                    conn.close()
                    
                    if row and row[0]: # Si hay datos
                        try:
                            # Intentar parsear JSON
                            datos = json.loads(row[0])
                            self._anamnesis_memoria[cc_paciente] = datos
                            return datos
                        except json.JSONDecodeError:
                            # Parche de compatibilidad: Retornar como estaba antes (si no era JSON)
                            # O construir una estructura básica si era texto plano
                            return {"motivo_consulta": row[0]}
            except Exception as e:
                print(f"Error consultando anamnesis DB: {e}")

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