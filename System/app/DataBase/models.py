from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Text, Enum, Time
from sqlalchemy.orm import relationship, declarative_base
from config import engine
from enum import Enum as PyEnum

Base = declarative_base()

class RoleEnum(PyEnum):
  ADMIN = "Administrador"
  COLLABORATOR = "Colaborador"
  
class MethodEnum(PyEnum):
  CASH = "Efectivo"
  BANK_TRANSFER = "Transferencia"
  BIO_PAYMENT = "Biopago"
  MOBILE_PAYMENT = "Pago Móvil"
  POINT_OF_SALE = "Punto de Venta"
  CRYPTO_ACTIVE = "Cripto Activo"

class Employee(Base):
  __tablename__ = "Employee"
  
  ciEmployee = Column(Integer, primary_key=True, index=True)
  name = Column(String(50), nullable=False)
  surname = Column(String(50), nullable=False)
  secondSurname = Column(String(50))
  birthdate = Column(Date, nullable=False)
  
  user = relationship("User", back_populates="employee", uselist=False)
  phones = relationship("Phone", back_populates="employee")

class User(Base):
  __tablename__ = "User"
  
  idUser = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username = Column(String(50), nullable=False)
  password = Column(String(255), nullable=False)
  role = Column(Enum("Administrador", "Colaborador"), nullable=False)
  ciEmployee = Column(Integer, ForeignKey("Employee.ciEmployee"))
  
  employee = relationship("Employee", back_populates="user", uselist=False)
  sales = relationship("Sale", back_populates="user")
  recovery = relationship("Recovery", back_populates="user", uselist=False)
  products = relationship("UserProduct", back_populates="user")
  
class Phone(Base):
  __tablename__ = "Telefono"
  
  idPhone = Column(Integer, primary_key=True, autoincrement=True, index=True)
  area = Column(Integer, nullable=False)
  number = Column(Integer, nullable=False)
  kind = Column(String(20), nullable=True)
  ciEmployee = Column(Integer, ForeignKey('Employee.ciEmployee'))
  
  employee = relationship("Employee", back_populates="phones")
  
class Client(Base):
  __tablename__ = "Client"
  
  ciClient = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  surname = Column(String(50), nullable=False)
  secondSurname = Column(String(50))
  
  sales = relationship("Sale", back_populates="client")

class Category(Base):
  __tablename__ = "Category"
  
  # name must to be unique
  idCategory = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  description = Column(Text)
  
  products = relationship("Product", back_populates="category")

class Product(Base):
  __tablename__ = "Product"
  
  idProduct = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  stock = Column(Integer, nullable=False)
  minStock = Column(Integer, nullable=False)
  cost = Column(DECIMAL(10, 2), nullable=False)
  gain = Column(DECIMAL(10, 2), nullable=False)
  iva = Column(DECIMAL(5, 2), nullable=False)
  description = Column(Text)
  idCategory = Column(Integer, ForeignKey("Category.idCategory"))
  
  users = relationship("UserProduct", back_populates="product")
  category = relationship("Category", back_populates="products")
  sales = relationship("SaleProduct", back_populates="product")
  combos = relationship("ProductCombo", back_populates="product")
  
class Closing(Base):
  __tablename__ = "Closing"
  
  idClosing = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(DECIMAL(10, 2), nullable=False)
  date = Column(Date, nullable=False)
  gain = Column(DECIMAL(10, 2))
  
  sales = relationship("Sale", back_populates="closing")
  
class Sale(Base):
  __tablename__ = "Sale"
  
  idSale = Column(Integer, primary_key=True, autoincrement=True)
  totalPrice = Column(DECIMAL(10, 2), nullable=False)
  date = Column(Date, nullable=False)
  gain = Column(DECIMAL(10, 2))
  idClosing = Column(Integer, ForeignKey("Closing.idClosing"))
  idUser = Column(Integer, ForeignKey("User.idUser"))
  idClient = Column(Integer, ForeignKey("Client.ciClient"))
  idPayment = Column(Integer, ForeignKey("Payment.idPayment"))
  
  closing = relationship("Closing", back_populates="sales")
  user = relationship("User", back_populates="sales")
  client = relationship("Client", back_populates="sales")
  payments = relationship("Payment", back_populates="sale", uselist=False)
  changes = relationship("Change", back_populates="sale")
  combos = relationship("SaleCombo", back_populates="sale")
  products = relationship("SaleProduct", back_populates="sale")
  
class Recovery(Base):
  __tablename__ = "Recovery"
  
  idRecovery = Column(Integer, primary_key=True, autoincrement=True)
  questionOne = Column(Text, nullable=False)
  answerOne = Column(Text, nullable=False)
  questionTwo = Column(Text, nullable=False)
  answerTwo = Column(Text, nullable=False)
  
  idUser = Column(Integer, ForeignKey("User.idUser"))
  user = relationship("User", back_populates="recovery")
  
class UserProduct(Base):
  __tablename__ = "UserProduct"
  
  idUserProduct = Column(Integer, primary_key=True, autoincrement=True)
  idUser = Column(Integer, ForeignKey("User.idUser"))
  idProduct = Column(Integer, ForeignKey("Product.idProduct"))
  productQuantity = Column(Integer, nullable=False)
  date = Column(Date, nullable=False)
  
  user = relationship("User", back_populates="products")
  product = relationship("Product", back_populates="users")
  
class SaleProduct(Base):
  __tablename__ = "SaleProduct"
  
  idSaleProduct = Column(Integer, primary_key=True, autoincrement=True)
  productQuantity = Column(Integer, nullable=False)
  date = Column(Date, nullable=False)
  idSale = Column(Integer, ForeignKey("Sale.idSale"))
  idProduct = Column(Integer, ForeignKey("Product.idProduct"))
  
  sale = relationship("Sale", back_populates="products")
  product = relationship("Product", back_populates="sales")
  
class Change(Base):
  __tablename__ = "Change"
  
  idChange = Column(Integer, primary_key=True, autoincrement=True)
  amountReturned = Column(DECIMAL(10, 2), nullable=False)
  method = Column(String(20), nullable=False)
  idSale = Column(Integer, ForeignKey("Sale.idSale"))
  
  sale = relationship("Sale", back_populates="changes")

class Combo(Base):
  __tablename__ = "Combo"
  
  idCombo = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  price = Column(DECIMAL(10, 2), nullable=False)
  sales = relationship("SaleCombo", back_populates="combo")
  products = relationship("ProductCombo", back_populates="combo")
  
class ProductCombo(Base):
  __tablename__ = "ProductCombo"
  
  idProductCombo = Column(Integer, primary_key=True, autoincrement=True)
  idProduct = Column(Integer, ForeignKey("Product.idProduct"))
  idCombo = Column(Integer, ForeignKey("Combo.idCombo"))
  productQuantity = Column(Integer, nullable=False)
  
  product = relationship("Product", back_populates="combos")
  combo = relationship("Combo", back_populates="products")

class SaleCombo(Base):
  __tablename__ = "SaleCombo"
  
  idSaleCombo = Column(Integer, primary_key=True, autoincrement=True)
  idSale = Column(Integer, ForeignKey("Sale.idSale"))
  idCombo = Column(Integer, ForeignKey("Combo.idCombo"))
  comboQuantity = Column(Integer, nullable=False)
  date = Column(Date, nullable=False)
  sale = relationship("Sale", back_populates="combos")
  combo = relationship("Combo", back_populates="sales")
  
class Payment(Base):
  __tablename__ = "Payment"
  
  idPayment = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(DECIMAL(10, 2), nullable=False)
  method = Column(Enum(MethodEnum), nullable=False)
  reference = Column(String(100))
  date = Column(Date, nullable=False)
  time = Column(Time, nullable=False)
  
  sale = relationship("Sale", back_populates="payments")

class Statistic(Base):
  __tablename__ = "Statistic"
  
  idStatistic = Column(Integer, primary_key=True, autoincrement=True)
  productOne = Column(Integer, ForeignKey("Product.idProduct"))
  quantityOne = Column(Integer, nullable=False)
  productTwo = Column(Integer, ForeignKey("Product.idProduct"))
  quantityTwo = Column(Integer, nullable=False)
  productThree = Column(Integer, ForeignKey("Product.idProduct"))
  quantityThree = Column(Integer, nullable=False)
  quantityOthers = Column(Integer, nullable=False)
  startOfMonth = Column(Date, nullable=False)
  endOfMonth = Column(Date, nullable=False)
  
Base.metadata.create_all(engine)