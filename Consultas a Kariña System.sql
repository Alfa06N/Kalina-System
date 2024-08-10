USE KariñaSystem;

INSERT INTO Empleado (ciEmpleado, nombre, apellido1, apellido2, fechaNacimiento)
VALUES (31453119, 'Nicolás', 'Alfaro', 'Alessandro', '2006-01-19');

INSERT INTO Cliente (ciCliente, nombre, apellido1, apellido2)
VALUES (16171570, 'María', 'Rodríguez', 'Lopez');

INSERT INTO Usuario (nombreUsuario, contraseña, rol, ciEmpleado) VALUES 
('Alfa06N', 'password123', 'Administrador', 31453119);

INSERT INTO Categoria (nombre, descripcion) VALUES ('Bebidas', 'Bebidas frías y calientes');
INSERT INTO Categoria (nombre, descripcion) VALUES ('Snacks', 'Aperitivos y botanas');
INSERT INTO Categoria (nombre, descripcion) VALUES ('Panadería', 'Productos de panadería y repostería');
INSERT INTO Categoria (nombre, descripcion) VALUES ('Lácteos', 'Productos lácteos y derivados');
INSERT INTO Categoria (nombre, descripcion) VALUES ('Carnes', 'Carnes y embutidos');

INSERT INTO Producto (nombre, stock, minStock, costo, ganancia, iva, descripcion, idCategoria) VALUES
('Café', 100, 10, 10.00, 30.00, 3.00, 'Café negro', 1),
('Galleta', 200, 20, 5.00, 20.00, 2.00, 'Galleta de chocolate', 1);

SELECT * FROM Usuario;
SELECT * FROM Producto;

INSERT INTO UsuarioProducto (idUsuario, idProducto, cantidadProducto, fecha) VALUES
(1, 1, 50, '2024-07-01'), -- Usuario 1 actualizó 50 unidades de producto 1
(1, 2, 100, '2024-07-01'); -- Usuario 2 actualizó 100 unidades de producto 2

-- JOIN entre Usuario y Producto a través de UsuarioProducto
SELECT 
    Usuario.nombreUsuario,
    Usuario.rol,
    Producto.nombre AS nombreProducto,
    Producto.descripcion,
    UsuarioProducto.cantidadProducto,
    UsuarioProducto.fecha
FROM 
    Usuario
JOIN 
    UsuarioProducto ON Usuario.idUsuario = UsuarioProducto.idUsuario
JOIN 
    Producto ON UsuarioProducto.idProducto = Producto.idProducto;

