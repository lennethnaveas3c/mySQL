Esta base de datos fue diseñada con fines educativos para representar un sistema de gestión de usuarios, tipos de usuario, ciudades y personas asociadas. Incluye relaciones, restricciones de integridad y campos de auditoría.

Estructura de Tablas
1. tipo_usuarios
Contiene los tipos de usuario disponibles en el sistema.

id_tipo (PK)

nombre_tipo

descripcion_tipo (mínimo 5 caracteres, con CHECK)

Campos de auditoría (created_at, updated_at, created_by, etc.)

2. usuarios
Almacena información de inicio de sesión y contacto.

id_usuario (PK)

username, password, email (únicos)

Relación con tipo_usuarios (id_tipo_usuario con FK)

Validación: username debe tener al menos 5 caracteres (CHECK)

Campos de auditoría y deleted lógico

3. ciudad
Lista de ciudades y regiones asociadas.

id_ciudad (PK)

nombre_ciudad, region

Validación: nombre_ciudad mínimo 5 caracteres (CHECK)

Campos de auditoría y deleted

4. personas
Información personal y demográfica.

rut (clave única)

nombre_completo (mínimo 5 caracteres)

fecha_nac, id_usuario, id_ciudad (con FK)

Campos de auditoría y deleted

Integridad y Validaciones
Relaciones con claves foráneas entre usuarios, tipo_usuarios, ciudad y personas.

Restricciones CHECK en campos clave para asegurar datos válidos.

Campos de auditoría (created_at, updated_at, etc.) en todas las tablas.

Implementación de borrado lógico con campo deleted.

Datos de ejemplo
La base de datos viene pre-poblada con:

3 tipos de usuario

10 usuarios

5 ciudades

10 personas relacionadas correctamente