from datetime import datetime
from .backend_farmacia import GestorFarmacia

class LogicaFarmacia:
    def __init__(self):
        self.db = GestorFarmacia()

    def _validar_texto(self, texto, nombre_campo):
        if not texto or len(texto.strip()) == 0:
            return False, f"El campo '{nombre_campo}' es obligatorio."
        return True, ""

    def _validar_numero(self, numero, min_val=0):
        try:
            val = int(numero)
            if val < min_val:
                return False, f"El valor debe ser mayor o igual a {min_val}."
            return True, ""
        except ValueError:
            return False, "Debe ingresar un número válido."

    # --- PROVEEDORES ---
    def registrar_proveedor(self, nombre, contacto, telefono, direccion):
        ok, msg = self._validar_texto(nombre, "Nombre")
        if not ok: return False, msg
        
        ok, msg = self._validar_texto(contacto, "Contacto")
        if not ok: return False, msg

        return self.db.registrar_proveedor(nombre, contacto, telefono, direccion)

    def obtener_proveedores(self):
        return self.db.obtener_proveedores()

    # --- INVENTARIO ---
    def registrar_medicamento(self, nombre, descripcion, stock, fecha_cad, presentacion, requiere_receta):
        ok, msg = self._validar_texto(nombre, "Nombre")
        if not ok: return False, msg
        
        ok, msg = self._validar_numero(stock)
        if not ok: return False, msg

        # Validar fecha
        try:
            datetime.strptime(fecha_cad, "%Y-%m-%d")
        except ValueError:
            return False, "Formato de fecha inválido (YYYY-MM-DD)."

        return self.db.registrar_producto(nombre, descripcion, "Medicamento", int(stock), fecha_cad, 
                                          presentacion=presentacion, requiere_receta=1 if requiere_receta else 0)

    def registrar_insumo(self, nombre, descripcion, stock, fecha_cad, tipo_material):
        ok, msg = self._validar_texto(nombre, "Nombre")
        if not ok: return False, msg
        
        ok, msg = self._validar_numero(stock)
        if not ok: return False, msg

        return self.db.registrar_producto(nombre, descripcion, "Insumo", int(stock), fecha_cad, 
                                          tipo_material=tipo_material)

    def obtener_inventario(self, tipo=None):
        return self.db.obtener_inventario(tipo)

    # --- PEDIDOS ---
    def crear_pedido_interno(self, solicitante, departamento, items):
        # Items: lista de dicts {'nombre': ..., 'cantidad': ...}
        if not items:
            return False, "No se pueden crear pedidos vacíos."
        
        ok, msg = self._validar_texto(solicitante, "Solicitante")
        if not ok: return False, msg

        # 1. Crear cabecera
        pedido_id, msg = self.db.crear_pedido_cabecera(solicitante, f"Departamento: {departamento}")
        if not pedido_id:
            return False, msg

        # 2. Agregar detalles
        for item in items:
            self.db.agregar_detalle_pedido(pedido_id, item['nombre'], item['cantidad'])
        
        return True, f"Pedido Interno #{pedido_id} creado correctamente."

    def crear_pedido_proveedor(self, id_proveedor, items):
        # Obtener nombre del proveedor para referenciarlo
        prov = self.db.buscar_proveedor_por_id(id_proveedor)
        if not prov:
            return False, "Proveedor no encontrado."
        nombre_prov = prov[1] # Asumiendo columna 1 es nombre

        pedido_id, msg = self.db.crear_pedido_cabecera("Farmacia", f"Proveedor: {nombre_prov}", estado="Enviado")
        if not pedido_id:
            return False, msg

        for item in items:
            self.db.agregar_detalle_pedido(pedido_id, item['nombre'], item['cantidad'])

        return True, f"Pedido a Proveedor #{pedido_id} enviado."

    def consultar_pedidos(self):
        # Retorna lista de dicts o tuplas más amigables
        pedidos_raw = self.db.obtener_pedidos()
        resultado = []
        for p in pedidos_raw:
            # p: (id, solicitante, diagnostico_ref, estado, fecha)
            detalles = self.db.obtener_detalles_pedido(p[0])
            items_str = ", ".join([f"{d[2]} ({d[3]})" for d in detalles]) # d[2]=nombre, d[3]=cant
            
            resultado.append({
                "id": p[0],
                "solicitante": p[1],
                "referencia": p[2],
                "estado": p[3],
                "fecha": p[4],
                "items": items_str
            })
        return resultado

    def recibir_pedido(self, pedido_id):
        # 1. Obtener detalles para actualizar stock
        detalles = self.db.obtener_detalles_pedido(pedido_id)
        if not detalles:
            return False, "Pedido no encontrado o vacío."
        
        # 2. Actualizar stock para cada item
        for d in detalles:
            nombre_item = d[2]
            cantidad = d[3]
            # Buscar ID del producto por nombre (una búsqueda simplificada)
            # Nota: Esto asume nombres únicos o toma el primero que encuentra.
            # En un sistema real, el pedido debería guardar el ID del producto si es un reabastecimiento exacto.
            # Dado el esquema actual, buscamos coincidencias.
            inv = self.db._ejecutar_seleccion("SELECT id FROM inventario WHERE nombre=?", (nombre_item,))
            if inv:
                prod_id = inv[0][0]
                self.db.actualizar_stock(prod_id, cantidad)
            else:
                # Si no existe, quizás advertir o crearlo es complejo sin más datos.
                pass 

        # 3. Marcar como Recibido
        return self.db.actualizar_estado_pedido(pedido_id, "Recibido")
        
    def consultar_caducidad(self, filtro="proximos"): # proximos, vencidos, todos
        productos = self.db.obtener_inventario() # Trae todos
        confirmados = []
        hoy = datetime.now()

        for p in productos:
            # p[5] es fecha_caducidad en string YYYY-MM-DD
            try:
                fecha_cad = datetime.strptime(p[5], "%Y-%m-%d")
                delta_dias = (fecha_cad - hoy).days
                
                agregar = False
                if filtro == "vencidos" and delta_dias < 0:
                    agregar = True
                elif filtro == "proximos" and 0 <= delta_dias <= 30:
                    agregar = True
                elif filtro == "todos":
                    agregar = True
                
                if agregar:
                    confirmados.append({
                        "nombre": p[1],
                        "tipo": p[3],
                        "fecha": p[5],
                        "dias": delta_dias
                    })
            except (ValueError, TypeError):
                continue

        return confirmados
