# ==========================================
# historial_equipo.py
# Gestión de historial de equipos con SP en MySQL
# ==========================================

import mysql.connector
from datetime import datetime

# ---------- CONFIGURACIÓN DE CONEXIÓN ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",  # Cambia si tu contraseña es distinta
    "database": "proyecto",
    "port": 3306
}

# ---------- FUNCIÓN DE CONEXIÓN ----------
def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None

# ---------- FUNCIONES CRUD ----------
def insertar_historial(fecha, descripcion, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        args = [fecha, descripcion, usuario_id, equipo_id, 0]  # OUT inicializado en 0
        cur.callproc("sp_insertar_historial_equipo", args)
        cnx.commit()
        nuevo_id = args[4]

        if nuevo_id == -1:
            print("❌ Error: No existe usuario con ID", usuario_id)
        elif nuevo_id == -2:
            print("❌ Error: No existe equipo con ID", equipo_id)
        else:
            print(f"✅ Historial insertado correctamente. Nuevo ID: {nuevo_id}")

    except mysql.connector.Error as e:
        print("❌ Error al insertar historial:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_historial_activo():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_historial_activos")
        print("\n=== HISTORIAL DE EQUIPOS ACTIVOS ===")
        print(f"{'ID':<5} | {'Fecha':<12} | {'Descripción':<30} | {'Usuario':<12} | {'Equipo':<12} | {'Creado':<19} | {'Actualizado':<19}")
        print("-"*120)
        for result in cur.stored_results():
            for (id_h, fecha, desc, usuario, equipo, created, updated) in result.fetchall():
                ca = created.strftime("%Y-%m-%d %H:%M:%S") if created else "-"
                ua = updated.strftime("%Y-%m-%d %H:%M:%S") if updated else "-"
                print(f"{id_h:<5} | {fecha} | {desc:<30} | {usuario:<12} | {equipo:<12} | {ca:<19} | {ua:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar historial activo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_historial_todos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_historial_todos")
        print("\n=== TODOS LOS HISTORIALES DE EQUIPOS ===")
        print(f"{'ID':<5} | {'Fecha':<12} | {'Descripción':<30} | {'Usuario':<12} | {'Equipo':<12} | {'Eliminado':<8} | {'Creado':<19}")
        print("-"*130)
        for result in cur.stored_results():
            for (id_h, fecha, desc, usuario, equipo, created, updated, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created.strftime("%Y-%m-%d %H:%M:%S") if created else "-"
                print(f"{id_h:<5} | {fecha} | {desc:<30} | {usuario:<12} | {equipo:<12} | {eliminado:<8} | {ca:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todos los historiales:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_historial(id_h, fecha, desc, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_historial_equipo", [id_h, fecha, desc, usuario_id, equipo_id])
        cnx.commit()
        print(f"✅ Historial ID {id_h} actualizado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar historial:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def borrado_logico_historial(id_h):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_historial_equipo", [id_h])
        cnx.commit()
        print(f"✅ Historial ID {id_h} eliminado lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al eliminar historial:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def restaurar_historial(id_h):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_historial_equipo", [id_h])
        cnx.commit()
        print(f"✅ Historial ID {id_h} restaurado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar historial:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

# ---------- MENÚ PRINCIPAL ----------
def menu():
    while True:
        print("\n" + "="*60)
        print("      GESTIÓN DE HISTORIAL DE EQUIPOS (MySQL + SP)")
        print("="*60)
        print("1) Insertar nuevo historial")
        print("2) Listar historiales ACTIVOS")
        print("3) Listar todos los historiales")
        print("4) Actualizar historial")
        print("5) Borrado lógico de historial")
        print("6) Restaurar historial eliminado")
        print("0) Salir")
        print("-"*60)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            estado = input("Descripción: ").strip()
            try:
                usuario_id = int(input("ID de usuario: ").strip())
                equipo_id = int(input("ID de equipo: ").strip())
                insertar_historial(fecha, estado, usuario_id, equipo_id)
            except ValueError:
                print("❌ Entrada inválida.")
        elif opcion == "2":
            listar_historial_activo()
        elif opcion == "3":
            listar_historial_todos()
        elif opcion == "4":
            try:
                id_h = int(input("ID a actualizar: ").strip())
                fecha = input("Nueva fecha (YYYY-MM-DD): ").strip()
                desc = input("Nueva descripción: ").strip()
                usuario_id = int(input("Nuevo ID de usuario: ").strip())
                equipo_id = int(input("Nuevo ID de equipo: ").strip())
                actualizar_historial(id_h, fecha, desc, usuario_id, equipo_id)
            except ValueError:
                print("❌ Entrada inválida.")
        elif opcion == "5":
            try:
                id_h = int(input("ID a eliminar: ").strip())
                borrado_logico_historial(id_h)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "6":
            try:
                id_h = int(input("ID a restaurar: ").strip())
                restaurar_historial(id_h)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "0":
            print("👋 Saliendo del sistema de historial de equipos...")
            break
        else:
            print("❌ Opción no válida. Intenta nuevamente.")

# ---------- EJECUCIÓN ----------
if __name__ == "__main__":
    conexion = conectar()
    if conexion:
        print("✅ Conexión a la base de datos establecida correctamente")
        conexion.close()
        menu()
    else:
        print("❌ No se pudo conectar a la base de datos.")
