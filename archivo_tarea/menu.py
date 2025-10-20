# ==========================================
# sp_gestion_tipos_usuario.py
# CRUD para la tabla tipo_usuario con Procedimientos Almacenados
# Autor: [Lenneth Naveas]
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
    """
    Crea y devuelve una conexión a MySQL usando los parámetros definidos en DB_CONFIG.
    """
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print(f"❌ Error de conexión: {e}")
        return None

# ---------- PROCEDIMIENTOS ALMACENADOS (debes crearlos en MySQL) ----------
"""
-- Procedimiento para insertar tipo de usuario
DELIMITER $$
CREATE PROCEDURE sp_insertar_tipo_usuario(
    IN p_nombre_tipo VARCHAR(45),
    IN p_descripcion VARCHAR(100),
    IN p_estado VARCHAR(20),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO tipo_usuario (nombre_tipo, descripcion, estado)
    VALUES (p_nombre_tipo, p_descripcion, p_estado);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$
DELIMITER ;

-- Procedimiento para listar tipos de usuario activos
DELIMITER $$
CREATE PROCEDURE sp_listar_tipos_usuario_activos()
BEGIN
    SELECT id_tipo_usuario, nombre_tipo, descripcion, estado, created_at, updated_at
    FROM tipo_usuario 
    WHERE deleted = 0;
END$$
DELIMITER ;

-- Procedimiento para listar todos los tipos de usuario
DELIMITER $$
CREATE PROCEDURE sp_listar_tipos_usuario_todos()
BEGIN
    SELECT id_tipo_usuario, nombre_tipo, descripcion, estado, created_at, updated_at, deleted
    FROM tipo_usuario;
END$$
DELIMITER ;

-- Procedimiento para borrado lógico
DELIMITER $$
CREATE PROCEDURE sp_borrado_logico_tipo_usuario(IN p_id INT)
BEGIN
    UPDATE tipo_usuario 
    SET deleted = 1, updated_at = CURRENT_TIMESTAMP 
    WHERE id_tipo_usuario = p_id AND deleted = 0;
END$$
DELIMITER ;

-- Procedimiento para restaurar
DELIMITER $$
CREATE PROCEDURE sp_restaurar_tipo_usuario(IN p_id INT)
BEGIN
    UPDATE tipo_usuario 
    SET deleted = 0, updated_at = CURRENT_TIMESTAMP 
    WHERE id_tipo_usuario = p_id AND deleted = 1;
END$$
DELIMITER ;

-- Procedimiento para actualizar tipo de usuario
DELIMITER $$
CREATE PROCEDURE sp_actualizar_tipo_usuario(
    IN p_id INT,
    IN p_nombre_tipo VARCHAR(45),
    IN p_descripcion VARCHAR(100),
    IN p_estado VARCHAR(20)
)
BEGIN
    UPDATE tipo_usuario 
    SET nombre_tipo = p_nombre_tipo,
        descripcion = p_descripcion,
        estado = p_estado,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_usuario = p_id AND deleted = 0;
END$$
DELIMITER ;
"""

# ---------- FUNCIONES CRUD ----------
def sp_insertar_tipo_usuario(nombre_tipo: str, descripcion: str, estado: str = "Activo") -> int:
    """
    Inserta un nuevo tipo de usuario llamando al procedimiento almacenado.
    Devuelve el ID generado o -1 si ocurre un error.
    """
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None:
            return -1
            
        cur = cnx.cursor()
        args = [nombre_tipo, descripcion, estado, 0]
        cur.callproc("sp_insertar_tipo_usuario", args)
        cnx.commit()
        nuevo_id = args[3]
        print(f"✅ Tipo de usuario insertado correctamente. Nuevo ID: {nuevo_id}")
        return nuevo_id
    except mysql.connector.Error as e:
        print("❌ Error en sp_insertar_tipo_usuario:", e)
        if cnx and cnx.is_connected():
            try:
                cnx.rollback()
            except:
                pass
        return -1
    finally:
        if cur: 
            cur.close()
        if cnx and cnx.is_connected(): 
            cnx.close()

def sp_listar_tipos_activos():
    """
    Lista todos los tipos de usuario activos (deleted = 0).
    """
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None:
            return
            
        cur = cnx.cursor()
        cur.callproc("sp_listar_tipos_usuario_activos")
        
        print("\n=== TIPOS DE USUARIO ACTIVOS ===")
        print(f"{'ID':<3} | {'Nombre Tipo':<15} | {'Descripción':<25} | {'Estado':<10} | {'Creado':<19} | {'Actualizado':<19}")
        print("-" * 100)
        
        for result in cur.stored_results():
            for (id_tipo, nombre, descripcion, estado, created_at, updated_at) in result.fetchall():
                ua = updated_at.strftime("%Y-%m-%d %H:%M:%S") if updated_at else "-"
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_tipo:<3} | {nombre:<15} | {descripcion:<25} | {estado:<10} | {ca} | {ua}")
                
    except mysql.connector.Error as e:
        print("❌ Error en sp_listar_tipos_activos:", e)
    finally:
        if cur: 
            cur.close()
        if cnx and cnx.is_connected(): 
            cnx.close()

def sp_listar_todos_tipos():
    """
    Lista todos los tipos de usuario, incluyendo eliminados.
    """
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None:
            return
            
        cur = cnx.cursor()
        cur.callproc("sp_listar_tipos_usuario_todos")
        
        print("\n=== TIPOS DE USUARIO (TODOS) ===")
        print(f"{'ID':<3} | {'Nombre':<15} | {'Descripción':<25} | {'Estado':<10} | {'Eliminado':<9} | {'Creado':<19}")
        print("-" * 120)
        
        for result in cur.stored_results():
            for (id_tipo, nombre, descripcion, estado, created_at, updated_at, deleted) in result.fetchall():
                estado_eliminado = "SÍ" if deleted == 1 else "NO"
                ca = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
                print(f"{id_tipo:<3} | {nombre:<15} | {descripcion:<25} | {estado:<10} | {estado_eliminado:<9} | {ca}")
                
    except mysql.connector.Error as e:
        print("❌ Error en sp_listar_todos_tipos:", e)
    finally:
        if cur: 
            cur.close()
        if cnx and cnx.is_connected(): 
            cnx.close()

def sp_borrado_logico_tipo(id_tipo: int):
    """
    Aplica borrado lógico a un tipo de usuario.
    """
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None:
            return
            
        cur = cnx.cursor()
        cur.callproc("sp_borrado_logico_tipo_usuario", [id_tipo])
        cnx.commit()
        
        if cur.rowcount > 0:
            print(f"✅ Borrado lógico aplicado al tipo de usuario ID {id_tipo}.")
        else:
            print(f"⚠️  No se encontró el tipo de usuario ID {id_tipo} o ya estaba eliminado.")
            
    except mysql.connector.Error as e:
        print("❌ Error en sp_borrado_logico_tipo:", e)
        if cnx and cnx.is_connected():
            try: 
                cnx.rollback()
            except: 
                pass
    finally:
        if cur: 
            cur.close()
        if cnx and cnx.is_connected(): 
            cnx.close()

def sp_restaurar_tipo(id_tipo: int):
    """
    Restaura un tipo de usuario eliminado lógicamente.
    """
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None:
            return
            
        cur = cnx.cursor()
        cur.callproc("sp_restaurar_tipo_usuario", [id_tipo])
        cnx.commit()
        
        if cur.rowcount > 0:
            print(f"✅ Tipo de usuario ID {id_tipo} restaurado correctamente.")
        else:
            print(f"⚠️  No se encontró el tipo de usuario ID {id_tipo} o ya estaba activo.")
            
    except mysql.connector.Error as e:
        print("❌ Error en sp_restaurar_tipo:", e)
        if cnx and cnx.is_connected():
            try: 
                cnx.rollback()
            except: 
                pass
    finally:
        if cur: 
            cur.close()
        if cnx and cnx.is_connected(): 
            cnx.close()

def sp_actualizar_tipo(id_tipo: int, nombre_tipo: str, descripcion: str, estado: str):
    """
    Actualiza un tipo de usuario existente.
    """
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None:
            return
            
        cur = cnx.cursor()
        cur.callproc("sp_actualizar_tipo_usuario", [id_tipo, nombre_tipo, descripcion, estado])
        cnx.commit()
        
        if cur.rowcount > 0:
            print(f"✅ Tipo de usuario ID {id_tipo} actualizado correctamente.")
        else:
            print(f"⚠️  No se pudo actualizar el tipo de usuario ID {id_tipo}. Verifica que exista y no esté eliminado.")
            
    except mysql.connector.Error as e:
        print("❌ Error en sp_actualizar_tipo:", e)
        if cnx and cnx.is_connected():
            try: 
                cnx.rollback()
            except: 
                pass
    finally:
        if cur: 
            cur.close()
        if cnx and cnx.is_connected(): 
            cnx.close()

def sp_buscar_por_id(id_tipo: int):
    """
    Busca un tipo de usuario por su ID.
    """
    cnx = cur = None
    try:
        cnx = conectar()
        if cnx is None:
            return
            
        cur = cnx.cursor()
        query = "SELECT id_tipo_usuario, nombre_tipo, descripcion, estado, created_at, updated_at, deleted FROM tipo_usuario WHERE id_tipo_usuario = %s"
        cur.execute(query, (id_tipo,))
        
        resultado = cur.fetchone()
        if resultado:
            id_tipo, nombre, descripcion, estado, created_at, updated_at, deleted = resultado
            estado_eliminado = "ELIMINADO" if deleted == 1 else "ACTIVO"
            print(f"\n=== DETALLE TIPO USUARIO ID {id_tipo} ===")
            print(f"Nombre: {nombre}")
            print(f"Descripción: {descripcion}")
            print(f"Estado: {estado}")
            print(f"Eliminado: {estado_eliminado}")
            print(f"Creado: {created_at}")
            print(f"Actualizado: {updated_at if updated_at else 'No actualizado'}")
        else:
            print(f"❌ No se encontró el tipo de usuario con ID {id_tipo}.")
            
    except mysql.connector.Error as e:
        print("❌ Error en sp_buscar_por_id:", e)
    finally:
        if cur: 
            cur.close()
        if cnx and cnx.is_connected(): 
            cnx.close()

# ---------------- MENÚ PRINCIPAL ----------------
def menu():
    """
    Menú interactivo para gestionar tipos de usuario.
    """
    while True:
        print("\n" + "="*50)
        print("      GESTIÓN DE TIPOS DE USUARIO")
        print("="*50)
        print("1) Insertar nuevo tipo de usuario")
        print("2) Listar tipos de usuario ACTIVOS")
        print("3) Listar todos los tipos de usuario")
        print("4) Buscar tipo de usuario por ID")
        print("5) Actualizar tipo de usuario")
        print("6) Borrado lógico por ID")
        print("7) Restaurar tipo de usuario eliminado")
        print("0) Salir")
        print("-"*50)

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\n--- INSERTAR NUEVO TIPO DE USUARIO ---")
            nombre = input("Nombre del tipo: ").strip()
            descripcion = input("Descripción: ").strip()
            estado = input("Estado (Activo/Inactivo) [Activo]: ").strip() or "Activo"
            sp_insertar_tipo_usuario(nombre, descripcion, estado)

        elif opcion == "2":
            sp_listar_tipos_activos()

        elif opcion == "3":
            sp_listar_todos_tipos()

        elif opcion == "4":
            try:
                id_tipo = int(input("ID a buscar: ").strip())
                sp_buscar_por_id(id_tipo)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "5":
            try:
                id_tipo = int(input("ID a actualizar: ").strip())
                nombre = input("Nuevo nombre: ").strip()
                descripcion = input("Nueva descripción: ").strip()
                estado = input("Nuevo estado (Activo/Inactivo): ").strip()
                sp_actualizar_tipo(id_tipo, nombre, descripcion, estado)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "6":
            try:
                id_tipo = int(input("ID para borrado lógico: ").strip())
                sp_borrado_logico_tipo(id_tipo)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "7":
            try:
                id_tipo = int(input("ID a restaurar: ").strip())
                sp_restaurar_tipo(id_tipo)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "0":
            print("👋 Saliendo del sistema de gestión...")
            break

        else:
            print("❌ Opción no válida. Intenta nuevamente.")

# Punto de entrada del programa
if __name__ == "__main__":
    # Verificar conexión al inicio
    conexion = conectar()
    if conexion:
        print("✅ Conexión a la base de datos establecida correctamente")
        conexion.close()
        menu()
    else:
        print("❌ No se pudo conectar a la base de datos. Verifica la configuración.")