import mysql.connector
from datetime import datetime

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
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None

# ---------- CRUD ----------
def insertar_mantenimiento(fecha, estado, descripcion, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        args = [fecha, estado, descripcion, usuario_id, equipo_id, 0]
        cur.callproc("sp_insertar_mantenimiento", args)
        cnx.commit()
        nuevo_id = args[5]

        if nuevo_id == -1:
            print("❌ Error: No existe usuario con ID", usuario_id)
        elif nuevo_id == -2:
            print("❌ Error: No existe equipo con ID", equipo_id)
        else:
            print(f"✅ Mantenimiento insertado correctamente. Nuevo ID: {nuevo_id}")

    except mysql.connector.Error as e:
        print("❌ Error al insertar mantenimiento:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_mantenimientos_activos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_mantenimientos_activos")
        print("\n=== MANTENIMIENTOS ACTIVOS ===")
        print(f"{'ID':<5} | {'Fecha':<12} | {'Estado':<12} | {'Descripción':<25} | {'Usuario':<12} | {'Equipo':<12} | {'Creado':<19} | {'Actualizado':<19}")
        print("-"*120)
        for result in cur.stored_results:
            for (id_m, fecha, estado, desc, usuario, equipo, created, updated) in result.fetchall():
                ca = created.strftime("%Y-%m-%d %H:%M:%S") if created else "-"
                ua = updated.strftime("%Y-%m-%d %H:%M:%S") if updated else "-"
                print(f"{id_m:<5} | {fecha} | {estado:<12} | {desc:<25} | {usuario:<12} | {equipo:<12} | {ca:<19} | {ua:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar mantenimientos activos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_mantenimientos_todos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_mantenimientos_todos")
        print("\n=== TODOS LOS MANTENIMIENTOS ===")
        print(f"{'ID':<5} | {'Fecha':<12} | {'Estado':<12} | {'Descripción':<25} | {'Usuario':<12} | {'Equipo':<12} | {'Eliminado':<8} | {'Creado':<19}")
        print("-"*130)
        for result in cur.stored_results:
            for (id_m, fecha, estado, desc, usuario, equipo, created, updated, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created.strftime("%Y-%m-%d %H:%M:%S") if created else "-"
                print(f"{id_m:<5} | {fecha} | {estado:<12} | {desc:<25} | {usuario:<12} | {equipo:<12} | {eliminado:<8} | {ca:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todos los mantenimientos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_mantenimiento(id_m, fecha, estado, desc, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_mantenimiento", [id_m, fecha, estado, desc, usuario_id, equipo_id])
        cnx.commit()
        print(f"✅ Mantenimiento ID {id_m} actualizado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar mantenimiento:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def borrado_logico_mantenimiento(id_m):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_mantenimiento", [id_m])
        cnx.commit()
        print(f"✅ Mantenimiento ID {id_m} eliminado lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al eliminar mantenimiento:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def restaurar_mantenimiento(id_m):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_mantenimiento", [id_m])
        cnx.commit()
        print(f"✅ Mantenimiento ID {id_m} restaurado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar mantenimiento:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()
