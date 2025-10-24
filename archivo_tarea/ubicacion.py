# ==========================================
# ubicacion.py
# Gestión de ubicaciones con SP en MySQL
# ==========================================

import mysql.connector

# ---------- CONFIGURACIÓN DE CONEXIÓN ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",  # cambia si tu contraseña es distinta
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
def insertar_ubicacion(nombre, descripcion):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()

        # 🔹 Llamada correcta al SP con parámetro OUT inicializado
        args = [nombre, descripcion, 0]  # <-- 0 es valor inicial para OUT
        cur.callproc("sp_insertar_ubicacion", args)
        cnx.commit()

        # 🔹 Obtenemos el ID generado del OUT
        nuevo_id = args[2]
        print(f"✅ Ubicación insertada correctamente. Nuevo ID: {nuevo_id}")

    except mysql.connector.Error as e:
        print(f"❌ Error al insertar ubicación: {e}")

    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_ubicaciones_activas():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_ubicaciones_activas")
        print("\n=== UBICACIONES ACTIVAS ===")
        print(f"{'ID':<5} | {'Nombre':<20} | {'Descripción':<30} | {'Creado':<19} | {'Actualizado':<19}")
        print("-"*100)
        for result in cur.stored_results():
            for (id_ubicacion, nombre, descripcion, created_at, updated_at) in result.fetchall():
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                ua = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else "-"
                print(f"{id_ubicacion:<5} | {nombre:<20} | {descripcion:<30} | {ca:<19} | {ua:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar ubicaciones activas:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_ubicaciones_todas():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_ubicaciones_todas")
        print("\n=== TODAS LAS UBICACIONES ===")
        print(f"{'ID':<5} | {'Nombre':<20} | {'Descripción':<30} | {'Eliminado':<8} | {'Creado':<19}")
        print("-"*90)
        for result in cur.stored_results():
            for (id_ubicacion, nombre, descripcion, created_at, updated_at, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_ubicacion:<5} | {nombre:<20} | {descripcion:<30} | {eliminado:<8} | {ca:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todas las ubicaciones:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def buscar_ubicacion_por_id(id_ubicacion):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.execute("""SELECT id_ubicacion, nombre_ubicacion, descripcion_ubicacion, created_at, updated_at, deleted
                       FROM ubicacion WHERE id_ubicacion=%s""", (id_ubicacion,))
        res = cur.fetchone()
        if res:
            estado_elim = "ELIMINADO" if res[5] else "ACTIVO"
            print(f"\n=== DETALLE UBICACIÓN ID {res[0]} ===")
            print(f"Nombre: {res[1]}")
            print(f"Descripción: {res[2]}")
            print(f"Creado: {res[3]}")
            print(f"Actualizado: {res[4]}")
            print(f"Eliminado: {estado_elim}")
        else:
            print("❌ No se encontró ubicación con ese ID.")
    except mysql.connector.Error as e:
        print("❌ Error al buscar ubicación:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_ubicacion(id_ubicacion, nombre, descripcion):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_ubicacion", [id_ubicacion, nombre, descripcion])
        cnx.commit()
        print(f"✅ Ubicación ID {id_ubicacion} actualizada correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar ubicación:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def borrado_logico_ubicacion(id_ubicacion):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_ubicacion", [id_ubicacion])
        cnx.commit()
        print(f"✅ Ubicación ID {id_ubicacion} eliminada lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al eliminar ubicación:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def restaurar_ubicacion(id_ubicacion):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_ubicacion", [id_ubicacion])
        cnx.commit()
        print(f"✅ Ubicación ID {id_ubicacion} restaurada correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar ubicación:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

# ---------- MENÚ PRINCIPAL ----------
def menu():
    while True:
        print("\n" + "="*60)
        print("      GESTIÓN DE UBICACIONES (MySQL + SP)")
        print("="*60)
        print("1) Insertar nueva ubicación")
        print("2) Listar ubicaciones ACTIVAS")
        print("3) Listar todas las ubicaciones")
        print("4) Buscar ubicación por ID")
        print("5) Actualizar ubicación")
        print("6) Borrado lógico de ubicación")
        print("7) Restaurar ubicación eliminada")
        print("0) Salir")
        print("-"*60)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\n--- NUEVA UBICACIÓN ---")
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción: ").strip()
            insertar_ubicacion(nombre, descripcion)

        elif opcion == "2":
            listar_ubicaciones_activas()

        elif opcion == "3":
            listar_ubicaciones_todas()

        elif opcion == "4":
            try:
                id_ubicacion = int(input("ID a buscar: ").strip())
                buscar_ubicacion_por_id(id_ubicacion)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "5":
            try:
                id_ubicacion = int(input("ID a actualizar: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                descripcion = input("Nueva descripción: ").strip()
                actualizar_ubicacion(id_ubicacion, nombre, descripcion)
            except ValueError:
                print("❌ Entrada inválida.")

        elif opcion == "6":
            try:
                id_ubicacion = int(input("ID de la ubicación a eliminar: ").strip())
                borrado_logico_ubicacion(id_ubicacion)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "7":
            try:
                id_ubicacion = int(input("ID de la ubicación a restaurar: ").strip())
                restaurar_ubicacion(id_ubicacion)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "0":
            print("👋 Saliendo del sistema de ubicaciones...")
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
