-- -----------------------------------------------------
-- INSERCIONES DE DATOS ESPECÍFICOS PARA GESTIÓN DE SALAS
-- -----------------------------------------------------

-- Insertar tipos de usuario específicos para salas
INSERT INTO `tipo_usuario` (`nombre_tipo`, `descripcion`) VALUES
('Administrador', 'Control total del sistema y reportes'),
('Docente', 'Usuario que manipula el estado de la sala'),
('Funcionario', 'Usuario que gestiona dispositivos en sala'),
('Técnico', 'Encargado de mantenimiento de equipos');

-- Insertar ubicaciones (salas específicas)
INSERT INTO `ubicacion` (`nombre_ubicacion`, `descripcion_ubicacion`) VALUES
('Sala A-101', 'Sala de computación principal - Piso 1'),
('Sala A-102', 'Sala de multimedia - Piso 1'),
('Sala B-201', 'Laboratorio de redes - Piso 2'),
('Sala B-202', 'Sala de desarrollo - Piso 2'),
('Sala C-301', 'Aula magna - Piso 3');

-- Insertar tipos de equipo para salas
INSERT INTO `tipo_equipo` (`nombre_tipo_equipo`, `descripcion_tipo_equipo`) VALUES
('Computadora', 'Equipo de escritorio para estudiantes'),
('Servidor', 'Servidor de aplicaciones de la sala'),
('Proyector', 'Equipo de proyección multimedia'),
('Switch', 'Dispositivo de red para conexiones'),
('Aire Acondicionado', 'Control climático de la sala'),
('UPS', 'Sistema de energía ininterrumpida'),
('Computadora Docente', 'Equipo principal del docente');


-- dice que esta mal
-- Insertar usuarios según roles
INSERT INTO `usuario` (`nombre`, `contrasena`, `correo`, `fecha_creacion`, `tipo_usuario_id_tipo_usuario`) VALUES
('Admin Principal', 'admin123', 'admin@institucion.edu', '2024-01-10', 1),
('Prof. María González', 'docente456', 'maria.gonzalez@institucion.edu', '2024-01-15', 2),
('Func. Carlos Ruiz', 'func789', 'carlos.ruiz@institucion.edu', '2024-01-20', 3),
('Técnico Roberto Silva', 'tec012', 'roberto.silva@institucion.edu', '2024-01-25', 4),
('Prof. Ana López', 'docente345', 'ana.lopez@institucion.edu', '2024-02-01', 2);

-- Insertar equipos por sala
INSERT INTO `equipo` (`nombre`, `estado_equipo`, `ubicacion_id_ubicacion`, `tipo_equipo_id_tipo_equipo`) VALUES
-- Sala A-101
('PC-EST-001', 'Operativo', 1, 1),
('PC-EST-002', 'Operativo', 1, 1),
('PC-DOC-101', 'Operativo', 1, 7),
('PROY-101', 'En reparación', 1, 3),
('AC-101', 'Operativo', 1, 5),
('UPS-101', 'Operativo', 1, 6),

-- Sala A-102
('PC-EST-101', 'Operativo', 2, 1),
('PC-EST-102', 'Fuera de servicio', 2, 1),
('PROY-102', 'Operativo', 2, 3),
('SW-102', 'Operativo', 2, 4),

-- Sala B-201
('SRV-RED-201', 'Operativo', 3, 2),
('SW-CORE-201', 'Operativo', 3, 4),
('PC-EST-201', 'Operativo', 3, 1),

-- Sala B-202
('PC-DEV-202', 'Operativo', 4, 1),
('PROY-202', 'Operativo', 4, 3);

-- Insertar mantenimientos
INSERT INTO `mantenimiento` (`fecha_mantenimiento`, `estado_mantenimiento`, `descripcion_mantenimiento`, `usuario_id_usuario`, `equipo_id_equipo`) VALUES
('2024-10-01', 'Completado', 'Limpieza general y actualización de software', 4, 1),
('2024-10-05', 'Pendiente', 'Reparación de lámpara del proyector', 4, 4),
('2024-10-10', 'Completado', 'Reemplazo de fuente de poder', 4, 8),
('2024-10-15', 'Pendiente', 'Mantenimiento preventivo aire acondicionado', 4, 5),
('2024-10-20', 'Completado', 'Actualización de firmware del switch', 4, 10);

-- Insertar historial de estados de sala (encendido/apagado)
INSERT INTO `historial_equipo` (`fecha_accion`, `descripcion_accion`, `usuario_id_usuario`, `equipo_id_equipo`) VALUES
-- Historial Sala A-101
('2024-10-01 08:00:00', 'Encendido completo de sala - Inicio de clases', 2, 1),
('2024-10-01 12:00:00', 'Apagado de sala - Fin de jornada matutina', 2, 1),
('2024-10-01 14:00:00', 'Encendido de sala - Inicio jornada vespertina', 2, 1),
('2024-10-01 18:00:00', 'Apagado de sala - Fin de actividades', 2, 1),

-- Historial Sala A-102
('2024-10-02 08:30:00', 'Encendido parcial - Solo proyector', 5, 9),
('2024-10-02 10:00:00', 'Encendido completo - Actividad grupal', 5, 9),
('2024-10-02 16:00:00', 'Apagado de sala', 5, 9),

-- Actividades de mantenimiento
('2024-10-03 09:00:00', 'Agregado nuevo computador a la sala', 3, 2),
('2024-10-04 11:00:00', 'Retirado equipo para reparación', 3, 8),
('2024-10-05 15:30:00', 'Instalación nuevo software educativo', 4, 1);




-- Verifica qué hay en cada tabla
SELECT '=== VERIFICANDO DATOS EXISTENTES ===' as info;
SELECT * FROM tipo_usuario;
SELECT * FROM ubicacion;
SELECT * FROM tipo_equipo;

-- usuario y equipo estan vacios
SELECT * FROM usuario;
SELECT * FROM equipo;



-- Verifica qué hay en CADA tabla (no solo usuario y equipo)
SELECT '=== VERIFICANDO TABLAS PADRE ===' as info;

SELECT 'tipo_usuario:' as tabla, COUNT(*) as cantidad FROM tipo_usuario
UNION ALL
SELECT 'ubicacion:' as tabla, COUNT(*) as cantidad FROM ubicacion
UNION ALL
SELECT 'tipo_equipo:' as tabla, COUNT(*) as cantidad FROM tipo_equipo
UNION ALL
SELECT 'usuario:' as tabla, COUNT(*) as cantidad FROM usuario
UNION ALL
SELECT 'equipo:' as tabla, COUNT(*) as cantidad FROM equipo;











-- Si quieres empezar desde cero, elimina todos los datos
DELETE FROM historial_equipo;
DELETE FROM mantenimiento;
DELETE FROM equipo;
DELETE FROM usuario;
DELETE FROM tipo_equipo;
DELETE FROM ubicacion;
DELETE FROM tipo_usuario;

-- Reiniciar los auto_increment
ALTER TABLE tipo_usuario AUTO_INCREMENT = 1;
ALTER TABLE ubicacion AUTO_INCREMENT = 1;
ALTER TABLE tipo_equipo AUTO_INCREMENT = 1;
ALTER TABLE usuario AUTO_INCREMENT = 1;
ALTER TABLE equipo AUTO_INCREMENT = 1;
ALTER TABLE mantenimiento AUTO_INCREMENT = 1;
ALTER TABLE historial_equipo AUTO_INCREMENT = 1;


-- -----------------------------------------------------
-- CONSULTAS DE VERIFICACIÓN Y REPORTES
-- -----------------------------------------------------

-- 1. Verificar todos los registros
SELECT '=== TODOS LOS REGISTROS ===' as info;
SELECT * FROM tipo_usuario;
SELECT * FROM usuario;
SELECT * FROM ubicacion;
SELECT * FROM tipo_equipo;
SELECT * FROM equipo;
SELECT * FROM mantenimiento;
SELECT * FROM historial_equipo;

-- 2. Mostrar solo registros activos (no eliminados)
SELECT '=== REGISTROS ACTIVOS ===' as info;
SELECT * FROM tipo_usuario WHERE deleted = 0;
SELECT * FROM usuario WHERE deleted = 0;
SELECT * FROM ubicacion WHERE deleted = 0;
SELECT * FROM tipo_equipo WHERE deleted = 0;
SELECT * FROM equipo WHERE deleted = 0;
SELECT * FROM mantenimiento WHERE deleted = 0;
SELECT * FROM historial_equipo WHERE deleted = 0;

-- 3. Consulta: Estado actual de las salas
SELECT '=== ESTADO ACTUAL DE SALAS ===' as info;
SELECT 
    u.nombre_ubicacion as sala,
    COUNT(e.id_equipo) as total_equipos,
    SUM(CASE WHEN e.estado_equipo = 'Operativo' THEN 1 ELSE 0 END) as equipos_operativos,
    SUM(CASE WHEN e.estado_equipo = 'En reparación' THEN 1 ELSE 0 END) as en_reparacion,
    SUM(CASE WHEN e.estado_equipo = 'Fuera de servicio' THEN 1 ELSE 0 END) as fuera_servicio
FROM ubicacion u
LEFT JOIN equipo e ON u.id_ubicacion = e.ubicacion_id_ubicacion AND e.deleted = 0
WHERE u.deleted = 0
GROUP BY u.id_ubicacion, u.nombre_ubicacion;

-- 4. Consulta: Historial de encendido/apagado por sala (últimos 7 días)
SELECT '=== HISTORIAL ENCENDIDO/APAGADO ===' as info;
SELECT 
    u.nombre_ubicacion as sala,
    he.fecha_accion,
    he.descripcion_accion,
    us.nombre as usuario
FROM historial_equipo he
INNER JOIN equipo e ON he.equipo_id_equipo = e.id_equipo
INNER JOIN ubicacion u ON e.ubicacion_id_ubicacion = u.id_ubicacion
INNER JOIN usuario us ON he.usuario_id_usuario = us.id_usuario
WHERE he.descripcion_accion LIKE '%Encendido%' OR he.descripcion_accion LIKE '%Apagado%'
AND he.fecha_accion >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
AND he.deleted = 0
ORDER BY he.fecha_accion DESC;

-- 5. Consulta: Reporte mensual de actividad por sala
SELECT '=== REPORTE MENSUAL DE ACTIVIDAD ===' as info;
SELECT 
    u.nombre_ubicacion as sala,
    DATE(he.fecha_accion) as fecha,
    COUNT(*) as total_acciones,
    SUM(CASE WHEN he.descripcion_accion LIKE '%Encendido%' THEN 1 ELSE 0 END) as encendidos,
    SUM(CASE WHEN he.descripcion_accion LIKE '%Apagado%' THEN 1 ELSE 0 END) as apagados,
    SUM(CASE WHEN he.descripcion_accion LIKE '%Agregado%' THEN 1 ELSE 0 END) as equipos_agregados,
    SUM(CASE WHEN he.descripcion_accion LIKE '%Retirado%' THEN 1 ELSE 0 END) as equipos_retirados
FROM historial_equipo he
INNER JOIN equipo e ON he.equipo_id_equipo = e.id_equipo
INNER JOIN ubicacion u ON e.ubicacion_id_ubicacion = u.id_ubicacion
WHERE MONTH(he.fecha_accion) = MONTH(CURDATE())
AND YEAR(he.fecha_accion) = YEAR(CURDATE())
AND he.deleted = 0
GROUP BY u.nombre_ubicacion, DATE(he.fecha_accion)
ORDER BY fecha DESC, sala;

-- 6. Consulta: Mantenimientos pendientes por sala
SELECT '=== MANTENIMIENTOS PENDIENTES ===' as info;
SELECT 
    u.nombre_ubicacion as sala,
    e.nombre as equipo,
    te.nombre_tipo_equipo as tipo,
    m.fecha_mantenimiento,
    m.descripcion_mantenimiento,
    us.nombre as tecnico_asignado
FROM mantenimiento m
INNER JOIN equipo e ON m.equipo_id_equipo = e.id_equipo
INNER JOIN ubicacion u ON e.ubicacion_id_ubicacion = u.id_ubicacion
INNER JOIN tipo_equipo te ON e.tipo_equipo_id_tipo_equipo = te.id_tipo_equipo
INNER JOIN usuario us ON m.usuario_id_usuario = us.id_usuario
WHERE m.estado_mantenimiento = 'Pendiente'
AND m.deleted = 0
ORDER BY m.fecha_mantenimiento;

-- 7. Consulta: Dispositivos por tipo en cada sala
SELECT '=== INVENTARIO POR SALA ===' as info;
SELECT 
    u.nombre_ubicacion as sala,
    te.nombre_tipo_equipo as tipo_equipo,
    COUNT(e.id_equipo) as cantidad,
    GROUP_CONCAT(e.nombre SEPARATOR ', ') as equipos
FROM equipo e
INNER JOIN ubicacion u ON e.ubicacion_id_ubicacion = u.id_ubicacion
INNER JOIN tipo_equipo te ON e.tipo_equipo_id_tipo_equipo = te.id_tipo_equipo
WHERE e.deleted = 0
GROUP BY u.nombre_ubicacion, te.nombre_tipo_equipo
ORDER BY u.nombre_ubicacion, te.nombre_tipo_equipo;

-- 8. Consulta: Validación de relaciones - Usuarios por tipo
SELECT '=== USUARIOS POR TIPO ===' as info;
SELECT 
    tu.nombre_tipo as tipo_usuario,
    COUNT(u.id_usuario) as cantidad_usuarios,
    GROUP_CONCAT(u.nombre SEPARATOR ', ') as usuarios
FROM usuario u
INNER JOIN tipo_usuario tu ON u.tipo_usuario_id_tipo_usuario = tu.id_tipo_usuario
WHERE u.deleted = 0
GROUP BY tu.nombre_tipo;

-- 9. Consulta: Actividad por usuario (para control de 1 usuario por sala)
SELECT '=== ACTIVIDAD POR USUARIO ===' as info;
SELECT 
    u.nombre as usuario,
    tu.nombre_tipo as tipo,
    COUNT(he.id_historial_equipo) as total_acciones,
    MAX(he.fecha_accion) as ultima_accion
FROM usuario u
INNER JOIN tipo_usuario tu ON u.tipo_usuario_id_tipo_usuario = tu.id_tipo_usuario
LEFT JOIN historial_equipo he ON u.id_usuario = he.usuario_id_usuario
WHERE u.deleted = 0
AND he.deleted = 0
GROUP BY u.id_usuario, u.nombre, tu.nombre_tipo
ORDER BY total_acciones DESC;

-- 10. Consulta: Equipos que necesitan atención
SELECT '=== EQUIPOS QUE NECESITAN ATENCIÓN ===' as info;
SELECT 
    e.nombre as equipo,
    e.estado_equipo,
    te.nombre_tipo_equipo as tipo,
    u.nombre_ubicacion as sala,
    (SELECT descripcion_mantenimiento 
     FROM mantenimiento 
     WHERE equipo_id_equipo = e.id_equipo 
     AND estado_mantenimiento = 'Pendiente'
     AND deleted = 0
     LIMIT 1) as mantenimiento_pendiente
FROM equipo e
INNER JOIN tipo_equipo te ON e.tipo_equipo_id_tipo_equipo = te.id_tipo_equipo
INNER JOIN ubicacion u ON e.ubicacion_id_ubicacion = u.id_ubicacion
WHERE e.estado_equipo IN ('En reparación', 'Fuera de servicio')
AND e.deleted = 0;