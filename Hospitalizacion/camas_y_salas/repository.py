from typing import Dict, Optional, List
from .models import Habitacion, Cama, Sala, Infraestructura, Paciente, PedidoHospitalizacion, Historial

class MemoryRepository:
    def __init__(self):
        # Datos quemados de ejemplo
        self.habitaciones: Dict[str, Habitacion] = {
            "H-PB-101": Habitacion("H-PB-101", "disponible", "Planta Baja"),
            "H-P1-102": Habitacion("H-P1-102", "ocupada", "Piso 1"),
            "H-P2-201": Habitacion("H-P2-201", "mantenimiento", "Piso 2"),
        }
        self.camas: Dict[str, Cama] = {
            "C-101-1": Cama("C-101-1", "101", "disponible", True),
            "C-101-2": Cama("C-101-2", "101", "disponible", True),
            "C-102-1": Cama("C-102-1", "102", "ocupada", True),
        }
        self.salas: Dict[str, Sala] = {
            "S-PB-01": Sala("S-PB-01", True, "Planta Baja"),
            "S-P1-02": Sala("S-P1-02", True, "Piso 1"),
            "S-P2-03": Sala("S-P2-03", False, "Piso 2"),
        }
        self.pacientes: Dict[str, Paciente] = {
            "P001": Paciente("P001", "Juan Perez", "en_observacion"),
            "P002": Paciente("P002", "Maria Gomez", "hospitalizado", "C-102-1"),
        }
        self.pedidos: Dict[str, PedidoHospitalizacion] = {}
        self.historial = Historial()

    # Infraestructura
    def registrar_infraestructura(self, infra: Infraestructura) -> Optional[str]:
        """Registra infraestructura y retorna el ID asignado, o None si falla."""
        try:
            def floor_code(ubic: str) -> str:
                u = (ubic or "Planta Baja").lower()
                if "planta" in u:
                    return "PB"
                if "piso 1" in u:
                    return "P1"
                if "piso 2" in u:
                    return "P2"
                if "piso 3" in u:
                    return "P3"
                return "PB"

            if infra.tipo == "habitacion":
                code = floor_code(infra.ubicacion)
                seq = 100 + len([h for h in self.habitaciones if h.startswith(f"H-{code}-")]) + 1
                hid = f"H-{code}-{seq}"
                if hid in self.habitaciones:
                    return None
                self.habitaciones[hid] = Habitacion(hid, "disponible", infra.ubicacion)
                self.historial.registrar(f"Infraestructura registrada: Habitacion {hid} ({infra.ubicacion})")
                return hid
            elif infra.tipo == "sala":
                code = floor_code(infra.ubicacion)
                seq = 1 + len([s for s in self.salas if s.startswith(f"S-{code}-")])
                sid = f"S-{code}-{seq:02d}"
                if sid in self.salas:
                    return None
                self.salas[sid] = Sala(sid, True, infra.ubicacion)
                self.historial.registrar(f"Infraestructura registrada: Sala {sid} ({infra.ubicacion})")
                return sid
            elif infra.tipo == "cama":
                hab_id = infra.ubicacion  # Para cama, 'ubicacion' representa la habitación destino
                if hab_id not in self.habitaciones:
                    return None
                seq = 1 + len([c for c in self.camas if c.startswith(f"C-{hab_id}-")])
                cid = f"C-{hab_id}-{seq}"
                if cid in self.camas:
                    return None
                self.camas[cid] = Cama(cid, hab_id, "disponible", True)
                self.historial.registrar(f"Infraestructura registrada: Cama {cid} (hab {hab_id})")
                return cid
            else:
                return None
        except Exception:
            return None

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

    def buscar_habitaciones(self, query: str) -> List[Habitacion]:
        q = (query or "").strip().lower()
        res: List[Habitacion] = []
        for hab in self.habitaciones.values():
            if q in hab.numero.lower() or q in (hab.ubicacion or "").lower():
                res.append(hab)
        # ordenar por ubicacion y numero
        return sorted(res, key=lambda h: (h.ubicacion, h.numero))

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
