# ==========================================
# tipo_usuario.py (versión adaptada al formato del profesor)
# Autor: Lenneth Naveas
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


# ---------- FUNCIONES ----------
def insertar_tipo_usuario(nombre, cargo, sueldo):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()
        args = [nombre, cargo, str(sueldo), 0]  # el último valor es el OUT p_nuevo_id
        cur.callproc("sp_insertar_tipo_usuario", args)
        cnx.commit()
        nuevo_id = args[3]
        print(f"✅ Registro insertado correctamente con ID: {nuevo_id}")
    except mysql.connector.Error as e:
        print("❌ Error al insertar el tipo de usuario:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()


def listar_tipos_activos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()
        cur.callproc("sp_listar_tipos_usuario_activos")
        print("\n=== LISTA DE EMPLEADOS ACTIVOS ===")
        print(f"{'ID':<5} | {'Nombre':<15} | {'Cargo':<20} | {'Sueldo':<10} | {'Creado':<19} | {'Actualizado':<19}")
        print("-"*95)
        for result in cur.stored_results():
            for (id_tipo, nombre, cargo, sueldo, created_at, updated_at) in result.fetchall():
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                ua = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else "-"
                print(f"{id_tipo:<5} | {nombre:<15} | {cargo:<20} | {sueldo:<10} | {ca:<19} | {ua:<19}")
    except mysql.connector.Error as e:
        print("❌ Error al listar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()


def listar_todos_tipos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()
        cur.callproc("sp_listar_tipos_usuario_todos")
        print("\n=== LISTA COMPLETA DE EMPLEADOS ===")
        print(f"{'ID':<5} | {'Nombre':<15} | {'Cargo':<20} | {'Sueldo':<10} | {'Eliminado':<10}")
        print("-"*70)
        for result in cur.stored_results():
            for (id_tipo, nombre, cargo, sueldo, created_at, updated_at, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                print(f"{id_tipo:<5} | {nombre:<15} | {cargo:<20} | {sueldo:<10} | {eliminado:<10}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()


def buscar_por_id(id_tipo):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()
        cur.execute("SELECT id_tipo_usuario, nombre_tipo, descripcion, estado FROM tipo_usuario WHERE id_tipo_usuario = %s", (id_tipo,))
        res = cur.fetchone()
        if res:
            print(f"\n=== DETALLE DEL EMPLEADO ID {res[0]} ===")
            print(f"Nombre: {res[1]}")
            print(f"Cargo: {res[2]}")
            print(f"Sueldo: {res[3]}")
        else:
            print("❌ No se encontró el empleado con ese ID.")
    except mysql.connector.Error as e:
        print("❌ Error al buscar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()


def actualizar_tipo_usuario(id_tipo, nombre, cargo, sueldo):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_tipo_usuario", [id_tipo, nombre, cargo, str(sueldo)])
        cnx.commit()
        print(f"✅ Empleado ID {id_tipo} actualizado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()


def borrado_logico(id_tipo):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_tipo_usuario", [id_tipo])
        cnx.commit()
        print(f"✅ Empleado ID {id_tipo} eliminado lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al eliminar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()


def restaurar_tipo(id_tipo):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: 
            return
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_tipo_usuario", [id_tipo])
        cnx.commit()
        print(f"✅ Empleado ID {id_tipo} restaurado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()


# ---------- MENÚ PRINCIPAL ----------
def menu():
    while True:
        print("\n" + "="*60)
        print("      GESTIÓN DE EMPLEADOS (versión tipo_usuario)")
        print("="*60)
        print("1) Insertar nuevo empleado")
        print("2) Listar empleados ACTIVOS")
        print("3) Listar todos los empleados")
        print("4) Buscar empleado por ID")
        print("5) Actualizar empleado")
        print("6) Borrado lógico de empleado")
        print("7) Restaurar empleado eliminado")
        print("0) Salir")
        print("-"*60)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\n--- NUEVO EMPLEADO ---")
            nombre = input("Nombre: ").strip()
            cargo = input("Cargo: ").strip()
            try:
                sueldo = float(input("Sueldo: ").strip())
                insertar_tipo_usuario(nombre, cargo, sueldo)
            except ValueError:
                print("❌ Sueldo inválido, debe ser numérico.")

        elif opcion == "2":
            listar_tipos_activos()

        elif opcion == "3":
            listar_todos_tipos()

        elif opcion == "4":
            try:
                id_tipo = int(input("ID a buscar: ").strip())
                buscar_por_id(id_tipo)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "5":
            try:
                id_tipo = int(input("ID del empleado a actualizar: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                cargo = input("Nuevo cargo: ").strip()
                sueldo = float(input("Nuevo sueldo: ").strip())
                actualizar_tipo_usuario(id_tipo, nombre, cargo, sueldo)
            except ValueError:
                print("❌ Entrada inválida.")

        elif opcion == "6":
            try:
                id_tipo = int(input("ID del empleado a eliminar: ").strip())
                borrado_logico(id_tipo)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "7":
            try:
                id_tipo = int(input("ID del empleado a restaurar: ").strip())
                restaurar_tipo(id_tipo)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "0":
            print("👋 Saliendo del sistema de empleados...")
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
