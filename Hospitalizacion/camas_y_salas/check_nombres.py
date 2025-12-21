from .repository import repo

def main():
    print("Salas:")
    for sid, s in sorted(repo.salas.items()):
        print(f"  {sid} -> nombre_clave={s.nombre_clave} ubicacion={s.ubicacion}")
    print("\nHabitaciones:")
    for hid, h in sorted(repo.habitaciones.items()):
        print(f"  {hid} -> nombre_clave={h.nombre_clave} sala_id={h.sala_id} ubicacion={h.ubicacion}")
    print("\nCamas:")
    for cid, c in sorted(repo.camas.items()):
        print(f"  {cid} -> nombre_clave={c.nombre_clave} hab={c.num_habitacion} estado={c.estado}")

if __name__ == "__main__":
    main()
