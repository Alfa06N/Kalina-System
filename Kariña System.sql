DROP DATABASE `KariñaSystem`;
CREATE DATABASE IF NOT EXISTS `KariñaSystem`;

USE KariñaSystem;

CREATE TABLE IF NOT EXISTS Empleado (
    ciEmpleado INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido1 VARCHAR(50) NOT NULL,
    apellido2 VARCHAR(50),
    fechaNacimiento DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Cliente (
    ciCliente INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido1 VARCHAR(50) NOT NULL,
    apellido2 VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Categoria (
    idCategoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS Producto (
    idProducto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    stock INT NOT NULL,
    minStock INT NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    ganancia DECIMAL(10, 2),
    iva DECIMAL(5, 2),
    descripcion TEXT,
    idCategoria INT,
    FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria)
);

CREATE TABLE IF NOT EXISTS Usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nombreUsuario VARCHAR(50) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'Colaborador') NOT NULL,
    ciEmpleado INT,
    FOREIGN KEY (ciEmpleado) 
    REFERENCES Empleado(ciEmpleado)
);

CREATE TABLE IF NOT EXISTS Cierre (
    idCierre INT AUTO_INCREMENT PRIMARY KEY,
    monto DECIMAL(10, 2) NOT NULL,
    fecha DATE NOT NULL,
    ganancia DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Venta (
    idVenta INT AUTO_INCREMENT PRIMARY KEY,
    precioTotal DECIMAL(10, 2) NOT NULL,
    idUsuario INT,
    fecha DATE NOT NULL,
    ganancia DECIMAL(10, 2),
    idCierre INT, 
    FOREIGN KEY (idCierre) REFERENCES Cierre(idCierre),
    FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
);

CREATE TABLE IF NOT EXISTS Pago (
    idPago INT AUTO_INCREMENT PRIMARY KEY,
    monto DECIMAL(10, 2) NOT NULL,
    metodo VARCHAR(20) NOT NULL,
    ciCliente INT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    idVenta INT,
    FOREIGN KEY (ciCliente) REFERENCES Cliente(ciCliente),
    FOREIGN KEY (idVenta) REFERENCES Venta(idVenta)
);

CREATE TABLE IF NOT EXISTS Recuperacion (
    idRecuperacion INT AUTO_INCREMENT PRIMARY KEY,
    pregunta1 TEXT NOT NULL,
    respuesta1 TEXT NOT NULL,
    pregunta2 TEXT NOT NULL,
    respuesta2 TEXT NOT NULL,
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
);

CREATE TABLE IF NOT EXISTS Telefono (
    idTelefono INT AUTO_INCREMENT PRIMARY KEY,
    area INTEGER NOT NULL,
    numero INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    idEmpleado INT,
    FOREIGN KEY (idEmpleado) REFERENCES Empleado(ciEmpleado)
);

CREATE TABLE IF NOT EXISTS UsuarioProducto (
    idUsuarioProducto INT AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT,
    idProducto INT,
    cantidadProducto INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
    FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
);

CREATE TABLE IF NOT EXISTS VentaProducto (
    idVentaProducto INT AUTO_INCREMENT PRIMARY KEY,
    idVenta INT,
    idProducto INT,
    cantidadProducto INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (idVenta) REFERENCES Venta(idVenta),
    FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
);

CREATE TABLE IF NOT EXISTS Vuelto (
    idVuelto INT AUTO_INCREMENT PRIMARY KEY,
    montoDevuelto DECIMAL(10, 2) NOT NULL,
    metodo VARCHAR(20) NOT NULL,
    idVenta INT,
    FOREIGN KEY (idVenta) REFERENCES Venta(idVenta)
);

CREATE TABLE IF NOT EXISTS Combo (
    idCombo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS VentaCombo (
	idVentaCombo INT AUTO_INCREMENT PRIMARY KEY,
    idVenta INT,
    idCombo INT,
    cantidadCombo INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (idVenta) REFERENCES Venta(idVenta),
    FOREIGN kEY (idCombo) REFERENCES Combo(idCombo)
);

CREATE TABLE IF NOT EXISTS ProductoCombo (
    idProductoCombo INT AUTO_INCREMENT PRIMARY KEY,
    idProducto INT,
    idCombo INT,
    cantidadProducto INT NOT NULL,
    FOREIGN KEY (idProducto) REFERENCES Producto(idProducto),
    FOREIGN KEY (idCombo) REFERENCES Combo(idCombo)
);

CREATE TABLE IF NOT EXISTS Efectivo (
    idPago INT,
    serial VARCHAR(50) NOT NULL,
    moneda VARCHAR(20) NOT NULL,
    PRIMARY KEY (idPago),
    FOREIGN KEY (idPago) REFERENCES Pago(idPago)
);

CREATE TABLE IF NOT EXISTS CriptoActivo (
    idPago INT,
    referencia VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    billetera VARCHAR(100) NOT NULL,
    PRIMARY KEY (idPago),
    FOREIGN KEY (idPago) REFERENCES Pago(idPago)
);

CREATE TABLE IF NOT EXISTS PagoMovil (
    idPago INT,
    referencia VARCHAR(100) NOT NULL,
    telefono INT NOT NULL,
    PRIMARY KEY (idPago),
    FOREIGN KEY (idPago) REFERENCES Pago(idPago)
);

CREATE TABLE IF NOT EXISTS Transferencia (
    idPago INT,
    bancoDestino VARCHAR(50) NOT NULL,
    referencia VARCHAR(100) NOT NULL,
    PRIMARY KEY (idPago),
    FOREIGN KEY (idPago) REFERENCES Pago(idPago)
);

CREATE TABLE IF NOT EXISTS BioPago (
    idPago INT,
    referencia VARCHAR(100) NOT NULL,
    PRIMARY KEY (idPago),
    FOREIGN KEY (idPago) REFERENCES Pago(idPago)
);

CREATE TABLE IF NOT EXISTS Punto (
    idPago INT,
    punto INT NOT NULL,
    PRIMARY KEY (idPago),
    FOREIGN KEY (idPago) REFERENCES Pago(idPago)
);

CREATE TABLE IF NOT EXISTS Estadistica (
    idEstadistica INT AUTO_INCREMENT PRIMARY KEY,
    producto1 INT,
    cantidad1 INT NOT NULL,
    producto2 INT,
    cantidad2 INT NOT NULL,
    producto3 INT,
    cantidad3 INT NOT NULL,
    cantidadOtros INT NOT NULL,
    InicioMes DATE NOT NULL,
    FinMes DATE NOT NULL,
    FOREIGN KEY (producto1) REFERENCES Producto(idProducto),
    FOREIGN KEY (producto2) REFERENCES Producto(idProducto),
    FOREIGN KEY (producto3) REFERENCES Producto(idProducto)
);