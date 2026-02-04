from __future__ import annotations
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Optional, Tuple

import sqlite3
import random
import string

from core.database import crear_conexion
from Pacientes import PacienteController
from .models import CitaMedica, Notificacion
from .validaciones import ValidacionesCitas


class CitasMedicasController:
    """
    Controlador del módulo de Citas Médicas (persistencia en memoria).
    """

    def __init__(self, paciente_controller: Optional[PacienteController] = None):
        self.pacientes = paciente_controller or PacienteController()
        self._notificaciones: List[Notificacion] = []
        self._agenda_medicos = {}
        self._verificar_tabla_citas()
        
    def _verificar_tabla_citas(self):
        """
        Crea la tabla de citas con integridad referencial.
        Resuelve el Punto 3 evitando que existan citas sin médico o paciente real.
        """
        conn = crear_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                # Eliminamos la redundancia de nombres y usamos IDs vinculados
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS citas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        codigo TEXT UNIQUE NOT NULL,
                        cc_paciente TEXT NOT NULL,
                        id_medico INTEGER NOT NULL,  -- Vinculación directa al módulo Médicos
                        fecha TEXT NOT NULL,
                        hora TEXT NOT NULL,
                        consultorio TEXT,
                        estado TEXT DEFAULT 'Programada',
                        comentario TEXT,
                        -- Estas reglas evitan las 'Citas Huérfanas' a nivel de Base de Datos
                        FOREIGN KEY (cc_paciente) REFERENCES pacientes(dni) ON DELETE CASCADE,
                        FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS horarios_medicos (
                        id_medico INTEGER PRIMARY KEY,
                        hora_inicio INTEGER DEFAULT 9,
                        hora_fin INTEGER DEFAULT 17,
                        FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE
                    )
                """)
                conn.commit()
            except Exception as e:
                print(f"Error al estructurar tabla citas: {e}")
            finally:
                conn.close()

    # ---------------------------
    # Validaciones
    # ---------------------------
    @staticmethod
    def validar_formato_cedula(cc: str) -> Tuple[bool, str]:
        """
        Valida el formato de la cédula usando el algoritmo ecuatoriano.
        Evita errores de búsqueda en SQL por formatos incorrectos.
        MEJORA: Ahora valida la cédula de acuerdo al estándar ecuatoriano.
        """
        # Primero hacer validación de formato básica
        ok, msg = ValidacionesCitas.validar_cedula_formato(cc)
        if not ok:
            return False, msg
        
        # Luego validar con el algoritmo ecuatoriano completo
        return ValidacionesCitas.validar_cedula_ecuador(cc)

    @staticmethod
    def _generar_codigo() -> str:
        """
        Genera un identificador alfanumérico único para la cita médica.
        Formato: CM-XXXXXX
        """
        caracteres = string.ascii_uppercase + string.digits
        cuerpo = "".join(random.choices(caracteres, k=6))
        return f"CM-{cuerpo}"

    # ---------------------------
    # Catálogo y agenda
    # ---------------------------
    def obtener_especialidades(self) -> List[str]:
        """
        Trae las especialidades únicas de los médicos activos.
        Útil para filtrar opciones en el formulario de agendamiento.
        """
        conn = crear_conexion()
        especialidades = []
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            # Añadimos ORDER BY para que en la UI aparezcan organizadas (A-Z)
            sql = "SELECT DISTINCT especialidad FROM medicos WHERE estado = 'Activo' ORDER BY especialidad"
            cursor.execute(sql)
            
            # Extraemos el primer elemento de cada tupla resultante
            especialidades = [row[0] for row in cursor.fetchall() if row[0]]
            
        except Exception as e:
            print(f"Error técnico al obtener especialidades: {e}")
        finally:
            conn.close()
            
        return especialidades

    def obtener_medicos_por_especialidad(self, especialidad: str) -> List[str]:
        """
        Trae ID y Nombre de médicos activos por especialidad.
        Garantiza que usemos el ID correcto para evitar citas huérfanas. [2026-02-01]
        """
        conn = crear_conexion()
        if not conn: return []
        try:
            cursor = conn.cursor()
            sql = """
                SELECT id, nombres || ' ' || apellidos 
                FROM medicos 
                WHERE especialidad = ? AND estado = 'Activo'
                ORDER BY nombres ASC
            """
            cursor.execute(sql, (especialidad,))
            return cursor.fetchall() # Esto ya devuelve [(1, 'Dr...'), (2, 'Dr...')]
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            conn.close()

    def obtener_todos_medicos(self) -> List[str]:
        """
        Obtiene la lista completa de médicos activos con sus identificadores.
        Retorna una lista de diccionarios para facilitar el manejo en la UI. [2026-02-01]
        """
        conn = crear_conexion()
        medicos = []
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            # Seleccionamos ID, nombre completo y especialidad
            # El orden del SELECT previene la 'Incoherencia de Columnas' (Punto 1)
            sql = """
                SELECT id, nombres || ' ' || apellidos, especialidad 
                FROM medicos 
                WHERE estado = 'Activo'
                ORDER BY nombres ASC
            """
            cursor.execute(sql)
            
            for row in cursor.fetchall():
                medicos.append({
                    "id": row[0],
                    "nombre_completo": row[1],
                    "especialidad": row[2]
                })
                
        except Exception as e:
            print(f"Error técnico al recuperar lista de médicos: {e}")
        finally:
            conn.close()
            
        return medicos

    def obtener_consultorio_medico(self, id_medico: int) -> str:
        """
        Busca el consultorio asignado al médico usando su ID único.
        Garantiza precisión absoluta incluso si hay médicos con nombres similares.
        """
        conn = crear_conexion()
        consultorio = "Consultorio General" # Valor por defecto
        
        if not conn:
            return consultorio

        try:
            cursor = conn.cursor()
            # Buscamos por ID, que es la forma más eficiente en SQL
            cursor.execute("SELECT direccion FROM medicos WHERE id = ?", (id_medico,))
            
            row = cursor.fetchone()
            if row and row[0]:
                consultorio = row[0]
                
        except Exception as e:
            print(f"Error técnico al recuperar consultorio: {str(e)}")
        finally:
            conn.close()
        
        return consultorio

    def obtener_agenda_medico(self, id_medico: int) -> Tuple[int, int]:
        """
        Obtiene el rango de atención (hora inicio, hora fin) del médico.
        Si no hay un horario específico en DB, retorna el estándar (09:00 - 17:00).
        """
        # 1. Primero checamos en memoria (caché rápida)
        if id_medico in self._agenda_medicos:
            return self._agenda_medicos[id_medico]

        # 2. Si no está en memoria, buscamos en la nueva tabla
        conn = crear_conexion()
        horario = (9, 17) # Por defecto
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT hora_inicio, hora_fin FROM horarios_medicos WHERE id_medico = ?", (id_medico,))
                row = cursor.fetchone()
                if row:
                    horario = (row[0], row[1])
                    self._agenda_medicos[id_medico] = horario # Guardamos en memoria
            finally:
                conn.close()
        return horario

    def registrar_agenda_medico(self, id_medico: int, hora_inicio: int, hora_fin: int) -> Tuple[bool, str]:
        """
        Registra o actualiza el horario de atención de un médico en la base de datos.
        Resuelve el problema de pérdida de datos al cerrar la sesión. [2026-02-01]
        """
        # 1. Validación lógica de horas
        if not (0 <= hora_inicio <= 23 and 1 <= hora_fin <= 24 and hora_inicio < hora_fin):
            return False, "Error: Rango de horas inválido (Ej: 9 a 17)."

        conn = crear_conexion()
        if not conn:
            return False, "Error de conexión."

        try:
            cursor = conn.cursor()
            # Usamos INSERT OR REPLACE para no duplicar filas por médico
            sql = """
                INSERT OR REPLACE INTO horarios_medicos (id_medico, hora_inicio, hora_fin)
                VALUES (?, ?, ?)
            """
            cursor.execute(sql, (id_medico, hora_inicio, hora_fin))
            conn.commit()
            
            # Sincronizamos la memoria
            self._agenda_medicos[id_medico] = (hora_inicio, hora_fin)
            return True, "Horario guardado correctamente en la tabla de horarios."
        except Exception as e:
            return False, f"Error al guardar horario: {e}"
        finally:
            conn.close()

    def obtener_horarios_disponibles(self, id_medico: int, fecha: date) -> List[time]:
        """
        Calcula los huecos libres cruzando el rango laboral con las citas ocupadas.
        Usa ID_MEDICO para evitar colisiones entre nombres iguales. [2026-02-01]
        """
        # 1. Obtener el rango laboral (definido en el paso anterior)
        # Si no tiene uno registrado, usamos el estándar 9-17
        start, end = self.obtener_agenda_medico(id_medico)
        horas_potenciales = [time(h, 0) for h in range(start, end)]

        ocupadas = set()
        conn = crear_conexion()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            # Buscamos por id_medico (numérico) y excluimos citas canceladas
            sql = """
                SELECT hora FROM citas 
                WHERE id_medico = ? AND fecha = ? AND estado != 'Cancelada'
            """
            cursor.execute(sql, (id_medico, fecha.isoformat()))
            
            for row in cursor.fetchall():
                try:
                    # row[0] es la hora. Garantizamos el formato HH:MM
                    # Esto evita errores si el string en DB está mal formado
                    hora_str = row[0]
                    hora_db = datetime.strptime(hora_str, "%H:%M").time()
                    ocupadas.add(hora_db)
                except ValueError:
                    print(f"Aviso: Formato de hora inválido en DB: {row[0]}")
                    
        except Exception as e:
            print(f"Error técnico al consultar disponibilidad: {e}")
            return []
        finally:
            conn.close()
                
        # Retornamos solo las horas que no están en el set de ocupadas
        return [h for h in horas_potenciales if h not in ocupadas]

    def     consultar_agenda(self, id_medico: int, fecha: date) -> List[CitaMedica]:
        """
        Consulta la agenda de un médico garantizando la integridad de las columnas.
        Fundamental para el Módulo 4 (Consulta Externa). [2026-02-01]
        """
        conn = crear_conexion()
        citas = []
        
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            # Mapeo Explícito: Evitamos SELECT * para prevenir el Punto 1.
            # Traemos el nombre del paciente mediante JOIN para asegurar datos frescos.
            sql = """
            SELECT 
                c.codigo,              -- 0
                c.cc_paciente,         -- 1
                p.nombres || ' ' || p.apellidos AS nombre_paciente, -- 2
                m.especialidad,        -- 3
                m.nombres || ' ' || m.apellidos AS medico,          -- 4
                c.fecha,               -- 5
                c.hora,                -- 6
                c.consultorio,         -- 7
                c.estado               -- 8
            FROM citas c
            INNER JOIN pacientes p ON c.cc_paciente = p.dni
            INNER JOIN medicos m ON c.id_medico = m.id
            WHERE c.id_medico = ? AND c.fecha = ?
            ORDER BY c.hora ASC
        """
            cursor.execute(sql, (id_medico, fecha.isoformat()))
            
            for row in cursor.fetchall():
                # Procesamiento flexible de Fecha
                f_val = row[5]
                if isinstance(f_val, str):
                    f_val = datetime.strptime(f_val.split('T')[0], '%Y-%m-%d').date()

                # Procesamiento flexible de Hora (Evita el error de match format)
                h_val = row[6]
                if isinstance(h_val, str):
                    # Intentamos con segundos, si falla, probamos sin segundos
                    try:
                        h_val = datetime.strptime(h_val, '%H:%M:%S').time()
                    except ValueError:
                        h_val = datetime.strptime(h_val, '%H:%M').time()

                cita = CitaMedica(
                    codigo=row[0],
                    cc_paciente=row[1],
                    nombre_paciente=row[2],
                    especialidad=row[3],
                    medico=row[4],
                    fecha=f_val,
                    hora=h_val,
                    consultorio=row[7],
                    estado=row[8],
                    id_medico=id_medico
                )
                citas.append(cita)
        except Exception as e:
            print(f"Error técnico al consultar agenda: {e}")
        finally:
            conn.close()
        return citas

    # ---------------------------
    # CRUD Citas
    # ---------------------------
    def solicitar_cita(self, cc: str, id_medico: int, fecha: date, hora: time) -> Tuple[bool, str, Optional[CitaMedica]]:
        """
        Orquesta el agendamiento validando integridad referencial y disponibilidad.
        Resuelve el Punto 3 (Citas Huérfanas) usando ID de médico. [2026-02-01]
        """
        # 1. Validación de Cédula (Filtro rápido)
        ok, msg = self.validar_formato_cedula(cc)
        if not ok:
            return False, msg, None

        # 2. Verificamos Paciente (Usa el controlador inyectado)
        paciente = self.pacientes.consultar_paciente(cc)
        if not paciente:
            return False, "Paciente no registrado. Debe crearlo primero.", None

        # 3. Verificamos Disponibilidad Real
        # Esto ya valida si el médico existe y si el horario está libre
        disponibles = self.obtener_horarios_disponibles(id_medico, fecha)
        if not disponibles:
            return False, "El médico no tiene horarios para esta fecha.", None

        if hora not in disponibles:
            return False, f"El horario {hora.strftime('%H:%M')} ya fue ocupado.", None

        # 4. Generación de Código Único
        codigo = self._generar_codigo()
        
        conn = crear_conexion()
        if not conn: return False, "Error de conexión", None

        try:
            cursor = conn.cursor()
            # RECUPERAR DATOS DEL MÉDICO PARA EL OBJETO CitaMedica
            cursor.execute("SELECT nombres || ' ' || apellidos, especialidad, direccion FROM medicos WHERE id = ?", (id_medico,))
            res_medico = cursor.fetchone()
            if not res_medico:
                return False, "Médico no encontrado", None
            
            nombre_medico_str, especialidad_str, consultorio = res_medico

            # INSERTAR EN DB
            codigo = self._generar_codigo()
            sql = """
                INSERT INTO citas (codigo, cc_paciente, id_medico, fecha, hora, consultorio, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'Confirmada')
            """
            cursor.execute(sql, (codigo, cc, id_medico, fecha.isoformat(), hora.strftime("%H:%M"), consultorio))
            conn.commit()

            # CREAR OBJETO CON LOS DATOS RECUPERADOS
            cita = CitaMedica(
                codigo=codigo, 
                cc_paciente=cc, 
                nombre_paciente=f"{paciente.nombre} {paciente.apellido}",
                especialidad=especialidad_str, 
                medico=nombre_medico_str,
                fecha=fecha, 
                hora=hora,
                consultorio=consultorio, 
                estado="Confirmada",
                id_medico=id_medico
            )
            self._notificar_cita_programada(cita)
            return True, f"Cita {codigo} agendada con éxito.", cita
        except Exception as e:
            return False, f"Error técnico al agendar cita: {str(e)}", None
        finally:
            conn.close()

    def consultar_cita_por_codigo(self, codigo: str) -> Optional[CitaMedica]:
        """
        Busca una cita específica por su código CM-XXXXXX.
        Usa mapeo explícito para evitar desplazamientos de columnas. [2026-02-01]
        """
        codigo_limpio = (codigo or "").strip()
        conn = crear_conexion()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            # Especificamos las columnas y traemos el nombre del médico mediante JOIN
            sql = """
                SELECT c.codigo, c.cc_paciente, c.fecha, c.hora, c.consultorio, c.estado,
                            m.nombres || ' ' || m.apellidos, p.nombres || ' ' || p.apellidos,
                            m.especialidad, c.id_medico
                FROM citas c
                JOIN medicos m ON c.id_medico = m.id
                JOIN pacientes p ON c.cc_paciente = p.dni
                WHERE c.codigo = ?
            """
            cursor.execute(sql, (codigo_limpio,))
            row = cursor.fetchone()
            
            if row:
                # El orden del SELECT garantiza que row[0] siempre sea el código
                try:
                    # Procesar fecha con validación
                    fecha_val = row[2]
                    if isinstance(fecha_val, str):
                        fecha_val = date.fromisoformat(fecha_val)
                    
                    # Procesar hora con validación
                    hora_val = row[3]
                    if isinstance(hora_val, str):
                        try:
                            hora_val = datetime.strptime(hora_val, "%H:%M:%S").time()
                        except ValueError:
                            hora_val = datetime.strptime(hora_val, "%H:%M").time()
                    
                    return CitaMedica(
                        codigo=row[0],
                        cc_paciente=row[1],
                        nombre_paciente=row[7],
                        medico=row[6],
                        especialidad=row[8],
                        id_medico=row[9],
                        fecha=fecha_val,
                        hora=hora_val,
                        consultorio=row[4],
                        estado=row[5]
                    )
                except (ValueError, TypeError) as parse_err:
                    print(f"Error al parsear datos de cita {codigo_limpio}: {parse_err}")
                    return None
                
        except Exception as e:
            print(f"Error técnico al consultar cita {codigo_limpio}: {e}")
        finally:
            conn.close()
            
        return None

    def consultar_citas_por_paciente(self, cc: str) -> List[CitaMedica]:
        """
        Recupera el historial de citas de un paciente con datos vinculados.
        Garantiza la integridad mediante JOINs y evita errores de índices. [2026-02-01]
        """
        cc = (cc or "").strip()
        conn = crear_conexion()
        citas = []
        
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            # Mapeo Explícito: Definimos exactamente qué columnas queremos.
            # Traemos nombres actualizados de médicos y pacientes.
            # CRÍTICO: Agregamos c.id_medico en la posición 9 (faltaba antes)
            sql = """
                SELECT c.codigo, c.cc_paciente, c.fecha, c.hora, c.consultorio, c.estado,
                       m.nombres || ' ' || m.apellidos AS nombre_medico,
                       m.especialidad,
                       p.nombres || ' ' || p.apellidos AS nombre_paciente,
                       c.id_medico
                FROM citas c
                JOIN medicos m ON c.id_medico = m.id
                JOIN pacientes p ON c.cc_paciente = p.dni
                WHERE c.cc_paciente = ?
                ORDER BY c.fecha DESC, c.hora DESC
            """
            cursor.execute(sql, (cc,))
            
            for row in cursor.fetchall():
                # El orden del SELECT garantiza que el mapeo sea siempre el mismo
                try:
                    # Procesar fecha con validación
                    fecha_val = row[2]
                    if isinstance(fecha_val, str):
                        fecha_val = date.fromisoformat(fecha_val)
                    
                    # Procesar hora con validación (puede venir como string o time)
                    hora_val = row[3]
                    if isinstance(hora_val, str):
                        try:
                            hora_val = datetime.strptime(hora_val, "%H:%M:%S").time()
                        except ValueError:
                            hora_val = datetime.strptime(hora_val, "%H:%M").time()
                    
                    citas.append(CitaMedica(
                        codigo=row[0],
                        cc_paciente=row[1],
                        fecha=fecha_val,
                        hora=hora_val,
                        consultorio=row[4],
                        estado=row[5],
                        medico=row[6],   # Datos del JOIN
                        especialidad=row[7],    # Datos del JOIN
                        nombre_paciente=row[8],  # Datos del JOIN
                        id_medico=row[9]  # CRÍTICO: Ahora se obtiene correctamente de la BD
                    ))
                except (IndexError, ValueError, TypeError) as parse_err:
                    print(f"Advertencia: Error al procesar fila de cita: {parse_err}. Fila: {row}")
                    continue
        except Exception as e:
            print(f"Error técnico al consultar historial del paciente {cc}: {e}")
        finally:
            conn.close()
            
        return citas

    def modificar_cita(self, codigo: str, nueva_fecha: date, nueva_hora: time) -> Tuple[bool, str, Optional[CitaMedica]]:
        """
        Reprograma una cita existente validando disponibilidad y políticas de tiempo.
        Previene la corrupción de datos al usar IDs únicos.
        """
        # 1. Recuperamos la cita actual para tener el ID del médico
        cita = self.consultar_cita_por_codigo(codigo)
        if not cita:
            return False, "No se encontró la cita especificada.", None

        if cita.estado == "Cancelada":
            return False, "No se puede modificar una cita que ya ha sido cancelada.", None

        # 2. Política de Preaviso (12h) - Validación de Negocio
        momento_cita = datetime.combine(cita.fecha, cita.hora)
        if datetime.now() > (momento_cita - timedelta(hours=12)):
            return False, "Política de preaviso: Las citas solo pueden modificarse con más de 12 horas de antelación.", None

        # 3. Validación de Disponibilidad (Solo si cambió el horario)
        if not (nueva_fecha == cita.fecha and nueva_hora == cita.hora):
            # Usamos cita.id_medico (garantizado tras el JOIN en consultar_cita_por_codigo)
            disponibles = self.obtener_horarios_disponibles(cita.id_medico, nueva_fecha)
            if nueva_hora not in disponibles:
                return False, "El médico no tiene disponibilidad en el nuevo horario seleccionado.", None

        conn = crear_conexion()
        if not conn:
            return False, "Fallo de conexión a la base de datos.", None
            
        try:
            cursor = conn.cursor()
            # 4. Actualización persistente
            sql = "UPDATE citas SET fecha = ?, hora = ?, estado = 'Reprogramada' WHERE codigo = ?"
            cursor.execute(sql, (nueva_fecha.isoformat(), nueva_hora.strftime("%H:%M"), codigo))
            
            conn.commit()

            # 5. Actualización del objeto local para la UI
            cita.fecha = nueva_fecha
            cita.hora = nueva_hora
            cita.estado = "Reprogramada"

            # 6. Notificaciones centralizadas
            self._notificar_cita_programada(cita) 
            
            return True, f"Cita {codigo} reprogramada exitosamente.", cita

        except Exception as e:
            return False, f"Error técnico en la actualización: {str(e)}", None
        finally:
            conn.close()

    def cancelar_cita(self, codigo: str) -> Tuple[bool, str]:
        """
        Cancela una cita médica actualizando su estado en la DB.
        Mantiene la integridad del historial clínico sin eliminar registros.
        """
        # 1. Recuperar la cita para validar estado y tiempos
        cita = self.consultar_cita_por_codigo(codigo)
        if not cita:
            return False, "No se encontró la cita especificada."

        if cita.estado == "Cancelada":
            return False, "La cita ya se encuentra en estado cancelada."

        # 2. Validación de Política de Preaviso (12h)
        # Usamos combine para comparar contra el tiempo actual del sistema
        momento_cita = datetime.combine(cita.fecha, cita.hora)
        if datetime.now() > (momento_cita - timedelta(hours=12)):
            return False, "No es posible cancelar: faltan menos de 12 horas para la cita."

        conn = crear_conexion()
        if not conn:
            return False, "Error de conexión con la base de datos."
            
        try:
            cursor = conn.cursor()
            # 3. Actualización persistente por Código Único
            sql = "UPDATE citas SET estado = 'Cancelada' WHERE codigo = ?"
            cursor.execute(sql, (codigo.strip(),))
            
            if cursor.rowcount == 0:
                return False, "No se pudo actualizar el estado de la cita."
                
            conn.commit()

            # 4. Notificaciones centralizadas (Punto 2 del plan)
            # Notificamos tanto al paciente como al médico
            self._notificar_cancelacion(cita) 
            
            return True, f"Cita {codigo} cancelada exitosamente."

        except Exception as e:
            return False, f"Error técnico al procesar la cancelación: {str(e)}"
        finally:
            conn.close()

    # ---------------------------
    # Recepción: registrar estado
    # ---------------------------
    def registrar_estado_cita(
        self,
        codigo: str,
        nuevo_estado: str,
        hora_llegada: Optional[time] = None,
        comentario: str = ""
    ) -> Tuple[bool, str, Optional[CitaMedica]]:
        """
        Registra la asistencia del paciente. 
        Actualiza el flujo de trabajo para el médico en el Módulo 4.
        """
        # 1. Recuperamos la cita usando el método blindado
        cita = self.consultar_cita_por_codigo(codigo)
        if not cita:
            return False, "No se encontró la cita especificada.", None

        if cita.estado == "Cancelada":
            return False, "Operación inválida: La cita ya fue cancelada.", None

        # 2. Validaciones de Negocio
        estados_validos = {"Asistió", "Ausente", "Tardanza"}
        if nuevo_estado not in estados_validos:
            return False, f"Error: '{nuevo_estado}' no es un estado válido de recepción.", None
        
        # Evitamos registros de asistencia para fechas que no son hoy
        if cita.fecha != date.today() and nuevo_estado == "Asistió":
            return False, f"Fecha incorrecta: La cita es para el {cita.fecha.strftime('%d/%m/%Y')}.", None

        conn = crear_conexion()
        if not conn:
            return False, "Fallo de conexión a la base de datos.", None
            
        try:
            cursor = conn.cursor()
            h_llegada_str = hora_llegada.strftime("%H:%M") if hora_llegada else None
            
            # 3. Actualización persistente
            sql = """
                UPDATE citas 
                SET estado = ?, hora_llegada = ?, comentario = ?
                WHERE codigo = ?
            """
            cursor.execute(sql, (nuevo_estado, h_llegada_str, comentario, codigo.strip()))
            
            if cursor.rowcount == 0:
                return False, "No se pudo actualizar el registro en la base de datos.", None
                
            conn.commit()

            # 4. Sincronización del objeto para la UI
            cita.estado = nuevo_estado
            cita.hora_llegada = hora_llegada
            cita.comentario = comentario

            # 5. Notificación al Médico (Trigger para el Módulo 4)
            self._notificar_estado_recepcion(cita)

            return True, f"Asistencia registrada: {nuevo_estado}.", cita

        except Exception as e:
            return False, f"Error técnico en base de datos: {str(e)}", None
        finally:
            conn.close()

    # ---------------------------
    # Notificaciones
    # ---------------------------
    def obtener_historial_notificaciones(self) -> List[Notificacion]:
        """
        Recupera el log de comunicaciones del sistema.
        Garantiza la trazabilidad de los avisos enviados a pacientes y médicos.
        """
        conn = crear_conexion()
        historial = []
        
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            # Usamos LEFT JOIN para buscar el nombre ya sea en pacientes o en médicos
            sql = """
                SELECT 
                    n.destinatario, 
                    n.mensaje, 
                    n.canal, 
                    n.fecha_envio,
                    n.estado,
                    COALESCE(p.nombres || ' ' || p.apellidos, m.nombres || ' ' || m.apellidos, 'Desconocido') AS nombre_completo,
                    CASE 
                        WHEN p.dni IS NOT NULL THEN 'Paciente'
                        WHEN m.id IS NOT NULL THEN 'Médico'
                        ELSE 'Sistema'
                    END AS tipo_usuario
                FROM notificaciones n
                LEFT JOIN pacientes p ON n.destinatario = p.dni
                LEFT JOIN medicos m ON n.destinatario = CAST(m.id AS TEXT)
                ORDER BY n.fecha_envio DESC
            """
            cursor.execute(sql)
            
            for row in cursor.fetchall():
                try:
                    # Limpieza de fecha para evitar el error de microsegundos
                    fecha_str = row[3][:19] if row[3] else datetime.now().isoformat()[:19]
                    fecha_valida = datetime.fromisoformat(fecha_str)
                    
                    # Creamos el objeto Notificacion 
                    # (Asegúrate de que tu modelo soporte 'nombre_destinatario' y 'tipo')
                    n = Notificacion(
                        destinatario=row[0],
                        mensaje=row[1],
                        canal=row[2],
                        enviada_en=fecha_valida,
                        estado=row[4]
                    )
                    # Atributos dinámicos para la UI
                    n.nombre_destinatario = row[5]
                    n.tipo_usuario = row[6]
                    
                    historial.append(n)
                except Exception as e:
                    print(f"Error en registro: {e}")
        finally:
            conn.close()
        return historial

    def _notificar(self, destinatario: str, canal: str, mensaje: str,
                  estado: str = "Enviada", detalle_error: str = ""):
        """
        Registra la comunicación en la base de datos de forma persistente.
        Método de soporte interno para trazabilidad y auditoría.
        """
        conn = crear_conexion()
        if not conn:
            # Si falla la conexión, al menos logueamos en consola
            print(f"ALERTA: Sin conexión para registrar notificación a {destinatario}")
            return

        try:
            cursor = conn.cursor()
            # Usamos el formato ISO para la fecha, facilitando la lectura 
            # desde obtener_historial_notificaciones
            fecha_actual = datetime.now().replace(microsecond=0).isoformat()
            
            # Definimos columnas explícitas para evitar el Punto 1
            sql = """
                INSERT INTO notificaciones 
                (destinatario, canal, mensaje, estado, detalle_error, fecha_envio)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (
                destinatario, canal, mensaje, estado, detalle_error, fecha_actual
            ))
            
            conn.commit()
            
        except Exception as e:
            # En notificaciones, un error no debe tumbar la app, pero sí reportarse
            print(f"Error crítico al guardar registro de notificación: {e}")
        finally:
            conn.close()

    def _notificar_cita_programada(self, cita: CitaMedica):
        """
        Sincronización de atributos con el modelo Paciente.
        Asegura que el canal de comunicación sea detectado correctamente.
        """
        # 1. Consultamos al paciente usando el controlador inyectado
        paciente = self.pacientes.consultar_paciente(cita.cc_paciente)

        canal = "interno" # Por defecto
        if paciente:
            # CORRECCIÓN: Usamos 'email' y 'telefono' (como están en tu DB/Clase)
            # No usamos 'telefono1' ni 'telefono2' porque no existen en tu modelo
            if getattr(paciente, "email", None) and "@" in paciente.email:
                canal = "email"
            elif getattr(paciente, "telefono", None) and len(str(paciente.telefono)) > 5:
                canal = "sms"

        # 2. Construcción del mensaje para el paciente
        msg_paciente = (
            f"Confirmación Cita {cita.codigo}: Especialidad {cita.especialidad} "
            f"con el Dr(a). {cita.medico} el día {cita.fecha.strftime('%d/%m/%Y')} "
            f"a las {cita.hora.strftime('%H:%M')}. Consultorio: {cita.consultorio}."
        )

        # 3. Registro de la notificación en el historial
        # Notificación al Paciente
        self._notificar(
            destinatario=cita.cc_paciente, 
            canal=canal, 
            mensaje=msg_paciente
        )
        
        # Notificación al Médico (Usando su ID como destinatario técnico)
        self._notificar(
            destinatario=str(cita.id_medico), 
            canal="interno", 
            mensaje=f"Nueva cita agendada: {cita.nombre_paciente} para el {cita.fecha}."
        )
        
    def _notificar_cancelacion(self, cita: CitaMedica):
            """
            Notifica la cancelación de la cita al paciente y al médico.
            """
            msg = f"Aviso: Su cita {cita.codigo} del {cita.fecha.strftime('%d/%m/%Y')} ha sido CANCELADA."
            
            # Notificar al paciente
            self._notificar(destinatario=cita.cc_paciente, canal="sistema", mensaje=msg)
            
            # Notificar al médico
            self._notificar(
                destinatario=str(cita.id_medico), 
                canal="interno", 
                mensaje=f"Cita cancelada por el paciente: {cita.nombre_paciente} ({cita.codigo})."
            )

    def _notificar_estado_recepcion(self, cita: CitaMedica):
            """
            Notifica al médico que el paciente ha llegado a la recepción.
            """
            msg_medico = f"Paciente en sala: {cita.nombre_paciente} ha llegado para su cita de las {cita.hora.strftime('%H:%M')}."
            
            self._notificar(
                destinatario=str(cita.id_medico), 
                canal="interno", 
                mensaje=msg_medico
            )