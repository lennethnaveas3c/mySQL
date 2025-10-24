# ==========================================
# equipo.py
# Gestión de equipos con SP en MySQL
# ==========================================

import mysql.connector

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
def insertar_equipo(nombre, estado, ubicacion_id, tipo_equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        args = [nombre, estado, ubicacion_id, tipo_equipo_id, 0]  # OUT inicializado en 0
        cur.callproc("sp_insertar_equipo", args)
        cnx.commit()
        nuevo_id = args[4]
        print(f"✅ Equipo insertado correctamente. Nuevo ID: {nuevo_id}")
    except mysql.connector.Error as e:
        print("❌ Error al insertar equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_equipos_activos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_equipos_activas")
        print("\n=== EQUIPOS ACTIVOS ===")
        print(f"{'ID':<5} | {'Nombre':<20} | {'Estado':<12} | {'Ubicación':<15} | {'Tipo':<15} | {'Creado':<19} | {'Actualizado':<19}")
        print("-"*110)
        for result in cur.stored_results():
            for (id_eq, nombre, estado, ubicacion, tipo, created_at, updated_at) in result.fetchall():
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                ua = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else "-"
                print(f"{id_eq:<5} | {nombre:<20} | {estado:<12} | {ubicacion:<15} | {tipo:<15} | {ca:<19} | {ua:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar equipos activos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_equipos_todos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_equipos_todos")
        print("\n=== TODOS LOS EQUIPOS ===")
        print(f"{'ID':<5} | {'Nombre':<20} | {'Estado':<12} | {'Ubicación':<15} | {'Tipo':<15} | {'Eliminado':<8} | {'Creado':<19}")
        print("-"*110)
        for result in cur.stored_results():
            for (id_eq, nombre, estado, ubicacion, tipo, created_at, updated_at, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_eq:<5} | {nombre:<20} | {estado:<12} | {ubicacion:<15} | {tipo:<15} | {eliminado:<8} | {ca:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todos los equipos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_equipo(id_eq, nombre, estado, ubicacion_id, tipo_equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_equipo", [id_eq, nombre, estado, ubicacion_id, tipo_equipo_id])
        cnx.commit()
        print(f"✅ Equipo ID {id_eq} actualizado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def borrado_logico_equipo(id_eq):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_equipo", [id_eq])
        cnx.commit()
        print(f"✅ Equipo ID {id_eq} eliminado lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al eliminar equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def restaurar_equipo(id_eq):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_equipo", [id_eq])
        cnx.commit()
        print(f"✅ Equipo ID {id_eq} restaurado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

# ---------- MENÚ PRINCIPAL ----------
def menu():
    while True:
        print("\n" + "="*60)
        print("      GESTIÓN DE EQUIPOS (MySQL + SP)")
        print("="*60)
        print("1) Insertar nuevo equipo")
        print("2) Listar equipos ACTIVOS")
        print("3) Listar todos los equipos")
        print("4) Actualizar equipo")
        print("5) Borrado lógico de equipo")
        print("6) Restaurar equipo eliminado")
        print("0) Salir")
        print("-"*60)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            estado = input("Estado (Operativo/Inactivo/etc.): ").strip()
            try:
                ubicacion_id = int(input("ID de ubicación: ").strip())
                tipo_equipo_id = int(input("ID de tipo de equipo: ").strip())
                insertar_equipo(nombre, estado, ubicacion_id, tipo_equipo_id)
            except ValueError:
                print("❌ Entrada inválida.")
        elif opcion == "2":
            listar_equipos_activos()
        elif opcion == "3":
            listar_equipos_todos()
        elif opcion == "4":
            try:
                id_eq = int(input("ID a actualizar: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                estado = input("Nuevo estado: ").strip()
                ubicacion_id = int(input("Nuevo ID de ubicación: ").strip())
                tipo_equipo_id = int(input("Nuevo ID de tipo de equipo: ").strip())
                actualizar_equipo(id_eq, nombre, estado, ubicacion_id, tipo_equipo_id)
            except ValueError:
                print("❌ Entrada inválida.")
        elif opcion == "5":
            try:
                id_eq = int(input("ID a eliminar: ").strip())
                borrado_logico_equipo(id_eq)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "6":
            try:
                id_eq = int(input("ID a restaurar: ").strip())
                restaurar_equipo(id_eq)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "0":
            print("👋 Saliendo del sistema de equipos...")
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
