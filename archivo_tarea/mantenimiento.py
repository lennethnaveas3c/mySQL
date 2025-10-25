# ==========================================
# mantenimiento.py
# Gestión de mantenimientos con SP en MySQL
# ==========================================

import mysql.connector
from datetime import datetime

# ---------- CONFIGURACIÓN DE CONEXIÓN ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
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
def insertar_mantenimiento(fecha, estado, descripcion, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()

        # Validar que el usuario exista
        cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario=%s AND deleted=0", (usuario_id,))
        if cur.fetchone() is None:
            print(f"❌ Error: No existe usuario con ID {usuario_id}")
            return

        # Validar que el equipo exista
        cur.execute("SELECT id_equipo FROM equipo WHERE id_equipo=%s AND deleted=0", (equipo_id,))
        if cur.fetchone() is None:
            print(f"❌ Error: No existe equipo con ID {equipo_id}")
            return

        # Llamada al SP
        args = [fecha, estado, descripcion, usuario_id, equipo_id, 0]  # 0 para OUT id_mantenimiento
        cur.callproc("sp_insertar_mantenimiento", args)
        cnx.commit()

        nuevo_id = args[5]
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
        print(f"{'ID':<5} | {'Fecha':<12} | {'Estado':<12} | {'Descripción':<30} | {'Usuario':<15} | {'Equipo':<15} | {'Creado':<19} | {'Actualizado':<19}")
        print("-"*140)
        for result in cur.stored_results():
            for (id_m, fecha, estado, descripcion, usuario, equipo, created_at, updated_at) in result.fetchall():
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                ua = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else "-"
                print(f"{id_m:<5} | {fecha:<12} | {estado:<12} | {descripcion:<30} | {usuario:<15} | {equipo:<15} | {ca:<19} | {ua:<19}")
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
        print(f"{'ID':<5} | {'Fecha':<12} | {'Estado':<12} | {'Descripción':<30} | {'Usuario':<15} | {'Equipo':<15} | {'Eliminado':<8} | {'Creado':<19}")
        print("-"*140)
        for result in cur.stored_results():
            for (id_m, fecha, estado, descripcion, usuario, equipo, created_at, updated_at, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_m:<5} | {fecha:<12} | {estado:<12} | {descripcion:<30} | {usuario:<15} | {equipo:<15} | {eliminado:<8} | {ca:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todos los mantenimientos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_mantenimiento(id_m, fecha, estado, descripcion, usuario_id, equipo_id):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()

        # Validaciones de FK
        cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario=%s AND deleted=0", (usuario_id,))
        if cur.fetchone() is None:
            print(f"❌ Error: No existe usuario con ID {usuario_id}")
            return

        cur.execute("SELECT id_equipo FROM equipo WHERE id_equipo=%s AND deleted=0", (equipo_id,))
        if cur.fetchone() is None:
            print(f"❌ Error: No existe equipo con ID {equipo_id}")
            return

        cur.callproc("sp_actualizar_mantenimiento", [id_m, fecha, estado, descripcion, usuario_id, equipo_id])
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

# ---------- MENÚ PRINCIPAL ----------
def menu():
    while True:
        print("\n" + "="*70)
        print("      GESTIÓN DE MANTENIMIENTOS (MySQL + SP)")
        print("="*70)
        print("1) Insertar nuevo mantenimiento")
        print("2) Listar mantenimientos ACTIVOS")
        print("3) Listar todos los mantenimientos")
        print("4) Actualizar mantenimiento")
        print("5) Borrado lógico de mantenimiento")
        print("6) Restaurar mantenimiento eliminado")
        print("0) Salir")
        print("-"*70)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            estado = input("Estado (Pendiente/Completado/etc.): ").strip()
            descripcion = input("Descripción: ").strip()
            try:
                usuario_id = int(input("ID de usuario: ").strip())
                equipo_id = int(input("ID de equipo: ").strip())
                insertar_mantenimiento(fecha, estado, descripcion, usuario_id, equipo_id)
            except ValueError:
                print("❌ Entrada inválida. IDs deben ser números.")
        elif opcion == "2":
            listar_mantenimientos_activos()
        elif opcion == "3":
            listar_mantenimientos_todos()
        elif opcion == "4":
            try:
                id_m = int(input("ID a actualizar: ").strip())
                fecha = input("Nueva fecha (YYYY-MM-DD): ").strip()
                estado = input("Nuevo estado: ").strip()
                descripcion = input("Nueva descripción: ").strip()
                usuario_id = int(input("Nuevo ID de usuario: ").strip())
                equipo_id = int(input("Nuevo ID de equipo: ").strip())
                actualizar_mantenimiento(id_m, fecha, estado, descripcion, usuario_id, equipo_id)
            except ValueError:
                print("❌ Entrada inválida.")
        elif opcion == "5":
            try:
                id_m = int(input("ID a eliminar: ").strip())
                borrado_logico_mantenimiento(id_m)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "6":
            try:
                id_m = int(input("ID a restaurar: ").strip())
                restaurar_mantenimiento(id_m)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "0":
            print("👋 Saliendo del sistema de mantenimientos...")
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
