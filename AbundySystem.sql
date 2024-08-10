CREATE DATABASE IF NOT EXISTS `Abundysystem`;
USE `Abundysystem`;


-- -----------------------------------------------------
-- Table `Base de datos`.`Producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Producto` (
  `IDProducto` INT NOT NULL,
  `Nombre` VARCHAR(45) NULL,
  `Tipo` TEXT(50) NULL,
  `Cantidad disponible` INT NULL,
  `Descripcion` DECIMAL NULL,
  `Precio` INT NULL,
  `Marca` VARCHAR(50) NULL,
  PRIMARY KEY (`IDProducto`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`EmpresaProveedora`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`EmpresaProveedora` (
  `Rif` varchar(45) NOT NULL,
  `Nombre de Empresa` VARCHAR(50) NULL,
  `ID Direccion` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`Rif`, `ID Direccion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Cliente` (
  `N. de afiliacion` INT NOT NULL,
  `C.I Cliente` INT NOT NULL,
  `ID de Direccion` INT NOT NULL,
  PRIMARY KEY (`N. de afiliacion`, `C.I Cliente`, `ID de Direccion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Usuario` (
  `IDUsuario` INT NOT NULL,
  `Nombre de usuario` VARCHAR(45) NULL,
  `Contraseña` VARCHAR(45) NULL,
  `Tipo de usuario` VARCHAR(45) NULL,
  PRIMARY KEY (`IDUsuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Venta` (
  `IDVenta` INT PRIMARY KEY NOT NULL,
  `Fecha` DATE NULL,
  `IDCliente` INT NOT NULL,
  `Total Venta` FLOAT NULL)

ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `Base de datos`.`DetalleVenta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Abundysystem.DetalleVenta (
   IDDetalleVenta INT NOT NULL,
   IDVenta INT NOT NULL,
   IDProducto INT NOT NULL,
   Cantidad INT NULL,
   Preciounitario DECIMAL NULL,
   IDUsuario INT NOT NULL,
   PRIMARY KEY (IDDetalleVenta),
     FOREIGN KEY (IDVenta) REFERENCES venta (IDVenta),
     FOREIGN KEY (IDProducto) REFERENCES producto (IDProducto),
     FOREIGN KEY (IDUsuario) REFERENCES usuario (IDUsuario)
    );

-- -----------------------------------------------------
-- Table `Base de datos`.`Empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Empleado` (
  `N_Carnet_del_empleado` INT NOT NULL,
  `Tipo de empleado` VARCHAR(45) NULL,
  `Fecha de inicio` DATE NULL,
  `Fecha que Demitio` DATE NULL,
  `ID direccion` INT NOT NULL,
  PRIMARY KEY (`N_Carnet_del_empleado`,`ID direccion` ))
    
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `Base de datos`.`DetalleCompra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`DetalleCompra` (
  `IDDetalleCompra` INT NOT NULL,
  `IDCompra` INT NOT NULL,
  `IDProducto` INT NOT NULL,
  `Cantidad` INT NULL,
  `Precio Unitario` FLOAT NULL,
  `IDUsuario` INT NOT NULL,
  PRIMARY KEY (`IDDetalleCompra`,`IDCompra` ),
 FOREIGN KEY(`IDProducto`) REFERENCES `producto` (`IDProducto`),
FOREIGN KEY (`IDUsuario`) REFERENCES usuario (`IDUsuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Compra` (
  `IDCompra` INT NOT NULL,
  `Fecha` DATE NULL,
  `IDproveedor` INT NOT NULL,
  `Total compra` DECIMAL NULL,
PRIMARY KEY (`IDCompra`),
    FOREIGN KEY (`IDproveedor`)
    REFERENCES compra (`IDCompra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Categoria` (
  `IDCategoria` INT NOT NULL,
  `Nombre` VARCHAR(45) NULL,
  `descripcion` VARCHAR(45) NULL,
  PRIMARY KEY (`IDCategoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`CambioContraseña`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`CambioContraseña` (
  `IDContraseña` INT NOT NULL,
  `IDUsuario` INT NOT NULL,
  `pregunta1` VARCHAR(45) NULL,
  `pregunta2` VARCHAR(45) NULL,
  `pregunta3` VARCHAR(45) NULL,
  `repuesta1` VARCHAR(45) NULL,
  `respuesta2` VARCHAR(45) NULL,
  `respuesta3` VARCHAR(45) NULL,
  PRIMARY KEY (`IDContraseña`),
  FOREIGN KEY (`IDUsuario`) REFERENCES `usuario` (`IDUsuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Persona`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Persona` (
  `C.I` INT NOT NULL,
  `Nombre1` VARCHAR(45) NULL,
  `Nombre2` VARCHAR(45) NULL,
  `Apellido1` VARCHAR(45) NULL,
  `Apellido2` VARCHAR(45) NULL,
  `Fecha de nacimiento` DATE NULL,
  `Edad` INT NULL,
  PRIMARY KEY (`C.I`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Herramienta_Mezcla`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Herramienta_Mezcla` (
  `ID_Herramienta` INT NOT NULL,
  `Nombre` VARCHAR(45) NULL,
  `Descripcion_uno` VARCHAR(45) NULL,
  `Unidad_medida` FLOAT NULL,
  `Medida` FLOAT NULL,
  PRIMARY KEY (`ID_Herramienta`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Sub_categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Sub_categoria` (
  `IDSub_categoria` INT NOT NULL,
  `Nombre` VARCHAR(45) NULL,
  `Descripcion` VARCHAR(45) NULL,
  `IDCategoria` INT NOT NULL,
  PRIMARY KEY (`IDSub_categoria`),
FOREIGN KEY (`IDCategoria`) REFERENCES categoria (`IDCategoria`))
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `Base de datos`.`Direccion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Direccion` (
  `Id Direccion` INT NOT NULL,
  `Codigo postal` INT NULL,
  `Nombre de calle` VARCHAR(45) NULL,
  `Numero de casa` INT NULL,
  `Numero de calle` INT NULL,
  `Tipo de vivienda` VARCHAR(45) NULL,
  `Tipo de Calle` VARCHAR(45) NULL,
  `Punto de referencia` VARCHAR(45) NULL,
  `Municipio` VARCHAR(45) NULL,
  `Ciudad` VARCHAR(45) NULL,
  `Estado` VARCHAR(45) NULL,
  PRIMARY KEY (`Id Direccion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Telefono`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Telefono` (
  `IDTelefono` INT NOT NULL,
  `Codigo de area` INT NULL,
  `Numero_telefono` INT NULL,
  PRIMARY KEY (`IDTelefono`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Correo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Correo` (
  `ID_Correo`  VARCHAR(45) NOT NULL,
  `Direccion de correo` VARCHAR(45) NULL,
  PRIMARY KEY (`ID_Correo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Entrega`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Entrega` (
  `IDEntrega` INT NOT NULL,
  `Fecha_entrega` VARCHAR(45) NULL,
  `Nombre_Producto` VARCHAR(45) NULL,
  `Cantidad_producto` VARCHAR(45) NULL,
  `IDProducto` INT NOT NULL,
  `Rif` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IDEntrega`), 
FOREIGN KEY (`IDProducto`) REFERENCES producto (`IDProducto`))

ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Empleado_tiene_correo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Empleado_tiene_correo` (
  `idEmpleado_tiene_correo` INT NOT NULL,
  `ID_correo` VARCHAR(45) NOT NULL,
  `N_carnet_empleado` INT NOT NULL,
  PRIMARY KEY (`idEmpleado_tiene_correo`)) 
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Empleado_tiene_tlf`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Empleado_tiene_tlf` (
  `idEmpleado_tiene_tlf` INT NOT NULL,
  `N_Carnet_del_empleado` INT NOT NULL,
  `IDTelefono` INT NOT NULL,
  PRIMARY KEY (`idEmpleado_tiene_tlf`),
FOREIGN KEY (`IDTelefono`) REFERENCES telefono (`IDTelefono`)) 
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Cliente_tiene_tlf`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Cliente_tiene_tlf` (
  `idCliente_tiene_tlf` INT NOT NULL,
  `IDTelefono` INT NOT NULL,
  `C.I Cliente` INT NOT NULL,
  PRIMARY KEY (`idCliente_tiene_tlf`),
FOREIGN KEY(`IDTelefono`) REFERENCES telefono (`IDTelefono`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Cliente_tiene_correo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Cliente_tiene_correo` (
  `IDCliente_tiene_correo` INT NOT NULL,
  `ID_Correo` VARCHAR(45) NOT NULL,
  `CI.Cliente` INT NOT NULL,
  PRIMARY KEY (`IDCliente_tiene_correo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Producto_utiliza_herramienta_mezcla`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Producto_utiliza_herramienta_mezcla` (
  `idProducto_utiliza_herramienta_mezcla` INT NOT NULL,
  `Cantidad_Utilizada` VARCHAR(45) NULL,
  `Fecha_uso` TIME NULL,
  `IDProducto` INT NOT NULL,
  `ID_Herramienta` INT NOT NULL,
  PRIMARY KEY (`idProducto_utiliza_herramienta_mezcla`),
FOREIGN KEY(`IDProducto`) REFERENCES producto (`IDProducto`),
FOREIGN KEY(`ID_Herramienta`) REFERENCES Herramienta_Mezcla (`ID_Herramienta`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Base de datos`.`Producto_pertenece_categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Abundysystem`.`Producto_pertenece_categoria` (
  `IDProducto_pertenece_categoria` INT NOT NULL,
  `IDCategoria` INT NOT NULL,
  `IDProducto` INT NOT NULL,
  PRIMARY KEY (`IDProducto_pertenece_categoria`),
FOREIGN KEY (`IDCategoria`) REFERENCES categoria (`IDCategoria`),
FOREIGN KEY(`IDProducto`) REFERENCES producto (`IDProducto`))

ENGINE = InnoDB;


insert into abundysystem.usuario (`IDUsuario`,`Nombre de usuario`,`Contraseña`,`Tipo de usuario`) values ('1', 'Jose Narvaez', 'Alg454','Gerente');
insert into abundysystem.usuario (`IDUsuario`,`Nombre de usuario`,`Contraseña`,`Tipo de usuario`) values ('2', 'Francisco Coll', '45A459','Cajero');
insert into abundysystem.usuario (`IDUsuario`,`Nombre de usuario`,`Contraseña`,`Tipo de usuario`) values ('3', 'Alberto Bernaez', 'Blr564','SubGerente');
insert into abundysystem.usuario (`IDUsuario`,`Nombre de usuario`,`Contraseña`,`Tipo de usuario`) values ('4', 'Arlety Rosas', 'Fvv453','Seguridad');
insert into abundysystem.cliente (`N. de afiliacion`,`C.I Cliente`,`ID de Direccion`) values ('1', '11004822', '1');
insert into abundysystem.cliente (`N. de afiliacion`,`C.I Cliente`,`ID de Direccion`) values ('2', '10845782', '2');
insert into abundysystem.cliente (`N. de afiliacion`,`C.I Cliente`,`ID de Direccion`) values ('3', '982789', '2');
insert into abundysystem.cliente (`N. de afiliacion`,`C.I Cliente`,`ID de Direccion`) values ('4', '4352785', '3');


select * from abundysystem.usuario;

select * from abundysystem.cliente;


SELECT * FROM cliente WHERE `ID de Direccion`= '2';

