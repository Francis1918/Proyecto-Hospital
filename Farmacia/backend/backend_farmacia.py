import sqlite3
from sqlite3 import Error
from core.database import crear_conexion

class GestorFarmacia:
    def __init__(self):
        pass

    def _ejecutar_consulta(self, consulta, parametros=()):
        """Ejecuta una consulta SQL de modificación (INSERT, UPDATE, DELETE)."""
        conn = crear_conexion()
        if not conn:
            return False, "Error de conexión con la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            conn.commit()
            return True, "Operación exitosa."
        except Error as e:
            return False, f"Error SQL: {e}"
        finally:
            if conn:
                conn.close()

    def _ejecutar_seleccion(self, consulta, parametros=()):
        """Ejecuta una consulta SQL de selección (SELECT)."""
        conn = crear_conexion()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            return cursor.fetchall()
        except Error as e:
            print(f"Error SQL: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # --- PROVEEDORES ---

    def registrar_proveedor(self, nombre, contacto, telefono, direccion):
        sql = "INSERT INTO proveedores (nombre, contacto, telefono, direccion) VALUES (?, ?, ?, ?)"
        return self._ejecutar_consulta(sql, (nombre, contacto, telefono, direccion))

    def obtener_proveedores(self):
        return self._ejecutar_seleccion("SELECT * FROM proveedores")
    
    def buscar_proveedor_por_id(self, id_proveedor):
        res = self._ejecutar_seleccion("SELECT * FROM proveedores WHERE id=?", (id_proveedor,))
        return res[0] if res else None

    # --- INVENTARIO (MEDICAMENTOS E INSUMOS) ---

    def registrar_producto(self, nombre, descripcion, tipo, stock, fecha_caducidad, 
                          presentacion=None, requiere_receta=0, tipo_material=None, proveedor_id=None):
        sql = """
            INSERT INTO inventario (nombre, descripcion, tipo, stock, fecha_caducidad, 
                                    presentacion, requiere_receta, tipo_material, proveedor_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self._ejecutar_consulta(sql, (nombre, descripcion, tipo, stock, fecha_caducidad, 
                                             presentacion, requiere_receta, tipo_material, proveedor_id))

    def obtener_inventario(self, tipo=None):
        if tipo:
            return self._ejecutar_seleccion("SELECT * FROM inventario WHERE tipo=?", (tipo,))
        return self._ejecutar_seleccion("SELECT * FROM inventario")

    def actualizar_stock(self, id_producto, cantidad_agregar):
        """Suma (o resta si es negativo) al stock actual."""
        # Se podría hacer en una sola consulta, pero leemos primero para validar si existe
        sql_update = "UPDATE inventario SET stock = stock + ? WHERE id = ?"
        return self._ejecutar_consulta(sql_update, (cantidad_agregar, id_producto))

    # --- PEDIDOS ---

    def crear_pedido_cabecera(self, solicitante, diagnostico_ref, estado="Pendiente"):
        conn = crear_conexion()
        if not conn:
            return None, "Error de conexión."
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO pedidos_farmacia (solicitante, diagnostico_referencia, estado) VALUES (?, ?, ?)"
            cursor.execute(sql, (solicitante, diagnostico_ref, estado))
            conn.commit()
            pedido_id = cursor.lastrowid
            return pedido_id, "Pedido creado."
        except Error as e:
            return None, f"Error abriendo pedido: {e}"
        finally:
            conn.close()

    def agregar_detalle_pedido(self, pedido_id, nombre_item, cantidad):
        sql = "INSERT INTO pedido_detalles (pedido_id, nombre_item, cantidad) VALUES (?, ?, ?)"
        return self._ejecutar_consulta(sql, (pedido_id, nombre_item, cantidad))

    def obtener_pedidos(self, estado=None):
        """Retorna lista de pedidos (cabecera)."""
        if estado:
            return self._ejecutar_seleccion("SELECT * FROM pedidos_farmacia WHERE estado=?", (estado,))
        return self._ejecutar_seleccion("SELECT * FROM pedidos_farmacia ORDER BY id DESC")

    def obtener_detalles_pedido(self, pedido_id):
        return self._ejecutar_seleccion("SELECT * FROM pedido_detalles WHERE pedido_id=?", (pedido_id,))

    def actualizar_estado_pedido(self, pedido_id, nuevo_estado):
        return self._ejecutar_consulta("UPDATE pedidos_farmacia SET estado=? WHERE id=?", (nuevo_estado, pedido_id))

    def eliminar_pedido(self, pedido_id):
        # Primero eliminar detalles, luego cabecera (o usar ON DELETE CASCADE si estuviera config)
        self._ejecutar_consulta("DELETE FROM pedido_detalles WHERE pedido_id=?", (pedido_id,))
        return self._ejecutar_consulta("DELETE FROM pedidos_farmacia WHERE id=?", (pedido_id,))
