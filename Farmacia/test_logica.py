import unittest
import datetime
from logica_farmacia import SistemaFarmacia

class TestSistemaFarmacia(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaFarmacia()

    def test_registro_proveedor_exitoso(self):
        msg = self.sistema.registrarProveedor("Farmacos SA", "555-1234", "Av. Siempre Viva")
        self.assertIn("éxito", msg)
        self.assertEqual(len(self.sistema.proveedores), 1)
        self.assertEqual(self.sistema.proveedores[0].id_proveedor, 1)

    def test_registro_proveedor_error_validacion(self):
        with self.assertRaises(ValueError):
            self.sistema.registrarProveedor("", "555-1234", "Dir")

    def test_registro_medicamento(self):
        msg = self.sistema.registrarMedicamento("Paracetamol", "500mg", 100, "2026-01-01", "Tableta", False)
        self.assertIn("éxito", msg)
        self.assertEqual(len(self.sistema.inventario_medicamentos), 1)

    def test_pedido_interno_creacion(self):
        items = [{'nombre_medicamento': 'Paracetamol', 'cantidad': 20}]
        msg = self.sistema.elaborarPedidoMedicamentos("Dr. House", "Diagnóstico", items)
        self.assertIn("creado", msg)
        self.assertEqual(len(self.sistema.pedidos_internos), 1)
        self.assertEqual(self.sistema.pedidos_internos[0].estado, "Pendiente")

    def test_flujo_pedido_proveedor(self):
        # 1. Registrar proveedor y producto
        self.sistema.registrarProveedor("ProvTest", "111", "Dir")
        self.sistema.registrarMedicamento("Ibuprofeno", "400mg", 50, "2026-01-01", "Caja", False)
        
        # 2. Crear pedido
        items = [{'nombre': 'Ibuprofeno', 'cantidad': 100}]
        # ID Proveedor = 1
        msg = self.sistema.elaborarPedidoDeMedicamentosAProveedor(1, items)
        self.assertIn("enviado", msg)
        
        pedido = self.sistema.pedidos_proveedores[0]
        self.assertEqual(pedido.estado, "Enviado")
        
        # 3. Modificar pedido
        items_mod = [{'nombre': 'Ibuprofeno', 'cantidad': 120}]
        self.sistema.modificarPedidoDeProveedor(pedido.id_pedido, items_mod)
        self.assertEqual(pedido.items[0]['cantidad'], 120)
        
        # 4. Recibir pedido
        msg_recep = self.sistema.registrarRecepcionPedido(pedido.id_pedido)
        self.assertIn("registrada", msg_recep)
        self.assertEqual(pedido.estado, "Recibido")
        
        # 5. Verificar inventario (50 inicial + 120 recibidos = 170)
        med = self.sistema.inventario_medicamentos[0]
        self.assertEqual(med.cantidad, 170)

    def test_control_caducidad(self):
        hoy = datetime.date.today()
        ayer = (hoy - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        futuro_cercano = (hoy + datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        futuro_lejano = (hoy + datetime.timedelta(days=60)).strftime("%Y-%m-%d")
        
        self.sistema.registrarMedicamento("Vencido", "Desc", 10, ayer, "X", False)
        self.sistema.registrarMedicamento("Proximo", "Desc", 10, futuro_cercano, "X", False)
        self.sistema.registrarMedicamento("Lejano", "Desc", 10, futuro_lejano, "X", False)
        
        # Test vencidos
        vencidos = self.sistema.consultarCaducidad(tipo="medicamentos", filtro="vencidos")
        self.assertEqual(len(vencidos), 1)
        self.assertEqual(vencidos[0].nombre, "Vencido")
        
        # Test próximos
        proximos = self.sistema.consultarCaducidad(tipo="medicamentos", filtro="proximos")
        self.assertEqual(len(proximos), 1)
        self.assertEqual(proximos[0].nombre, "Proximo")

if __name__ == '__main__':
    unittest.main()
