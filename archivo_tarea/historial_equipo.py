import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "proyecto",
    "port": 3306
}

def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar: {e}")
        return None

# ===========================================================
# CRUD
# ===========================================================

def insertar_historial(fecha, descripcion, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if not cnx: return
        cur = cnx.cursor()
        args = [fecha, descripcion, usuario_id, equipo_id, 0]
        cur.callproc("sp_insertar_historial_equipo", args)
        cnx.commit()
        nuevo_id = args[4]

        if nuevo_id == -1:
            print("❌ No existe usuario con ese ID.")
        elif nuevo_id == -2:
            print("❌ No existe equipo con ese ID.")
        else:
            print(f"✅ Historial insertado correctamente. ID: {nuevo_id}")
    except mysql.connector.Error as e:
        print("❌ Error al insertar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_historiales_activos():
    cnx = cur = None
    try:
        cnx = conectar()
        if not cnx: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_historial_activos")

        print("\n=== HISTORIALES ACTIVOS ===")
        print(f"{'ID':<5} | {'Fecha':<12} | {'Descripción':<25} | {'Usuario':<15} | {'Equipo':<15} | {'Creado':<19} | {'Actualizado':<19}")
        print("-" * 120)

        for result in cur.stored_results():
            for (id_h, fecha, desc, usuario, equipo, created, updated) in result.fetchall():
                ca = created.strftime("%Y-%m-%d %H:%M:%S") if created else "-"
                ua = updated.strftime("%Y-%m-%d %H:%M:%S") if updated else "-"
                print(f"{id_h:<5} | {fecha} | {desc:<25} | {usuario:<15} | {equipo:<15} | {ca:<19} | {ua:<19}")

    except mysql.connector.Error as e:
        print("❌ Error al listar historial activo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_historiales_todos():
    cnx = cur = None
    try:
        cnx = conectar()
        if not cnx: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_historial_todos")

        print("\n=== TODOS LOS HISTORIALES ===")
        print(f"{'ID':<5} | {'Fecha':<12} | {'Descripción':<25} | {'Usuario':<15} | {'Equipo':<15} | {'Eliminado':<9} | {'Creado':<19}")
        print("-" * 130)

        for result in cur.stored_results():
            for (id_h, fecha, desc, usuario, equipo, deleted, created, updated) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created.strftime("%Y-%m-%d %H:%M:%S") if created else "-"
                print(f"{id_h:<5} | {fecha} | {desc:<25} | {usuario:<15} | {equipo:<15} | {eliminado:<9} | {ca:<19}")

    except mysql.connector.Error as e:
        print("❌ Error al listar todos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_historial(id_h, fecha, descripcion, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_historial_equipo", [id_h, fecha, descripcion, usuario_id, equipo_id])
        cnx.commit()
        print("✅ Historial actualizado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def borrado_logico_historial(id_h):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_historial_equipo", [id_h])
        cnx.commit()
        print("✅ Historial eliminado lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al borrar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def restaurar_historial(id_h):
    cnx = cur = None
    try:
        cnx = conectar()
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_historial_equipo", [id_h])
        cnx.commit()
        print("✅ Historial restaurado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

# ===========================================================
# MENÚ
# ===========================================================
def menu():
    while True:
        print("""
============================================================
      GESTIÓN DE HISTORIAL DE EQUIPOS (MySQL + SP)
============================================================
1) Insertar nuevo historial
2) Listar historiales ACTIVOS
3) Listar todos los historiales
4) Actualizar historial
5) Borrado lógico de historial
6) Restaurar historial eliminado
0) Salir
------------------------------------------------------------""")
        op = input("Selecciona una opción: ")

        if op == "1":
            fecha = input("Fecha (YYYY-MM-DD): ")
            desc = input("Descripción: ")
            usuario = int(input("ID de usuario: "))
            equipo = int(input("ID de equipo: "))
            insertar_historial(fecha, desc, usuario, equipo)
        elif op == "2":
            listar_historiales_activos()
        elif op == "3":
            listar_historiales_todos()
        elif op == "4":
            id_h = int(input("ID del historial: "))
            fecha = input("Nueva fecha (YYYY-MM-DD): ")
            desc = input("Nueva descripción: ")
            usuario = int(input("Nuevo ID usuario: "))
            equipo = int(input("Nuevo ID equipo: "))
            actualizar_historial(id_h, fecha, desc, usuario, equipo)
        elif op == "5":
            id_h = int(input("ID del historial a eliminar: "))
            borrado_logico_historial(id_h)
        elif op == "6":
            id_h = int(input("ID del historial a restaurar: "))
            restaurar_historial(id_h)
        elif op == "0":
            print("👋 Saliendo...")
            break
        else:
            print("⚠️ Opción no válida.")

if __name__ == "__main__":
    menu()
