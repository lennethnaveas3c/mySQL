-- Script de creación de base de datos - Proyecto de Gestión de Equipos
-- Autor: [Lenneth Naveas]
-- Fecha: 06/10/2025
-- Descripción: Creación de esquema, tablas y relaciones con restricciones y auditoría
-- -----------------------------------------------------

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Creación del esquema
-- -----------------------------------------------------
DROP DATABASE IF EXISTS `proyecto`;
CREATE DATABASE IF NOT EXISTS `proyecto` DEFAULT CHARACTER SET utf8;

CREATE DATABASE IF NOT EXISTS `proyecto` DEFAULT CHARACTER SET utf8mb4;
USE `proyecto`;

-- -----------------------------------------------------
-- Tabla: tipo_usuario
-- Contiene los diferentes tipos de usuarios del sistema (Administrador, Técnico, etc.)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tipo_usuario` (
  `id_tipo_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre_tipo` VARCHAR(45) NOT NULL,
  `descripcion` VARCHAR(100) NOT NULL,
  `estado` VARCHAR(20) NOT NULL DEFAULT 'Activo',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id_tipo_usuario`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla: usuario
-- Almacena la información de los usuarios registrados en el sistema
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `contrasena` VARCHAR(100) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  `fecha_creacion` DATE NOT NULL,
  `estado` VARCHAR(20) DEFAULT 'Activo',
  `tipo_usuario_id_tipo_usuario` INT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo_unico` (`correo`),
  CONSTRAINT `fk_usuario_tipo_usuario`
    FOREIGN KEY (`tipo_usuario_id_tipo_usuario`)
    REFERENCES `tipo_usuario` (`id_tipo_usuario`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla: ubicacion
-- Define los lugares físicos donde se encuentran los equipos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ubicacion` (
  `id_ubicacion` INT NOT NULL AUTO_INCREMENT,
  `nombre_ubicacion` VARCHAR(45) NOT NULL,
  `descripcion_ubicacion` VARCHAR(100),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id_ubicacion`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla: tipo_equipo
-- Contiene las categorías de los equipos (Computador, Impresora, Router, etc.)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tipo_equipo` (
  `id_tipo_equipo` INT NOT NULL AUTO_INCREMENT,
  `nombre_tipo_equipo` VARCHAR(45) NOT NULL,
  `descripcion_tipo_equipo` VARCHAR(100),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id_tipo_equipo`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla: equipo
-- Almacena los equipos registrados, con su tipo y ubicación
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `equipo` (
  `id_equipo` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `estado_equipo` VARCHAR(20) NOT NULL DEFAULT 'Operativo',
  `ubicacion_id_ubicacion` INT NOT NULL,
  `tipo_equipo_id_tipo_equipo` INT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id_equipo`),
  CONSTRAINT `fk_equipo_ubicacion`
    FOREIGN KEY (`ubicacion_id_ubicacion`)
    REFERENCES `ubicacion` (`id_ubicacion`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_equipo_tipo_equipo`
    FOREIGN KEY (`tipo_equipo_id_tipo_equipo`)
    REFERENCES `tipo_equipo` (`id_tipo_equipo`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla: mantenimiento
-- Registra las actividades de mantenimiento realizadas a los equipos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mantenimiento` (
  `id_mantenimiento` INT NOT NULL AUTO_INCREMENT,
  `fecha_mantenimiento` DATE NOT NULL,
  `estado_mantenimiento` VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
  `descripcion_mantenimiento` VARCHAR(200),
  `usuario_id_usuario` INT NOT NULL,
  `equipo_id_equipo` INT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id_mantenimiento`),
  CONSTRAINT `fk_mantenimiento_usuario`
    FOREIGN KEY (`usuario_id_usuario`)
    REFERENCES `usuario` (`id_usuario`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_mantenimiento_equipo`
    FOREIGN KEY (`equipo_id_equipo`)
    REFERENCES `equipo` (`id_equipo`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla: historial_equipo
-- Guarda el registro histórico de acciones realizadas sobre los equipos
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `historial_equipo` (
  `id_historial_equipo` INT NOT NULL AUTO_INCREMENT,
  `fecha_accion` DATE NOT NULL,
  `descripcion_accion` VARCHAR(200) NOT NULL,
  `usuario_id_usuario` INT NOT NULL,
  `equipo_id_equipo` INT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id_historial_equipo`),
  CONSTRAINT `fk_historial_equipo_usuario`
    FOREIGN KEY (`usuario_id_usuario`)
    REFERENCES `usuario` (`id_usuario`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_historial_equipo_equipo`
    FOREIGN KEY (`equipo_id_equipo`)
    REFERENCES `equipo` (`id_equipo`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Agregar índices para mejorar el rendimiento
-- -----------------------------------------------------
CREATE INDEX idx_usuario_correo ON usuario(correo);
CREATE INDEX idx_equipo_estado ON equipo(estado_equipo);
CREATE INDEX idx_mantenimiento_fecha ON mantenimiento(fecha_mantenimiento);
CREATE INDEX idx_historial_fecha ON historial_equipo(fecha_accion);

-- -----------------------------------------------------
-- Restaurar configuraciones originales
-- -----------------------------------------------------
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;






otra base de datos




-- 1) Crear base y usarla
CREATE DATABASE IF NOT EXISTS empresa;
USE empresa;

-- 2) Crear tabla si no existe (con estructura mínima)
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    cargo  VARCHAR(50) NOT NULL,
    sueldo DECIMAL(10,2) NOT NULL
);

-- 3) Asegurar columnas de auditoría y borrado lógico (MySQL 8.0.29+: IF NOT EXISTS)
ALTER TABLE empleados
  ADD COLUMN eliminado  TINYINT(1) NOT NULL DEFAULT 0 AFTER sueldo,
  ADD COLUMN created_at DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN updated_at DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  ADD COLUMN deleted_at DATETIME NULL DEFAULT NULL;

-- 4) Poblar datos de ejemplo SOLO si está vacía
INSERT INTO empleados (nombre, cargo, sueldo)
SELECT 'Juan Pérez', 'Administrador', 850000
WHERE NOT EXISTS (SELECT 1 FROM empleados LIMIT 1);
INSERT INTO empleados (nombre, cargo, sueldo)
SELECT 'Ana Gómez', 'Vendedora', 650000
WHERE NOT EXISTS (SELECT 1 FROM empleados LIMIT 1 OFFSET 1);
INSERT INTO empleados (nombre, cargo, sueldo)
SELECT 'Carlos Rojas', 'Técnico', 720000
WHERE NOT EXISTS (SELECT 1 FROM empleados LIMIT 1 OFFSET 2);

-- 5) Recrear procedimientos almacenados
DELIMITER $$

-- A) Listar SOLO activos
DROP PROCEDURE IF EXISTS sp_listar_empleados_activos $$
CREATE PROCEDURE sp_listar_empleados_activos()
BEGIN
    SELECT id, nombre, cargo, sueldo, created_at, updated_at
    FROM empleados
    WHERE eliminado = 0
    ORDER BY id;
END $$

-- B) Listar TODOS (incluye eliminados)
DROP PROCEDURE IF EXISTS sp_listar_empleados_todos $$
CREATE PROCEDURE sp_listar_empleados_todos()
BEGIN
    SELECT id, nombre, cargo, sueldo, eliminado, created_at, updated_at, deleted_at
    FROM empleados
    ORDER BY id;
END $$

-- C) Insertar y devolver ID nuevo (OUT)
DROP PROCEDURE IF EXISTS sp_insertar_empleado $$
CREATE PROCEDURE sp_insertar_empleado(
    IN  p_nombre VARCHAR(50),
    IN  p_cargo  VARCHAR(50),
    IN  p_sueldo DECIMAL(10,2),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO empleados (nombre, cargo, sueldo)
    VALUES (p_nombre, p_cargo, p_sueldo);

    SET p_nuevo_id = LAST_INSERT_ID();
END $$

-- D) Borrado lógico
DROP PROCEDURE IF EXISTS sp_borrado_logico_empleado $$
CREATE PROCEDURE sp_borrado_logico_empleado(IN p_id INT)
BEGIN
    UPDATE empleados
    SET eliminado = 1,
        deleted_at = NOW()
    WHERE id = p_id AND eliminado = 0;
END $$

-- E) Restaurar (opcional)
DROP PROCEDURE IF EXISTS sp_restaurar_empleado $$
CREATE PROCEDURE sp_restaurar_empleado(IN p_id INT)
BEGIN
    UPDATE empleados
    SET eliminado = 0,
        deleted_at = NULL
    WHERE id = p_id AND eliminado = 1;
END $$

DELIMITER ;





















DELIMITER $$

-- Procedimiento para insertar tipo de usuario
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


-- Procedimiento para listar tipos de usuario activos
CREATE PROCEDURE sp_listar_tipos_usuario_activos()
BEGIN
    SELECT id_tipo_usuario, nombre_tipo, descripcion, estado, created_at, updated_at
    FROM tipo_usuario
    WHERE deleted = 0;
END$$


-- Procedimiento para listar todos los tipos de usuario
CREATE PROCEDURE sp_listar_tipos_usuario_todos()
BEGIN
    SELECT id_tipo_usuario, nombre_tipo, descripcion, estado, created_at, updated_at, deleted
    FROM tipo_usuario;
END$$


-- Procedimiento para borrado lógico
CREATE PROCEDURE sp_borrado_logico_tipo_usuario(IN p_id INT)
BEGIN
    UPDATE tipo_usuario
    SET deleted = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_usuario = p_id AND deleted = 0;
END$$


-- Procedimiento para restaurar
CREATE PROCEDURE sp_restaurar_tipo_usuario(IN p_id INT)
BEGIN
    UPDATE tipo_usuario
    SET deleted = 0, updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_usuario = p_id AND deleted = 1;
END$$


-- Procedimiento para actualizar tipo de usuario
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












DELIMITER $$

CREATE PROCEDURE sp_borrado_logico_tipo_usuario(IN p_id INT)
BEGIN
    UPDATE tipo_usuario
    SET deleted = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_usuario = p_id AND deleted = 0;
END$$

DELIMITER ;


DROP PROCEDURE IF EXISTS sp_insertar_tipo_usuario;


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





-- Cambiamos el delimitador para procedimientos
DELIMITER $$

-- -----------------------------------------------------
-- Procedimiento para insertar tipo de usuario
-- -----------------------------------------------------
DROP PROCEDURE IF EXISTS sp_insertar_tipo_usuario$$
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

-- -----------------------------------------------------
-- Procedimiento para listar tipos de usuario activos
-- -----------------------------------------------------
DROP PROCEDURE IF EXISTS sp_listar_tipos_usuario_activos$$
CREATE PROCEDURE sp_listar_tipos_usuario_activos()
BEGIN
    SELECT id_tipo_usuario, nombre_tipo, descripcion, estado, created_at, updated_at
    FROM tipo_usuario
    WHERE deleted = 0;
END$$

-- -----------------------------------------------------
-- Procedimiento para listar todos los tipos de usuario
-- -----------------------------------------------------
DROP PROCEDURE IF EXISTS sp_listar_tipos_usuario_todos$$
CREATE PROCEDURE sp_listar_tipos_usuario_todos()
BEGIN
    SELECT id_tipo_usuario, nombre_tipo, descripcion, estado, created_at, updated_at, deleted
    FROM tipo_usuario;
END$$

-- -----------------------------------------------------
-- Procedimiento para borrado lógico
-- -----------------------------------------------------
DROP PROCEDURE IF EXISTS sp_borrado_logico_tipo_usuario$$
CREATE PROCEDURE sp_borrado_logico_tipo_usuario(IN p_id INT)
BEGIN
    UPDATE tipo_usuario
    SET deleted = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_usuario = p_id AND deleted = 0;
END$$

-- -----------------------------------------------------
-- Procedimiento para restaurar tipo de usuario
-- -----------------------------------------------------
DROP PROCEDURE IF EXISTS sp_restaurar_tipo_usuario$$
CREATE PROCEDURE sp_restaurar_tipo_usuario(IN p_id INT)
BEGIN
    UPDATE tipo_usuario
    SET deleted = 0, updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_usuario = p_id AND deleted = 1;
END$$

-- -----------------------------------------------------
-- Procedimiento para actualizar tipo de usuario
-- -----------------------------------------------------
DROP PROCEDURE IF EXISTS sp_actualizar_tipo_usuario$$
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

-- Restauramos el delimitador normal
DELIMITER ;












-- ==========================================
-- PROCEDIMIENTOS PARA TABLA USUARIO
-- ==========================================

DELIMITER $$

-- Insertar usuario
CREATE PROCEDURE sp_insertar_usuario(
    IN p_nombre VARCHAR(45),
    IN p_correo VARCHAR(100),
    IN p_contrasena VARCHAR(100),
    IN p_tipo_usuario_id INT,
    IN p_estado VARCHAR(20),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO usuario (nombre, correo, contrasena, tipo_usuario_id_tipo_usuario, estado)
    VALUES (p_nombre, p_correo, p_contrasena, p_tipo_usuario_id, p_estado);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$

-- Listar usuarios activos
CREATE PROCEDURE sp_listar_usuarios_activos()
BEGIN
    SELECT id_usuario, nombre, correo, tipo_usuario_id_tipo_usuario, estado, created_at
    FROM usuario
    WHERE deleted = 0;
END$$

-- Listar todos los usuarios
CREATE PROCEDURE sp_listar_usuarios_todos()
BEGIN
    SELECT id_usuario, nombre, correo, tipo_usuario_id_tipo_usuario, estado, created_at, deleted
    FROM usuario;
END$$

-- Borrado lógico
CREATE PROCEDURE sp_borrado_logico_usuario(IN p_id INT)
BEGIN
    UPDATE usuario
    SET deleted = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id_usuario = p_id AND deleted = 0;
END$$

-- Restaurar usuario eliminado
CREATE PROCEDURE sp_restaurar_usuario(IN p_id INT)
BEGIN
    UPDATE usuario
    SET deleted = 0, updated_at = CURRENT_TIMESTAMP
    WHERE id_usuario = p_id AND deleted = 1;
END$$

-- Actualizar usuario
CREATE PROCEDURE sp_actualizar_usuario(
    IN p_id INT,
    IN p_nombre VARCHAR(45),
    IN p_correo VARCHAR(100),
    IN p_contrasena VARCHAR(100),
    IN p_tipo_usuario_id INT,
    IN p_estado VARCHAR(20)
)
BEGIN
    UPDATE usuario
    SET nombre = p_nombre,
        correo = p_correo,
        contrasena = p_contrasena,
        tipo_usuario_id_tipo_usuario = p_tipo_usuario_id,
        estado = p_estado,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_usuario = p_id AND deleted = 0;
END$$

DELIMITER ;






DELIMITER $$
CREATE PROCEDURE sp_insertar_ubicacion(
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO ubicacion(nombre_ubicacion, descripcion_ubicacion)
    VALUES (p_nombre, p_descripcion);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$
DELIMITER ;





DELIMITER $$
CREATE PROCEDURE sp_listar_ubicaciones_activas()
BEGIN
    SELECT id_ubicacion, nombre_ubicacion, descripcion_ubicacion, created_at, updated_at
    FROM ubicacion
    WHERE deleted = 0;
END$$
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE sp_listar_ubicaciones_todas()
BEGIN
    SELECT id_ubicacion, nombre_ubicacion, descripcion_ubicacion, created_at, updated_at, deleted
    FROM ubicacion;
END$$
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE sp_actualizar_ubicacion(
    IN p_id INT,
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100)
)
BEGIN
    UPDATE ubicacion
    SET nombre_ubicacion = p_nombre,
        descripcion_ubicacion = p_descripcion,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_ubicacion = p_id;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_borrado_logico_ubicacion(IN p_id INT)
BEGIN
    UPDATE ubicacion
    SET deleted = 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_ubicacion = p_id;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_restaurar_ubicacion(IN p_id INT)
BEGIN
    UPDATE ubicacion
    SET deleted = 0,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_ubicacion = p_id;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE sp_insertar_ubicacion(
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO ubicacion(nombre_ubicacion, descripcion_ubicacion)
    VALUES (p_nombre, p_descripcion);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$
DELIMITER ;




DELIMITER $$

DROP PROCEDURE IF EXISTS sp_insertar_ubicacion$$

CREATE PROCEDURE sp_insertar_ubicacion(
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100)
)
BEGIN
    INSERT INTO ubicacion(nombre_ubicacion, descripcion_ubicacion)
    VALUES (p_nombre, p_descripcion);
END$$

DELIMITER ;















DELIMITER $$
CREATE PROCEDURE sp_insertar_ubicacion(
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO ubicacion(nombre_ubicacion, descripcion_ubicacion)
    VALUES (p_nombre, p_descripcion);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$
DELIMITER ;










DROP PROCEDURE IF EXISTS sp_insertar_ubicacion;
DELIMITER $$
CREATE PROCEDURE sp_insertar_ubicacion(
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO ubicacion (nombre_ubicacion, descripcion_ubicacion)
    VALUES (p_nombre, p_descripcion);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$
DELIMITER ;














-- DROP PROCEDURES si ya existen
DROP PROCEDURE IF EXISTS sp_insertar_tipo_equipo;
DROP PROCEDURE IF EXISTS sp_listar_tipos_equipo_activas;
DROP PROCEDURE IF EXISTS sp_listar_tipos_equipo_todas;
DROP PROCEDURE IF EXISTS sp_actualizar_tipo_equipo;
DROP PROCEDURE IF EXISTS sp_borrado_logico_tipo_equipo;
DROP PROCEDURE IF EXISTS sp_restaurar_tipo_equipo;

DELIMITER $$

-- Insertar tipo_equipo
CREATE PROCEDURE sp_insertar_tipo_equipo(
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100),
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO tipo_equipo(nombre_tipo_equipo, descripcion_tipo_equipo)
    VALUES (p_nombre, p_descripcion);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$

-- Listar activas
CREATE PROCEDURE sp_listar_tipos_equipo_activas()
BEGIN
    SELECT id_tipo_equipo, nombre_tipo_equipo, descripcion_tipo_equipo, created_at, updated_at
    FROM tipo_equipo
    WHERE deleted = 0;
END$$

-- Listar todas
CREATE PROCEDURE sp_listar_tipos_equipo_todas()
BEGIN
    SELECT id_tipo_equipo, nombre_tipo_equipo, descripcion_tipo_equipo, created_at, updated_at, deleted
    FROM tipo_equipo;
END$$

-- Actualizar tipo_equipo
CREATE PROCEDURE sp_actualizar_tipo_equipo(
    IN p_id INT,
    IN p_nombre VARCHAR(45),
    IN p_descripcion VARCHAR(100)
)
BEGIN
    UPDATE tipo_equipo
    SET nombre_tipo_equipo = p_nombre,
        descripcion_tipo_equipo = p_descripcion,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_equipo = p_id;
END$$

-- Borrado lógico
CREATE PROCEDURE sp_borrado_logico_tipo_equipo(IN p_id INT)
BEGIN
    UPDATE tipo_equipo
    SET deleted = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_equipo = p_id;
END$$

-- Restaurar
CREATE PROCEDURE sp_restaurar_tipo_equipo(IN p_id INT)
BEGIN
    UPDATE tipo_equipo
    SET deleted = 0, updated_at = CURRENT_TIMESTAMP
    WHERE id_tipo_equipo = p_id;
END$$

DELIMITER ;

















-- INSERTAR EQUIPO
DROP PROCEDURE IF EXISTS sp_insertar_equipo;
DELIMITER $$
CREATE PROCEDURE sp_insertar_equipo(
    IN p_nombre VARCHAR(45),
    IN p_estado VARCHAR(20),
    IN p_ubicacion_id INT,
    IN p_tipo_equipo_id INT,
    OUT p_nuevo_id INT
)
BEGIN
    INSERT INTO equipo (nombre, estado_equipo, ubicacion_id_ubicacion, tipo_equipo_id_tipo_equipo)
    VALUES (p_nombre, p_estado, p_ubicacion_id, p_tipo_equipo_id);
    SET p_nuevo_id = LAST_INSERT_ID();
END$$
DELIMITER ;

-- LISTAR EQUIPOS ACTIVOS
DROP PROCEDURE IF EXISTS sp_listar_equipos_activas;
DELIMITER $$
CREATE PROCEDURE sp_listar_equipos_activas()
BEGIN
    SELECT e.id_equipo, e.nombre, e.estado_equipo, u.nombre_ubicacion, t.nombre_tipo_equipo, e.created_at, e.updated_at
    FROM equipo e
    JOIN ubicacion u ON e.ubicacion_id_ubicacion = u.id_ubicacion
    JOIN tipo_equipo t ON e.tipo_equipo_id_tipo_equipo = t.id_tipo_equipo
    WHERE e.deleted = 0;
END$$
DELIMITER ;

-- LISTAR TODOS LOS EQUIPOS
DROP PROCEDURE IF EXISTS sp_listar_equipos_todos;
DELIMITER $$
CREATE PROCEDURE sp_listar_equipos_todos()
BEGIN
    SELECT e.id_equipo, e.nombre, e.estado_equipo, u.nombre_ubicacion, t.nombre_tipo_equipo, e.created_at, e.updated_at, e.deleted
    FROM equipo e
    JOIN ubicacion u ON e.ubicacion_id_ubicacion = u.id_ubicacion
    JOIN tipo_equipo t ON e.tipo_equipo_id_tipo_equipo = t.id_tipo_equipo;
END$$
DELIMITER ;

-- ACTUALIZAR EQUIPO
DROP PROCEDURE IF EXISTS sp_actualizar_equipo;
DELIMITER $$
CREATE PROCEDURE sp_actualizar_equipo(
    IN p_id INT,
    IN p_nombre VARCHAR(45),
    IN p_estado VARCHAR(20),
    IN p_ubicacion_id INT,
    IN p_tipo_equipo_id INT
)
BEGIN
    UPDATE equipo
    SET nombre = p_nombre,
        estado_equipo = p_estado,
        ubicacion_id_ubicacion = p_ubicacion_id,
        tipo_equipo_id_tipo_equipo = p_tipo_equipo_id,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_equipo = p_id;
END$$
DELIMITER ;

-- BORRADO LÓGICO EQUIPO
DROP PROCEDURE IF EXISTS sp_borrado_logico_equipo;
DELIMITER $$
CREATE PROCEDURE sp_borrado_logico_equipo(IN p_id INT)
BEGIN
    UPDATE equipo SET deleted = 1, updated_at = CURRENT_TIMESTAMP WHERE id_equipo = p_id;
END$$
DELIMITER ;

-- RESTAURAR EQUIPO
DROP PROCEDURE IF EXISTS sp_restaurar_equipo;
DELIMITER $$
CREATE PROCEDURE sp_restaurar_equipo(IN p_id INT)
BEGIN
    UPDATE equipo SET deleted = 0, updated_at = CURRENT_TIMESTAMP WHERE id_equipo = p_id;
END$$
DELIMITER ;
















DELIMITER $$

CREATE PROCEDURE sp_listar_mantenimientos_activos()
BEGIN
    SELECT m.id_mantenimiento, m.fecha_mantenimiento, m.estado_mantenimiento, 
           m.descripcion_mantenimiento, u.nombre_usuario, e.nombre AS nombre_equipo, 
           m.created_at, m.updated_at
    FROM mantenimiento m
    JOIN usuario u ON m.usuario_id_usuario = u.id_usuario
    JOIN equipo e ON m.equipo_id_equipo = e.id_equipo
    WHERE m.deleted = 0;
END$$

DELIMITER ;










DELIMITER $$

CREATE PROCEDURE sp_listar_mantenimientos_activos()
BEGIN
    SELECT m.id_mantenimiento, m.fecha_mantenimiento, m.estado_mantenimiento, 
           m.descripcion_mantenimiento, u.nombre, e.nombre AS nombre_equipo, 
           m.created_at, m.updated_at
    FROM mantenimiento m
    JOIN usuario u ON m.usuario_id_usuario = u.id_usuario
    JOIN equipo e ON m.equipo_id_equipo = e.id_equipo
    WHERE m.deleted = 0;
END$$

DELIMITER ;





DROP PROCEDURE IF EXISTS sp_listar_mantenimientos_activos;

DELIMITER $$

CREATE PROCEDURE sp_listar_mantenimientos_activos()
BEGIN
    SELECT m.id_mantenimiento, m.fecha_mantenimiento, m.estado_mantenimiento, 
           m.descripcion_mantenimiento, u.nombre, e.nombre AS nombre_equipo, 
           m.created_at, m.updated_at
    FROM mantenimiento m
    JOIN usuario u ON m.usuario_id_usuario = u.id_usuario
    JOIN equipo e ON m.equipo_id_equipo = e.id_equipo
    WHERE m.deleted = 0;
END$$

DELIMITER ;
















-- -----------------------------------------------------
-- SP: Insertar mantenimiento
DROP PROCEDURE IF EXISTS sp_insertar_mantenimiento;
DELIMITER $$
CREATE PROCEDURE sp_insertar_mantenimiento(
    IN p_fecha DATE,
    IN p_estado VARCHAR(20),
    IN p_descripcion VARCHAR(200),
    IN p_usuario_id INT,
    IN p_equipo_id INT,
    OUT p_nuevo_id INT
)
BEGIN
    -- Validar usuario
    IF NOT EXISTS (SELECT 1 FROM usuario WHERE id_usuario = p_usuario_id AND deleted = 0) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe usuario con ese ID';
    END IF;

    -- Validar equipo
    IF NOT EXISTS (SELECT 1 FROM equipo WHERE id_equipo = p_equipo_id AND deleted = 0) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe equipo con ese ID';
    END IF;

    INSERT INTO mantenimiento(
        fecha_mantenimiento, estado_mantenimiento, descripcion_mantenimiento, usuario_id_usuario, equipo_id_equipo
    ) VALUES (p_fecha, p_estado, p_descripcion, p_usuario_id, p_equipo_id);

    SET p_nuevo_id = LAST_INSERT_ID();
END$$
DELIMITER ;

-- -----------------------------------------------------
-- SP: Listar mantenimientos activos
DROP PROCEDURE IF EXISTS sp_listar_mantenimientos_activos;
DELIMITER $$
CREATE PROCEDURE sp_listar_mantenimientos_activos()
BEGIN
    SELECT m.id_mantenimiento, m.fecha_mantenimiento, m.estado_mantenimiento, 
           m.descripcion_mantenimiento, u.nombre AS usuario, e.nombre AS equipo, 
           m.created_at, m.updated_at
    FROM mantenimiento m
    JOIN usuario u ON m.usuario_id_usuario = u.id_usuario
    JOIN equipo e ON m.equipo_id_equipo = e.id_equipo
    WHERE m.deleted = 0;
END$$
DELIMITER ;

-- -----------------------------------------------------
-- SP: Listar todos los mantenimientos
DROP PROCEDURE IF EXISTS sp_listar_mantenimientos_todos;
DELIMITER $$
CREATE PROCEDURE sp_listar_mantenimientos_todos()
BEGIN
    SELECT m.id_mantenimiento, m.fecha_mantenimiento, m.estado_mantenimiento, 
           m.descripcion_mantenimiento, u.nombre AS usuario, e.nombre AS equipo, 
           m.created_at, m.updated_at, m.deleted
    FROM mantenimiento m
    JOIN usuario u ON m.usuario_id_usuario = u.id_usuario
    JOIN equipo e ON m.equipo_id_equipo = e.id_equipo;
END$$
DELIMITER ;

-- -----------------------------------------------------
-- SP: Borrado lógico
DROP PROCEDURE IF EXISTS sp_borrado_logico_mantenimiento;
DELIMITER $$
CREATE PROCEDURE sp_borrado_logico_mantenimiento(IN p_id INT)
BEGIN
    UPDATE mantenimiento SET deleted = 1 WHERE id_mantenimiento = p_id;
END$$
DELIMITER ;

-- -----------------------------------------------------
-- SP: Restaurar mantenimiento
DROP PROCEDURE IF EXISTS sp_restaurar_mantenimiento;
DELIMITER $$
CREATE PROCEDURE sp_restaurar_mantenimiento(IN p_id INT)
BEGIN
    UPDATE mantenimiento SET deleted = 0 WHERE id_mantenimiento = p_id;
END$$
DELIMITER ;










-- DROP PROCEDURES EXISTENTES
DROP PROCEDURE IF EXISTS sp_insertar_historial_equipo;
DROP PROCEDURE IF EXISTS sp_listar_historial_activos;
DROP PROCEDURE IF EXISTS sp_listar_historial_todos;
DROP PROCEDURE IF EXISTS sp_actualizar_historial;
DROP PROCEDURE IF EXISTS sp_borrado_logico_historial;
DROP PROCEDURE IF EXISTS sp_restaurar_historial;










# ehhhhhhhhh lo guardo en caso de
DROP PROCEDURE IF EXISTS sp_insertar_historial_equipo;

DELIMITER //
CREATE PROCEDURE sp_insertar_historial_equipo(
    IN p_fecha DATE,
    IN p_descripcion VARCHAR(200),
    IN p_usuario_id INT,
    IN p_equipo_id INT,
    OUT p_nuevo_id INT
)
BEGIN
    -- Validar usuario
    IF NOT EXISTS (SELECT 1 FROM usuario WHERE id_usuario = p_usuario_id) THEN
        SET p_nuevo_id = -1;
    -- Validar equipo
    ELSEIF NOT EXISTS (SELECT 1 FROM equipo WHERE id_equipo = p_equipo_id) THEN
        SET p_nuevo_id = -2;
    ELSE
        INSERT INTO historial_equipo(fecha_accion, descripcion_accion, usuario_id_usuario, equipo_id_equipo)
        VALUES (p_fecha, p_descripcion, p_usuario_id, p_equipo_id);
        SET p_nuevo_id = LAST_INSERT_ID();
    END IF;
END //
DELIMITER ;















# este si funciono
USE proyecto;
DROP PROCEDURE IF EXISTS sp_insertar_historial_equipo;
DELIMITER //
CREATE PROCEDURE sp_insertar_historial_equipo(
    IN p_fecha DATE,
    IN p_descripcion VARCHAR(200),
    IN p_usuario_id INT,
    IN p_equipo_id INT,
    OUT p_nuevo_id INT
)
BEGIN
    -- Validar usuario
    IF NOT EXISTS (SELECT 1 FROM usuario WHERE id_usuario = p_usuario_id) THEN
        SET p_nuevo_id = -1;
    -- Validar equipo
    ELSEIF NOT EXISTS (SELECT 1 FROM equipo WHERE id_equipo = p_equipo_id) THEN
        SET p_nuevo_id = -2;
    ELSE
        INSERT INTO historial_equipo(fecha_accion, descripcion_accion, usuario_id_usuario, equipo_id_equipo)
        VALUES (p_fecha, p_descripcion, p_usuario_id, p_equipo_id);
        SET p_nuevo_id = LAST_INSERT_ID();
    END IF;
END//
DELIMITER ;
