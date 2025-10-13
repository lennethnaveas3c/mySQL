
-- usuario
-- Insertar usuario simple
DELIMITER //
CREATE PROCEDURE insertar_usuario(
    IN nombre_usuario VARCHAR(45),
    IN contrasena_usuario VARCHAR(100),
    IN correo_usuario VARCHAR(100),
    IN tipo_id INT
)
BEGIN
    INSERT INTO usuario (nombre, contrasena, correo, fecha_creacion, tipo_usuario_id_tipo_usuario)
    VALUES (nombre_usuario, contrasena_usuario, correo_usuario, CURDATE(), tipo_id);
END//
DELIMITER ;

-- Borrar usuario (solo marca como eliminado)
DELIMITER //
CREATE PROCEDURE borrar_usuario(IN id_usuario_borrar INT)
BEGIN
    UPDATE usuario SET deleted = 1 WHERE id_usuario = id_usuario_borrar;
END//
DELIMITER ;

-- Mostrar usuarios activos
DELIMITER //
CREATE PROCEDURE mostrar_usuarios_activos()
BEGIN
    SELECT * FROM usuario WHERE deleted = 0;
END//
DELIMITER ;

-- Mostrar todos los usuarios
DELIMITER //
CREATE PROCEDURE mostrar_todos_usuarios()
BEGIN
    SELECT * FROM usuario;
END//
DELIMITER ;


-- equipo
-- Insertar usuario simple
  

-- Borrar usuario (solo marca como eliminado)
DELIMITER //
CREATE PROCEDURE borrar_usuario(IN id_usuario_borrar INT)
BEGIN
    UPDATE usuario SET deleted = 1 WHERE id_usuario = id_usuario_borrar;
END//
DELIMITER ;
-- no funciona






-- Primero elimina el procedimiento si existe
DROP PROCEDURE IF EXISTS borrar_usuario;

-- Luego crea el nuevo
DELIMITER //
CREATE PROCEDURE borrar_usuario(IN id_usuario_borrar INT)
BEGIN
    UPDATE usuario SET deleted = 1 WHERE id_usuario = id_usuario_borrar;
END//
DELIMITER ;






-- mantenimiento
-- Insertar mantenimiento
DELIMITER //
CREATE PROCEDURE insertar_mantenimiento(
    IN fecha_mantenimiento DATE,
    IN descripcion_mantenimiento VARCHAR(200),
    IN usuario_id INT,
    IN equipo_id INT
)
BEGIN
    INSERT INTO mantenimiento (fecha_mantenimiento, descripcion_mantenimiento, usuario_id_usuario, equipo_id_equipo)
    VALUES (fecha_mantenimiento, descripcion_mantenimiento, usuario_id, equipo_id);
END//
DELIMITER ;

-- Completar mantenimiento
DELIMITER //
CREATE PROCEDURE completar_mantenimiento(IN id_mantenimiento_completar INT)
BEGIN
    UPDATE mantenimiento 
    SET estado_mantenimiento = 'Completado' 
    WHERE id_mantenimiento = id_mantenimiento_completar;
END//
DELIMITER ;

-- Mostrar mantenimientos pendientes
DELIMITER //
CREATE PROCEDURE mostrar_mantenimientos_pendientes()
BEGIN
    SELECT * FROM mantenimiento 
    WHERE estado_mantenimiento = 'Pendiente' 
    AND deleted = 0;
END//
DELIMITER ;


-- historial equipo
-- Insertar en historial
DELIMITER //
CREATE PROCEDURE insertar_historial(
    IN descripcion_accion VARCHAR(200),
    IN usuario_id INT,
    IN equipo_id INT
)
BEGIN
    INSERT INTO historial_equipo (fecha_accion, descripcion_accion, usuario_id_usuario, equipo_id_equipo)
    VALUES (CURDATE(), descripcion_accion, usuario_id, equipo_id);
END//
DELIMITER ;

-- Mostrar historial reciente
DELIMITER //
CREATE PROCEDURE mostrar_historial_reciente()
BEGIN
    SELECT * FROM historial_equipo 
    WHERE deleted = 0 
    ORDER BY fecha_accion DESC 
    LIMIT 10;
END//
DELIMITER ;

-- Mostrar historial por equipo
DELIMITER //
CREATE PROCEDURE mostrar_historial_equipo(IN id_equipo_buscar INT)
BEGIN
    SELECT * FROM historial_equipo 
    WHERE equipo_id_equipo = id_equipo_buscar 
    AND deleted = 0 
    ORDER BY fecha_accion DESC;
END//
DELIMITER ;


-- procedimientos para reportes simples
-- Contar equipos por sala
DELIMITER //
CREATE PROCEDURE contar_equipos_por_sala()
BEGIN
    SELECT u.nombre_ubicacion, COUNT(e.id_equipo) as total_equipos
    FROM ubicacion u
    LEFT JOIN equipo e ON u.id_ubicacion = e.ubicacion_id_ubicacion AND e.deleted = 0
    WHERE u.deleted = 0
    GROUP BY u.nombre_ubicacion;
END//
DELIMITER ;

-- Mostrar estado de salas
DELIMITER //
CREATE PROCEDURE mostrar_estado_salas()
BEGIN
    SELECT 
        u.nombre_ubicacion as sala,
        e.nombre as equipo,
        e.estado_equipo as estado
    FROM ubicacion u
    JOIN equipo e ON u.id_ubicacion = e.ubicacion_id_ubicacion
    WHERE e.deleted = 0
    ORDER BY u.nombre_ubicacion, e.nombre;
END//
DELIMITER ;

-- Buscar equipos por nombre
DELIMITER //
CREATE PROCEDURE buscar_equipo_por_nombre(IN nombre_buscar VARCHAR(45))
BEGIN
    SELECT * FROM equipo 
    WHERE nombre LIKE CONCAT('%', nombre_buscar, '%') 
    AND deleted = 0;
END//
DELIMITER ;



-- Primero ve qué tipos de usuario hay en tu base de datos
SELECT * FROM tipo_usuario;





-- ejemplos de usos sencillos
-- Insertar un usuario
CALL insertar_usuario('Pedro García', 'clave123', 'pedro@email.com', 2);

-- Ver usuarios activos
CALL mostrar_usuarios_activos();

-- Insertar un equipo
CALL insertar_equipo('PC-NUEVO-001', 1, 1);

-- Ver equipos de la sala 1
CALL mostrar_equipos_por_sala(1);

-- Registrar mantenimiento
CALL insertar_mantenimiento('2024-10-07', 'Limpieza general', 4, 1);

-- Ver mantenimientos pendientes
CALL mostrar_mantenimientos_pendientes();

-- Registrar en historial
CALL insertar_historial('Encendido de sala', 2, 1);

-- Ver historial reciente
CALL mostrar_historial_reciente();

-- Ver reporte de salas
CALL contar_equipos_por_sala(); 