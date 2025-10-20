CREATE DATABASE empresa;
USE empresa;

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    cargo VARCHAR(50),
    sueldo DECIMAL(10,2)
);

INSERT INTO empleados (nombre, cargo, sueldo) VALUES
('Juan Pérez', 'Administrador', 850000),
('Ana Gómez', 'Vendedora', 650000),
('Carlos Rojas', 'Técnico', 720000);