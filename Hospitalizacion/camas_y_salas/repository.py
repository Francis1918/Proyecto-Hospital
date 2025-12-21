from typing import Dict, Optional, List
from .models import Habitacion, Cama, Sala, Infraestructura, Paciente, PedidoHospitalizacion, Historial

# Nombres griegos para salas (en español)
GREEK_NAMES = [
    "Alfa", "Beta", "Gama", "Delta", "Épsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Ómicron", "Pi", "Rho",
    "Sigma", "Tau", "Úpsilon", "Phi", "Chi", "Psi", "Omega"
]

def letter_sequence(n: int) -> str:
    """Devuelve una secuencia alfabética: 1->A, 2->B, ..., 26->Z, 27->AA, etc."""
    if n <= 0:
        return "A"
    s = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        s = chr(ord('A') + rem) + s
    return s

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
        # Índice opcional para mapear cédulas (cc) del módulo Pacientes a IDs internos del repositorio
        self._pacientes_idx_por_cc: Dict[str, str] = {}
        self.pedidos: Dict[str, PedidoHospitalizacion] = {}
        self.historial = Historial()
        # Mapa de hospitalizaciones registradas sin cama asignada: id_paciente -> {sala, fecha, motivo}
        self.hospitalizaciones: Dict[str, Dict[str, str]] = {}

        # Inicializar nombres clave para salas y relacionar habitaciones con salas por ubicacion
        try:
            # 1) Asignar nombre_clave a salas de forma global (ALFA, BETA, GAMA, ...)
            for idx, sid in enumerate(sorted(self.salas.keys()), start=1):
                sala = self.salas.get(sid)
                if sala:
                    sala.nombre_clave = GREEK_NAMES[(idx - 1) % len(GREEK_NAMES)]

            # 2) Vincular habitaciones a una sala del mismo piso y nombrarlas como "<SalaClave> <N>"
            #    Recalcular índices por sala en orden estable
            for hid, hab in self.habitaciones.items():
                sala_match = self._find_sala_by_floor(hab.ubicacion)
                hab.sala_id = sala_match
            # construir listas por sala
            habs_por_sala: Dict[str, List[str]] = {}
            for hid, hab in self.habitaciones.items():
                if hab.sala_id:
                    habs_por_sala.setdefault(hab.sala_id, []).append(hid)
            for sala_id, hids in habs_por_sala.items():
                # ordenar por ID de habitación para índice determinista
                for idx, hid in enumerate(sorted(hids), start=1):
                    hab = self.habitaciones.get(hid)
                    sala_clave = self.salas[sala_id].nombre_clave if sala_id in self.salas else "Sala"
                    if hab:
                        hab.nombre_clave = f"{sala_clave} {idx}"

            # 3) Asignar nombre_clave a camas como "<SalaClave> <N><Letra>" (p.ej., Alfa 1A, Alfa 1B)
            camas_por_hab: Dict[str, List[str]] = {}
            for cid, cama in self.camas.items():
                camas_por_hab.setdefault(cama.num_habitacion, []).append(cid)
            for hid, cids in camas_por_hab.items():
                hab = self._resolve_habitacion(hid)
                if not hab:
                    continue
                # ordenar por secuencia numérica del ID de cama
                def cama_seq(c_id: str) -> int:
                    try:
                        parts = c_id.split('-')
                        return int(parts[-1])
                    except Exception:
                        return 0
                for idx, cid in enumerate(sorted(cids, key=cama_seq), start=1):
                    cama = self.camas.get(cid)
                    letra = letter_sequence(idx)
                    if cama:
                        # Formato exacto: "Alfa 1A"
                        base = hab.nombre_clave or hab.numero
                        cama.nombre_clave = f"{base}{letra}"
        except Exception:
            # No interrumpir si falla la inicialización opcional
            pass

    def _gen_paciente_id(self) -> str:
        """Genera un nuevo ID interno para paciente (formato P###) evitando colisiones."""
        n = 1
        while True:
            pid = f"P{n:03d}"
            if pid not in self.pacientes:
                return pid
            n += 1

    def ensure_repo_patient(self, cc: Optional[str], nombre: str) -> str:
        """
        Asegura que exista un paciente en el repositorio para la cédula/nombre dado.
        - Si hay `cc` y ya está mapeado, retorna el ID existente.
        - Si no existe, crea un nuevo `Paciente` con ID interno autogenerado y lo retorna.
        """
        # Si tenemos cc mapeada previamente, usarla
        if cc:
            mapped = self._pacientes_idx_por_cc.get(cc)
            if mapped and mapped in self.pacientes:
                return mapped
        # Intento heurístico: si existe un paciente con el mismo nombre, reutilizar su ID
        for pid, pac in self.pacientes.items():
            try:
                if (pac.nombre or "").strip().lower() == (nombre or "").strip().lower():
                    if cc:
                        self._pacientes_idx_por_cc[cc] = pid
                    return pid
            except Exception:
                pass
        # Crear uno nuevo
        new_id = self._gen_paciente_id()
        self.pacientes[new_id] = Paciente(new_id, nombre or f"Paciente {new_id}")
        if cc:
            self._pacientes_idx_por_cc[cc] = new_id
        self.historial.registrar(f"Paciente creado/asegurado: {new_id} ({nombre})")
        return new_id

    # Infraestructura
    def registrar_infraestructura(self, infra: Infraestructura) -> Optional[str]:
        """Registra infraestructura y retorna el ID asignado, o None si falla."""
        try:
            def floor_code(ubic: str) -> str:
                return self._floor_code(ubic)

            if infra.tipo == "habitacion":
                code = floor_code(infra.ubicacion)
                seq = 100 + len([h for h in self.habitaciones if h.startswith(f"H-{code}-")]) + 1
                hid = f"H-{code}-{seq}"
                if hid in self.habitaciones:
                    return None
                # Asignar a una sala (si se provee) y calcular nombre_clave
                sala_id = infra.rel_sala_id or self._find_sala_by_floor(infra.ubicacion)
                # Enforce sala capacity: default 5 habitaciones
                if sala_id and sala_id in self.salas:
                    current_count = len([h for h in self.habitaciones.values() if h.sala_id == sala_id])
                    capacidad = getattr(self.salas[sala_id], "capacidad", 5)
                    if current_count >= capacidad:
                        # sin espacio en la sala
                        return None
                # índice de habitación dentro de la sala
                hab_index = 1 + len([h for h in self.habitaciones.values() if h.sala_id == sala_id])
                sala_clave = self.salas[sala_id].nombre_clave if sala_id and sala_id in self.salas else "Sala"
                nombre_clave = f"{sala_clave} {hab_index}"
                self.habitaciones[hid] = Habitacion(hid, "disponible", infra.ubicacion, sala_id=sala_id, nombre_clave=nombre_clave)
                self.historial.registrar(f"Infraestructura registrada: Habitacion {hid} ({infra.ubicacion})")
                return hid
            elif infra.tipo == "sala":
                code = floor_code(infra.ubicacion)
                seq = 1 + len([s for s in self.salas if s.startswith(f"S-{code}-")])
                sid = f"S-{code}-{seq:02d}"
                if sid in self.salas:
                    return None
                # nombre_clave: griego por secuencia del piso
                nombre_griego = GREEK_NAMES[(seq - 1) % len(GREEK_NAMES)]
                # capacidad por defecto 5 si no se provee
                cap = infra.capacidad if isinstance(infra.capacidad, int) and infra.capacidad > 0 else 5
                self.salas[sid] = Sala(sid, True, infra.ubicacion, cap, nombre_clave=nombre_griego)
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
                # nombre_clave: <SalaClave> <N> <Letra>
                hab = self.habitaciones.get(hab_id)
                letra = letter_sequence(seq)
                clave_base = (hab.nombre_clave if hab and hab.nombre_clave else hab_id)
                self.camas[cid] = Cama(cid, hab_id, "disponible", True, nombre_clave=f"{clave_base} {letra}")
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
            if q in hab.numero.lower() or q in (hab.ubicacion or "").lower() or q in ((hab.nombre_clave or "").lower()):
                res.append(hab)
        # ordenar por ubicacion y numero
        return sorted(res, key=lambda h: (h.ubicacion, h.numero))

    def buscar_salas(self, query: str) -> List[Sala]:
        q = (query or "").strip().lower()
        res: List[Sala] = []
        for sala in self.salas.values():
            if q in sala.nombre.lower() or q in (sala.ubicacion or "").lower() or q in ((sala.nombre_clave or "").lower()):
                res.append(sala)
        # ordenar por ubicacion y nombre
        return sorted(res, key=lambda s: (s.ubicacion, s.nombre))

    def buscar_camas(self, query: str) -> List[Cama]:
        q = (query or "").strip().lower()
        res: List[Cama] = []
        for cama in self.camas.values():
            hab = self._resolve_habitacion(cama.num_habitacion)
            nombre_base = (hab.nombre_clave if hab and hab.nombre_clave else cama.num_habitacion)
            display = f"{nombre_base}"
            if q in (cama.id_cama or "").lower() or q in display.lower() or q in ((cama.nombre_clave or "").lower()):
                res.append(cama)
        # ordenar por estado y id
        return sorted(res, key=lambda c: (c.estado, c.id_cama))

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
        # Registrar/actualizar la sala asociada a la hospitalización del paciente
        info = self.hospitalizaciones.get(id_paciente)
        if not info:
            self.hospitalizaciones[id_paciente] = {"sala": sala, "fecha": "", "motivo": ""}
        else:
            info["sala"] = sala
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

    def registrar_hospitalizacion_solo_sala(self, id_paciente: str, fecha: str, sala: str, motivo: str) -> str:
        """Registra una hospitalización con solo sala (sin cama asignada aún)."""
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return "Paciente no registrado"
        sl = self.salas.get(sala)
        if not sl:
            return "Sala no registrada"
        if not sl.activa:
            return "Sala inactiva: no se puede registrar hospitalización"
        # Registrar hospitalización sin cama
        self.hospitalizaciones[id_paciente] = {"sala": sala, "fecha": fecha, "motivo": motivo}
        pac.estado = "hospitalizado"
        pac.cama_asignada = None
        self.historial.registrar(f"Hospitalización (solo sala) registrada: {id_paciente} sala {sala} motivo {motivo} fecha {fecha}")
        return "OK"

    def registrar_hospitalizacion_sin_sala(self, id_paciente: str, fecha: str, motivo: str) -> str:
        """Registra una hospitalización sin sala ni cama (se asignarán después)."""
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return "Paciente no registrado"
        # Registrar hospitalización sin sala
        self.hospitalizaciones[id_paciente] = {"sala": None, "fecha": fecha, "motivo": motivo}
        pac.estado = "hospitalizado"
        pac.cama_asignada = None
        self.historial.registrar(f"Hospitalización (sin sala) registrada: {id_paciente} motivo {motivo} fecha {fecha}")
        return "OK"

    def listar_pacientes_hospitalizados_con_sala(self) -> List[str]:
        """Lista IDs de pacientes hospitalizados que tienen una sala registrada y ninguna cama asignada."""
        res: List[str] = []
        for pid, pac in self.pacientes.items():
            if pac.estado == "hospitalizado" and pid in self.hospitalizaciones and not pac.cama_asignada:
                res.append(pid)
        return res

    def listar_para_autorizar(self) -> List[str]:
        """Lista IDs de pacientes que requieren autorización de hospitalización.
        Incluye:
        - Pedidos de hospitalización en estado 'pendiente'.
        - Pacientes con cama asignada cuyo estado aún no es 'hospitalización autorizada'.
        """
        ids = set()
        for pid, ped in self.pedidos.items():
            if ped.estado == "pendiente":
                ids.add(pid)
        for pid, pac in self.pacientes.items():
            if pac.cama_asignada and pac.estado != "hospitalización autorizada":
                ids.add(pid)
        return sorted(ids)

    def get_sala_de_paciente(self, id_paciente: str) -> Optional[str]:
        info = self.hospitalizaciones.get(id_paciente)
        return info.get("sala") if info else None

    def get_pid_por_cc(self, cc: Optional[str]) -> Optional[str]:
        """Obtiene el ID interno del repositorio mapeado para una cédula, sin crear registros."""
        if not cc:
            return None
        return self._pacientes_idx_por_cc.get(cc)

    def tiene_cama_por_cc(self, cc: Optional[str]) -> bool:
        """Indica si el paciente mapeado por cédula tiene cama asignada."""
        pid = self.get_pid_por_cc(cc)
        if not pid:
            return False
        pac = self.pacientes.get(pid)
        return bool(pac and pac.cama_asignada)

    def get_motivo_hospitalizacion(self, id_paciente: str) -> Optional[str]:
        """Devuelve el motivo registrado en la hospitalización del paciente, si existe."""
        info = self.hospitalizaciones.get(id_paciente)
        return info.get("motivo") if info else None

    # Paciente
    def consultar_estado_paciente(self, id_paciente: str) -> Optional[str]:
        pac = self.pacientes.get(id_paciente)
        if not pac:
            return None
        self.historial.registrar(f"Consulta estado paciente {id_paciente}: {pac.estado}")
        return pac.estado

    def find_paciente_id_por_nombre(self, nombre: str) -> Optional[str]:
        """Devuelve el ID interno del repositorio para un nombre exacto (case-insensitive), si existe."""
        try:
            target = (nombre or "").strip().lower()
            for pid, pac in self.pacientes.items():
                if (pac.nombre or "").strip().lower() == target:
                    return pid
        except Exception:
            pass
        return None

    def esta_hospitalizado_por_cc(self, cc: Optional[str]) -> bool:
        """Indica si el paciente mapeado por cédula está hospitalizado. No crea registros nuevos."""
        if not cc:
            return False
        pid = self._pacientes_idx_por_cc.get(cc)
        if not pid:
            return False
        pac = self.pacientes.get(pid)
        return bool(pac and (pac.estado == "hospitalizado" or pac.cama_asignada))

    def esta_hospitalizado_por_nombre(self, nombre: str) -> bool:
        """Indica si un paciente identificado por nombre ya está hospitalizado (si existe)."""
        pid = self.find_paciente_id_por_nombre(nombre)
        if not pid:
            return False
        pac = self.pacientes.get(pid)
        return bool(pac and (pac.estado == "hospitalizado" or pac.cama_asignada))

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

    # Helpers internos
    def _floor_code(self, ubic: str) -> str:
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

    def _find_sala_by_floor(self, ubicacion: str) -> Optional[str]:
        code = self._floor_code(ubicacion)
        # priorizar la sala con menor secuencia del piso
        candidates = sorted([sid for sid in self.salas if sid.startswith(f"S-{code}-")])
        return candidates[0] if candidates else None

    def _resolve_habitacion(self, num_habitacion: str) -> Optional[Habitacion]:
        # Intentar id completo
        hab = self.habitaciones.get(num_habitacion)
        if hab:
            return hab
        # Intentar por sufijo numérico (compatibilidad con datos iniciales "101")
        for hid, h in self.habitaciones.items():
            try:
                if hid.split("-")[-1] == num_habitacion:
                    return h
            except Exception:
                pass
        return None

# Repositorio global simple (podría reemplazarse por DB en el futuro)
repo = MemoryRepository()
