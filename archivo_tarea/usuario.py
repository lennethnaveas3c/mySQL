# ==========================================
# usuario.py
# Gestión de usuarios con SP en MySQL
# ==========================================

import mysql.connector
from getpass import getpass

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
def insertar_usuario(nombre, correo, contrasena, tipo_usuario_id, estado="Activo"):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        args = [nombre, correo, contrasena, tipo_usuario_id, estado, 0]  # OUT p_nuevo_id
        cur.callproc("sp_insertar_usuario", args)
        cnx.commit()
        nuevo_id = args[5]
        print(f"✅ Usuario insertado correctamente. ID: {nuevo_id}")
    except mysql.connector.Error as e:
        print("❌ Error al insertar usuario:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_usuarios_activos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_usuarios_activos")
        print("\n=== USUARIOS ACTIVOS ===")
        print(f"{'ID':<5} | {'Nombre':<15} | {'Correo':<25} | {'Tipo Usuario':<10} | {'Estado':<8} | {'Creado':<19}")
        print("-"*90)
        for result in cur.stored_results():
            for (id_usuario, nombre, correo, tipo_usuario_id, estado, created_at) in result.fetchall():
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_usuario:<5} | {nombre:<15} | {correo:<25} | {tipo_usuario_id:<10} | {estado:<8} | {ca}")
    except mysql.connector.Error as e:
        print("❌ Error al listar usuarios activos:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def listar_usuarios_todos():
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_listar_usuarios_todos")
        print("\n=== TODOS LOS USUARIOS ===")
        print(f"{'ID':<5} | {'Nombre':<15} | {'Correo':<25} | {'Tipo Usuario':<10} | {'Estado':<8} | {'Eliminado':<8} | {'Creado':<19}")
        print("-"*100)
        for result in cur.stored_results():
            for (id_usuario, nombre, correo, tipo_usuario_id, estado, created_at, deleted) in result.fetchall():
                eliminado = "SÍ" if deleted else "NO"
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_usuario:<5} | {nombre:<15} | {correo:<25} | {tipo_usuario_id:<10} | {estado:<8} | {eliminado:<8} | {ca}")
    except mysql.connector.Error as e:
        print("❌ Error al listar todos los usuarios:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def buscar_usuario_por_id(id_usuario):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.execute("""SELECT id_usuario, nombre, correo, tipo_usuario_id_tipo_usuario, estado, created_at, updated_at, deleted
                       FROM usuario WHERE id_usuario=%s""", (id_usuario,))
        res = cur.fetchone()
        if res:
            estado_elim = "ELIMINADO" if res[7] else "ACTIVO"
            print(f"\n=== DETALLE USUARIO ID {res[0]} ===")
            print(f"Nombre: {res[1]}")
            print(f"Correo: {res[2]}")
            print(f"Tipo de usuario ID: {res[3]}")
            print(f"Estado: {res[4]}")
            print(f"Creado: {res[5]}")
            print(f"Actualizado: {res[6]}")
            print(f"Eliminado: {estado_elim}")
        else:
            print("❌ No se encontró usuario con ese ID.")
    except mysql.connector.Error as e:
        print("❌ Error al buscar usuario:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def actualizar_usuario(id_usuario, nombre, correo, contrasena, tipo_usuario_id, estado):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_usuario", [id_usuario, nombre, correo, contrasena, tipo_usuario_id, estado])
        cnx.commit()
        print(f"✅ Usuario ID {id_usuario} actualizado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al actualizar usuario:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def borrado_logico_usuario(id_usuario):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_usuario", [id_usuario])
        cnx.commit()
        print(f"✅ Usuario ID {id_usuario} eliminado lógicamente.")
    except mysql.connector.Error as e:
        print("❌ Error al eliminar usuario:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

def restaurar_usuario(id_usuario):
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None: return
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_usuario", [id_usuario])
        cnx.commit()
        print(f"✅ Usuario ID {id_usuario} restaurado correctamente.")
    except mysql.connector.Error as e:
        print("❌ Error al restaurar usuario:", e)
    finally:
        if cur: cur.close()
        if cnx and cnx.is_connected(): cnx.close()

# ---------- MENÚ PRINCIPAL ----------
def menu():
    while True:
        print("\n" + "="*60)
        print("      GESTIÓN DE USUARIOS (MySQL + SP)")
        print("="*60)
        print("1) Insertar nuevo usuario")
        print("2) Listar usuarios ACTIVOS")
        print("3) Listar todos los usuarios")
        print("4) Buscar usuario por ID")
        print("5) Actualizar usuario")
        print("6) Borrado lógico de usuario")
        print("7) Restaurar usuario eliminado")
        print("0) Salir")
        print("-"*60)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\n--- NUEVO USUARIO ---")
            nombre = input("Nombre: ").strip()
            correo = input("Correo: ").strip()
            contrasena = getpass("Contraseña: ").strip()
            try:
                tipo_id = int(input("ID tipo de usuario: ").strip())
                estado = input("Estado (Activo/Inactivo) [Activo]: ").strip() or "Activo"
                insertar_usuario(nombre, correo, contrasena, tipo_id, estado)
            except ValueError:
                print("❌ ID tipo de usuario inválido.")

        elif opcion == "2":
            listar_usuarios_activos()

        elif opcion == "3":
            listar_usuarios_todos()

        elif opcion == "4":
            try:
                id_usuario = int(input("ID a buscar: ").strip())
                buscar_usuario_por_id(id_usuario)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "5":
            try:
                id_usuario = int(input("ID a actualizar: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                correo = input("Nuevo correo: ").strip()
                contrasena = getpass("Nueva contraseña: ").strip()
                tipo_id = int(input("Nuevo ID tipo de usuario: ").strip())
                estado = input("Nuevo estado (Activo/Inactivo): ").strip()
                actualizar_usuario(id_usuario, nombre, correo, contrasena, tipo_id, estado)
            except ValueError:
                print("❌ Entrada inválida.")

        elif opcion == "6":
            try:
                id_usuario = int(input("ID del usuario a eliminar: ").strip())
                borrado_logico_usuario(id_usuario)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "7":
            try:
                id_usuario = int(input("ID del usuario a restaurar: ").strip())
                restaurar_usuario(id_usuario)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "0":
            print("👋 Saliendo del sistema de usuarios...")
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
