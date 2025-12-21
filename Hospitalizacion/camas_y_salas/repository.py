from typing import Dict, Optional, List
from .models import Habitacion, Cama, Sala, Infraestructura, Paciente, PedidoHospitalizacion, Historial

class MemoryRepository:
    def __init__(self):
        # Datos quemados de ejemplo
        self.habitaciones: Dict[str, Habitacion] = {
            "101": Habitacion("101", "disponible"),
            "102": Habitacion("102", "ocupada"),
            "201": Habitacion("201", "mantenimiento"),
        }
        self.camas: Dict[str, Cama] = {
            "C-101-1": Cama("C-101-1", "101", "disponible", True),
            "C-101-2": Cama("C-101-2", "101", "disponible", True),
            "C-102-1": Cama("C-102-1", "102", "ocupada", True),
        }
        self.salas: Dict[str, Sala] = {
            "UCI": Sala("UCI", True),
            "General": Sala("General", True),
            "Pediatria": Sala("Pediatria", False),
        }
        self.pacientes: Dict[str, Paciente] = {
            "P001": Paciente("P001", "Juan Perez", "en_observacion"),
            "P002": Paciente("P002", "Maria Gomez", "hospitalizado", "C-102-1"),
        }
        self.pedidos: Dict[str, PedidoHospitalizacion] = {}
        self.historial = Historial()

    # Infraestructura
    def registrar_infraestructura(self, infra: Infraestructura) -> bool:
        try:
            if infra.tipo == "habitacion":
                if infra.nombre in self.habitaciones:
                    return False
                self.habitaciones[infra.nombre] = Habitacion(infra.nombre, "disponible")
            elif infra.tipo == "sala":
                if infra.nombre in self.salas:
                    return False
                self.salas[infra.nombre] = Sala(infra.nombre, True)
            elif infra.tipo == "cama":
                if infra.nombre in self.camas:
                    return False
                # Se espera formato nombre: C-<hab>-<n>
                self.camas[infra.nombre] = Cama(infra.nombre, infra.ubicacion, "disponible", True)
            else:
                return False
            self.historial.registrar(f"Infraestructura registrada: {infra}")
            return True
        except Exception:
            return False

    # Habitaciones
    def consultar_estado_habitacion(self, numero: str) -> Optional[str]:
        hab = self.habitaciones.get(numero)
        if not hab:
            return None
        self.historial.registrar(f"Consulta estado habitación {numero}: {hab.estado}")
        return hab.estado

    def actualizar_estado_habitacion(self, numero: str, estado: str) -> bool:
        hab = self.habitaciones.get(numero)
        if not hab:
            return False
        if estado not in {"disponible", "ocupada", "mantenimiento"}:
            return False
        hab.estado = estado
        self.historial.registrar(f"Habitación {numero} actualizada a {estado}")
        return True

    # Asignaciones
    def asignar_cama(self, id_paciente: str, sala: str, id_cama: str) -> str:
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return "Paciente no registrado"
        if pac.cama_asignada:
            return "El paciente ya tiene una cama asignada"
        sl = self.salas.get(sala)
        if not sl:
            return "Sala no registrada"
        if not sl.activa:
            return "Sala inactiva: no se puede asignar cama"
        cama = self.camas.get(id_cama)
        if not cama:
            return "Cama no encontrada"
        if cama.estado != "disponible":
            return "La cama seleccionada no está disponible"
        if not cama.higiene_ok:
            return "La cama no está apta para uso"
        # asignar
        cama.estado = "ocupada"
        pac.cama_asignada = id_cama
        pac.estado = "hospitalizado"
        self.historial.registrar(f"Cama {id_cama} asignada a paciente {id_paciente} en sala {sala}")
        return "OK"

    # Hospitalización: pedidos y autorizaciones
    def registrar_pedido(self, id_paciente: str, motivo: str) -> bool:
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return False
        self.pedidos[id_paciente] = PedidoHospitalizacion(id_paciente, motivo, "pendiente")
        pac.estado = "pedido_registrado"
        self.historial.registrar(f"Pedido hospitalización registrado: {id_paciente} motivo {motivo}")
        return True

    def autorizar_hospitalizacion(self, id_paciente: str) -> str:
        ped = self.pedidos.get(id_paciente)
        if not ped:
            return "Solicitud de hospitalización no encontrada"
        if ped.estado == "autorizado":
            return "Solicitud ya autorizada"
        ped.estado = "autorizado"
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return "Paciente no registrado"
        pac.estado = "hospitalización autorizada"
        self.historial.registrar(f"Hospitalización autorizada para paciente {id_paciente}")
        return "OK"

    def registrar_hospitalizacion(self, id_paciente: str, fecha: str, sala: str, id_cama: str, motivo: str) -> str:
        # validar paciente y cama disponible
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return "Paciente no registrado"
        cama = self.camas.get(id_cama)
        if not cama or cama.estado != "disponible":
            return "La cama seleccionada no está disponible"
        # asignar cama y actualizar estados
        cama.estado = "ocupada"
        pac.cama_asignada = id_cama
        pac.estado = "hospitalizado"
        self.historial.registrar(f"Hospitalización registrada: {id_paciente} cama {id_cama} sala {sala} motivo {motivo} fecha {fecha}")
        return "OK"

    # Paciente
    def consultar_estado_paciente(self, id_paciente: str) -> Optional[str]:
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return None
        self.historial.registrar(f"Consulta estado paciente {id_paciente}: {pac.estado}")
        return pac.estado

    def autorizar_alta(self, id_paciente: str) -> str:
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return "Paciente no registrado"
        if pac.estado == "alta autorizada":
            return "Paciente ya tiene alta autorizada"
        pac.estado = "alta autorizada"
        # liberar cama si tenía
        if pac.cama_asignada and pac.cama_asignada in self.camas:
            self.camas[pac.cama_asignada].estado = "disponible"
            pac.cama_asignada = None
        self.historial.registrar(f"Alta autorizada para paciente {id_paciente}")
        return "OK"

# Repositorio global simple (podría reemplazarse por DB en el futuro)
repo = MemoryRepository()
