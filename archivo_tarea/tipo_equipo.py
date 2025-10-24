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
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None

# ---------- FUNCIONES CRUD ----------
def insertar_tipo_equipo(nombre, descripcion):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        args = [nombre, descripcion, 0]  # OUT inicializado en 0
        cur.callproc("sp_insertar_tipo_equipo", args)
        cnx.commit()
        nuevo_id = args[2]
        print(f"✅ Tipo de equipo insertado correctamente. Nuevo ID: {nuevo_id}")
    except mysql.connector.Error as e:
        print("❌ Error al insertar tipo de equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_tipos_equipo_activas():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_tipos_equipo_activas")
        print("\n=== TIPOS DE EQUIPO ACTIVOS ===")
        print(f"{'ID':<5} | {'Nombre':<20} | {'Descripción':<30} | {'Creado':<19} | {'Actualizado':<19}")
        print("-"*100)
        for result in cur.stored_results():
            for (id_te, nombre, descripcion, created_at, updated_at) in result.fetchall():
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                ua = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else "-"
                print(f"{id_te:<5} | {nombre:<20} | {descripcion:<30} | {ca:<19} | {ua:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar tipos de equipo activos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_tipos_equipo_todas():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_tipos_equipo_todas")
        print("\n=== TODOS LOS TIPOS DE EQUIPO ===")
        print(f"{'ID':<5} | {'Nombre':<20} | {'Descripción':<30} | {'Eliminado':<8} | {'Creado':<19}")
        print("-"*90)
        for result in cur.stored_results():
            for (id_te, nombre, descripcion, created_at, updated_at, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_te:<5} | {nombre:<20} | {descripcion:<30} | {eliminado:<8} | {ca:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todos los tipos de equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_tipo_equipo(id_te, nombre, descripcion):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_tipo_equipo", [id_te, nombre, descripcion])
        cnx.commit()
        print(f"✅ Tipo de equipo ID {id_te} actualizado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar tipo de equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def borrado_logico_tipo_equipo(id_te):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_tipo_equipo", [id_te])
        cnx.commit()
        print(f"✅ Tipo de equipo ID {id_te} eliminado lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al eliminar tipo de equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def restaurar_tipo_equipo(id_te):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_tipo_equipo", [id_te])
        cnx.commit()
        print(f"✅ Tipo de equipo ID {id_te} restaurado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar tipo de equipo:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

# ---------- MENÚ PRINCIPAL ----------
def menu():
    while True:
        print("\n" + "="*60)
        print("      GESTIÓN DE TIPOS DE EQUIPO (MySQL + SP)")
        print("="*60)
        print("1) Insertar nuevo tipo de equipo")
        print("2) Listar tipos de equipo ACTIVOS")
        print("3) Listar todos los tipos de equipo")
        print("4) Actualizar tipo de equipo")
        print("5) Borrado lógico de tipo de equipo")
        print("6) Restaurar tipo de equipo eliminado")
        print("0) Salir")
        print("-"*60)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción: ").strip()
            insertar_tipo_equipo(nombre, descripcion)
        elif opcion == "2":
            listar_tipos_equipo_activas()
        elif opcion == "3":
            listar_tipos_equipo_todas()
        elif opcion == "4":
            try:
                id_te = int(input("ID a actualizar: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                descripcion = input("Nueva descripción: ").strip()
                actualizar_tipo_equipo(id_te, nombre, descripcion)
            except ValueError:
                print("❌ Entrada inválida.")
        elif opcion == "5":
            try:
                id_te = int(input("ID a eliminar: ").strip())
                borrado_logico_tipo_equipo(id_te)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "6":
            try:
                id_te = int(input("ID a restaurar: ").strip())
                restaurar_tipo_equipo(id_te)
            except ValueError:
                print("❌ ID inválido.")
        elif opcion == "0":
            print("👋 Saliendo del sistema de tipos de equipo...")
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
