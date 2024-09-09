from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Text, Enum, Time, DateTime
from sqlalchemy.orm import relationship, declarative_base
from config import engine
from enum import Enum as PyEnum
from utils.dateConversions import getUTC

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
  secondSurname = Column(String(50), default="")
  birthdate = Column(Date, nullable=False)
  
  user = relationship("User", back_populates="employee", uselist=False, cascade="all, delete-orphan")
  phones = relationship("Phone", back_populates="employee", cascade="all, delete-orphan")

class User(Base):
  __tablename__ = "User"
  
  idUser = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username = Column(String(50), nullable=False)
  password = Column(String(255), nullable=False)
  role = Column(Enum("Administrador", "Colaborador"), nullable=False)
  ciEmployee = Column(Integer, ForeignKey("Employee.ciEmployee", ondelete="CASCADE"))
  
  employee = relationship("Employee", back_populates="user", uselist=False)
  sales = relationship("Sale", back_populates="user")
  recovery = relationship("Recovery", back_populates="user", uselist=False)
  products = relationship("UserProduct", back_populates="user")
  
class Phone(Base):
  __tablename__ = "Telefono"
  
  idPhone = Column(Integer, primary_key=True, autoincrement=True, index=True)
  area = Column(String(4), nullable=False)
  number = Column(String(7), nullable=False)
  kind = Column(Enum("Casa", "Móvil", "Empresa"), nullable=True)
  ciEmployee = Column(Integer, ForeignKey('Employee.ciEmployee', ondelete="CASCADE"))
  
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
  imgPath = Column(String(50), default=None)
  
  products = relationship("Product", back_populates="category")

class Product(Base):
  __tablename__ = "Product"
  
  idProduct = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  stock = Column(Integer, nullable=False)
  minStock = Column(Integer, nullable=False)
  cost = Column(DECIMAL(10, 3), nullable=False)
  gain = Column(DECIMAL(10, 3), nullable=False)
  iva = Column(DECIMAL(5, 3), nullable=False)
  description = Column(Text)
  imgPath = Column(String(50), default=None)
  idCategory = Column(Integer, ForeignKey("Category.idCategory"))
  
  users = relationship("UserProduct", back_populates="product")
  category = relationship("Category", back_populates="products")
  sales = relationship("SaleProduct", back_populates="product")
  combos = relationship("ProductCombo", back_populates="product", cascade="all, delete-orphan")
  
class Closing(Base):
  __tablename__ = "Closing"
  
  idClosing = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(DECIMAL(10, 3), nullable=False)
  date = Column(Date, nullable=False)
  gain = Column(DECIMAL(10, 3))

  sales = relationship("Sale", back_populates="closing")
  
class Sale(Base):
  __tablename__ = "Sale"
  
  idSale = Column(Integer, primary_key=True, autoincrement=True)
  totalPrice = Column(DECIMAL(10, 3), nullable=False)
  date = Column(DateTime, nullable=False, default=getUTC())
  gain = Column(DECIMAL(10, 3))
  idClosing = Column(Integer, ForeignKey("Closing.idClosing"), default=None)
  idUser = Column(Integer, ForeignKey("User.idUser"))
  ciClient = Column(Integer, ForeignKey("Client.ciClient"))
  
  closing = relationship("Closing", back_populates="sales")
  user = relationship("User", back_populates="sales")
  client = relationship("Client", back_populates="sales")
  payments = relationship("Payment", back_populates="sale", cascade="all, delete-orphan")
  changes = relationship("Change", back_populates="sale", cascade="all, delete-orphan")
  combos = relationship("SaleCombo", back_populates="sale", cascade="all, delete-orphan")
  products = relationship("SaleProduct", back_populates="sale", cascade="all, delete-orphan")
  
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
  date = Column(DateTime, nullable=False, default=getUTC())
  
  user = relationship("User", back_populates="products")
  product = relationship("Product", back_populates="users")
  
class SaleProduct(Base):
  __tablename__ = "SaleProduct"
  
  idSaleProduct = Column(Integer, primary_key=True, autoincrement=True)
  productQuantity = Column(Integer, nullable=False)
  price = Column(DECIMAL(10, 3), nullable=False)
  idSale = Column(Integer, ForeignKey("Sale.idSale", ondelete="CASCADE"))
  idProduct = Column(Integer, ForeignKey("Product.idProduct"))
  
  sale = relationship("Sale", back_populates="products")
  product = relationship("Product", back_populates="sales")
  
class Change(Base):
  __tablename__ = "Change"
  
  idChange = Column(Integer, primary_key=True, autoincrement=True)
  amountReturned = Column(DECIMAL(10, 2), nullable=False)
  method = Column(String(20), nullable=False)
  idSale = Column(Integer, ForeignKey("Sale.idSale", ondelete="CASCADE"))
  
  sale = relationship("Sale", back_populates="changes")

class Combo(Base):
  __tablename__ = "Combo"
  
  idCombo = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  cost = Column(DECIMAL(10, 3), nullable=False, default=0.0)
  price = Column(DECIMAL(10, 3), default=None)
  imgPath = Column(String(50), default=None)
  sales = relationship("SaleCombo", back_populates="combo")
  products = relationship("ProductCombo", back_populates="combo", cascade="all, delete-orphan")
  
class ProductCombo(Base):
  __tablename__ = "ProductCombo"
  
  idProductCombo = Column(Integer, primary_key=True, autoincrement=True)
  idProduct = Column(Integer, ForeignKey("Product.idProduct", ondelete="CASCADE"))
  idCombo = Column(Integer, ForeignKey("Combo.idCombo", ondelete="CASCADE"))
  productQuantity = Column(Integer, nullable=False)
  
  product = relationship("Product", back_populates="combos")
  combo = relationship("Combo", back_populates="products")

class SaleCombo(Base):
  __tablename__ = "SaleCombo"
  
  idSaleCombo = Column(Integer, primary_key=True, autoincrement=True)
  idSale = Column(Integer, ForeignKey("Sale.idSale", ondelete="CASCADE"))
  price = Column(DECIMAL(10, 3))
  idCombo = Column(Integer, ForeignKey("Combo.idCombo"))
  comboQuantity = Column(Integer, nullable=False)
  sale = relationship("Sale", back_populates="combos")
  combo = relationship("Combo", back_populates="sales")
  
class Payment(Base):
  __tablename__ = "Payment"
  
  idPayment = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(DECIMAL(10, 3), nullable=False)
  method = Column(Enum(MethodEnum), nullable=False)
  reference = Column(String(100))
  idSale = Column(Integer, ForeignKey("Sale.idSale", ondelete="CASCADE"))
  
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