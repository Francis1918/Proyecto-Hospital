import datetime

class Proveedor:
    def __init__(self, id_proveedor, nombre, contacto, direccion):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion

    def __str__(self):
        return f"{self.nombre} (ID: {self.id_proveedor})"

class Producto:
    def __init__(self, id_producto, nombre, descripcion, cantidad, fecha_caducidad):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.fecha_caducidad = fecha_caducidad  # Formato: 'YYYY-MM-DD'

class Medicamento(Producto):
    def __init__(self, id_producto, nombre, descripcion, cantidad, fecha_caducidad, tipo_presentacion, requiere_receta):
        super().__init__(id_producto, nombre, descripcion, cantidad, fecha_caducidad)
        self.tipo_presentacion = tipo_presentacion
        self.requiere_receta = requiere_receta

class Insumo(Producto):
    def __init__(self, id_producto, nombre, descripcion, cantidad, fecha_caducidad, tipo_material):
        super().__init__(id_producto, nombre, descripcion, cantidad, fecha_caducidad)
        self.tipo_material = tipo_material

class Pedido:
    def __init__(self, id_pedido, items, fecha_creacion, estado="Pendiente"):
        self.id_pedido = id_pedido
        self.items = items  # Lista de diccionarios: {'nombre': ..., 'cantidad': ...}
        self.fecha_creacion = fecha_creacion
        self.estado = estado # "Pendiente", "Enviado", "Recibido", "Cancelado"

class PedidoInterno(Pedido):
    def __init__(self, id_pedido, items, fecha_creacion, solicitante, departamento):
        super().__init__(id_pedido, items, fecha_creacion, estado="Pendiente")
        self.solicitante = solicitante # Médico o Enfermero
        self.departamento = departamento

class PedidoProveedor(Pedido):
    def __init__(self, id_pedido, items, fecha_creacion, proveedor):
        super().__init__(id_pedido, items, fecha_creacion, estado="Enviado") # Al crear pedido a proveedor, se asume enviado
        self.proveedor = proveedor

class SistemaFarmacia:
    def __init__(self):
        # Simulación de base de datos en memoria
        self.proveedores = []
        self.inventario_medicamentos = []
        self.inventario_insumos = []
        
        # Listas separadas para pedidos internos y externos
        self.pedidos_internos = [] 
        self.pedidos_proveedores = []
        
        # Contadores para IDs autoincrementales
        self._contador_proveedores = 1
        self._contador_productos = 1
        self._contador_pedidos = 1

    # --- GESTIÓN DE REGISTROS ---

    def registrarProveedor(self, nombre, contacto, direccion):
        if not nombre or not contacto:
            raise ValueError("Nombre y contacto son obligatorios.")
            
        nuevo_proveedor = Proveedor(self._contador_proveedores, nombre, contacto, direccion)
        self.proveedores.append(nuevo_proveedor)
        self._contador_proveedores += 1
        return f"Proveedor '{nombre}' registrado con éxito (ID: {nuevo_proveedor.id_proveedor})."

    def registrarMedicamento(self, nombre, descripcion, cantidad, fecha_caducidad, tipo_presentacion, requiere_receta):
        if not nombre:
            raise ValueError("El nombre del medicamento es obligatorio.")
        if int(cantidad) < 0:
            raise ValueError("La cantidad no puede ser negativa.")
            
        nuevo_med = Medicamento(self._contador_productos, nombre, descripcion, int(cantidad), fecha_caducidad, tipo_presentacion, requiere_receta)
        self.inventario_medicamentos.append(nuevo_med)
        self._contador_productos += 1
        return f"Medicamento '{nombre}' registrado con éxito."

    def registrarInsumo(self, nombre, descripcion, cantidad, fecha_caducidad, tipo_material):
        if not nombre:
            raise ValueError("El nombre del insumo es obligatorio.")
            
        nuevo_insumo = Insumo(self._contador_productos, nombre, descripcion, int(cantidad), fecha_caducidad, tipo_material)
        self.inventario_insumos.append(nuevo_insumo)
        self._contador_productos += 1
        return f"Insumo '{nombre}' registrado con éxito."

    # --- PEDIDOS INTERNOS (Solicitados por Médicos/Enfermeros) ---

    def elaborarPedidoMedicamentos(self, solicitante, departamento, items):
        """
        Crea un pedido interno de medicamentos.
        items: lista de {'nombre_medicamento': str, 'cantidad': int}
        """
        if not items:
            raise ValueError("El pedido debe contener al menos un item.")
            
        nuevo_pedido = PedidoInterno(self._contador_pedidos, items, datetime.date.today(), solicitante, departamento)
        self.pedidos_internos.append(nuevo_pedido)
        self._contador_pedidos += 1
        return f"Pedido interno #{nuevo_pedido.id_pedido} creado para {departamento}."

    def elaborarPedidoInsumos(self, solicitante, departamento, items):
        if not items:
            raise ValueError("El pedido debe contener al menos un item.")

        nuevo_pedido = PedidoInterno(self._contador_pedidos, items, datetime.date.today(), solicitante, departamento)
        self.pedidos_internos.append(nuevo_pedido)
        self._contador_pedidos += 1
        return f"Pedido interno de insumos #{nuevo_pedido.id_pedido} creado."

    def consultarPedidosInternos(self):
        return self.pedidos_internos

    # --- PEDIDOS A PROVEEDORES (Reposición de Stock) ---

    def elaborarPedidoDeMedicamentosAProveedor(self, id_proveedor, items):
        proveedor = self._buscar_proveedor(id_proveedor)
        if not proveedor:
            raise ValueError("Proveedor no encontrado.")
        if not items:
            raise ValueError("El pedido debe contener items.")
        
        # Normalizar items a formato estándar {'nombre': ..., 'cantidad': ...}
        # Si vienen como {'nombre_medicamento': ...} o similar, ajustar aquí si fuera necesario
        
        nuevo_pedido = PedidoProveedor(self._contador_pedidos, items, datetime.date.today(), proveedor)
        self.pedidos_proveedores.append(nuevo_pedido)
        self._contador_pedidos += 1
        return f"Pedido a proveedor #{nuevo_pedido.id_pedido} enviado a {proveedor.nombre}."

    def elaborarPedidoDeInsumosAProveedor(self, id_proveedor, items):
        return self.elaborarPedidoDeMedicamentosAProveedor(id_proveedor, items) # Reutilizamos lógica

    def modificarPedidoDeProveedor(self, id_pedido, nuevos_items):
        pedido = self._buscar_pedido(self.pedidos_proveedores, id_pedido)
        if not pedido:
            raise ValueError("Pedido no encontrado.")
        if pedido.estado == "Recibido":
            raise ValueError("No se puede modificar un pedido ya recibido.")
            
        pedido.items = nuevos_items
        return f"Pedido #{id_pedido} modificado exitosamente."

    def eliminarPedidoDeProveedor(self, id_pedido):
        pedido = self._buscar_pedido(self.pedidos_proveedores, id_pedido)
        if not pedido:
            raise ValueError("Pedido no encontrado.")
        if pedido.estado == "Recibido":
            raise ValueError("No se puede eliminar un pedido ya recibido.")
            
        self.pedidos_proveedores.remove(pedido)
        return f"Pedido #{id_pedido} eliminado."

    # --- RECEPCIÓN DE PEDIDOS ---

    def registrarRecepcionPedido(self, id_pedido):
        pedido = self._buscar_pedido(self.pedidos_proveedores, id_pedido)
        if not pedido:
            raise ValueError("Pedido no encontrado.")
        if pedido.estado == "Recibido":
            return "El pedido ya fue recibido anteriormente."
            
        pedido.estado = "Recibido"
        
        # Actualizar inventario
        # Intentamos actualizar tanto en medicamentos como insumos
        for item in pedido.items:
            nombre = item.get('nombre') or item.get('nombre_medicamento')
            cantidad = item.get('cantidad')
            
            # Buscar en medicamentos
            encontrado = False
            for med in self.inventario_medicamentos:
                if med.nombre.lower() == nombre.lower():
                    med.cantidad += int(cantidad)
                    encontrado = True
                    break
            
            # Si no está en medicamentos, buscar en insumos
            if not encontrado:
                for ins in self.inventario_insumos:
                    if ins.nombre.lower() == nombre.lower():
                        ins.cantidad += int(cantidad)
                        encontrado = True
                        break
            
            # Si no existe en ninguno, se podría optar por crearlo o loguear una advertencia.
            # Por ahora, asumimos que solo reabastecemos productos registrados.
            
        return f"Recepción del pedido #{id_pedido} registrada. Inventario actualizado."

    # --- CONTROL DE CADUCIDAD ---

    def consultarCaducidad(self, tipo="todos", filtro="proximos"):
        """
        tipo: "medicamentos", "insumos", "todos"
        filtro: "vencidos" (ya pasaron), "proximos" (<= 30 dias), "todos"
        """
        lista_revision = []
        if tipo in ["medicamentos", "todos"]:
            lista_revision.extend(self.inventario_medicamentos)
        if tipo in ["insumos", "todos"]:
            lista_revision.extend(self.inventario_insumos)
            
        hoy = datetime.date.today()
        resultado = []
        
        for prod in lista_revision:
            try:
                fecha_cad = datetime.datetime.strptime(prod.fecha_caducidad, "%Y-%m-%d").date()
                dias_restantes = (fecha_cad - hoy).days
                
                if filtro == "vencidos":
                    if dias_restantes < 0:
                        resultado.append(prod)
                elif filtro == "proximos":
                    if 0 <= dias_restantes <= 30:
                        resultado.append(prod)
                else: # todos
                    resultado.append(prod)
            except ValueError:
                continue # Fecha inválida
                
        return resultado

    # --- MÉTODOS AUXILIARES ---

    def _buscar_proveedor(self, id_proveedor):
        for p in self.proveedores:
            if p.id_proveedor == int(id_proveedor):
                return p
        return None

    def _buscar_pedido(self, lista_pedidos, id_pedido):
        for p in lista_pedidos:
            if p.id_pedido == int(id_pedido):
                return p
        return None
