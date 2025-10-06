-- -----------------------------------------------------
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

CREATE DATABASE IF NOT EXISTS `proyecto` DEFAULT CHARACTER SET utf8;
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
