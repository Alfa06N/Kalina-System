from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Text, Enum, Time, DateTime
from sqlalchemy.orm import relationship, declarative_base
from config import engine
from enum import Enum as PyEnum
from utils.dateConversions import getUTC, getLocal

Base = declarative_base()

class RoleEnum(PyEnum):
  ADMIN = "Administrador"
  COLLABORATOR = "Colaborador"
  
class MethodEnum(PyEnum):
  EFECTIVO = "Efectivo"
  TRANSFERENCIA = "Transferencia"
  BIOPAGO = "Biopago"
  PAGO_MOVIL = "Pago Móvil"
  PUNTO_DE_VENTA = "Punto de Venta"
  CRIPTO_ACTIVO = "Cripto Activo"

class Employee(Base):
  __tablename__ = "Employee"
  
  ciEmployee = Column(Integer, primary_key=True, index=True)
  name = Column(String(25), nullable=False)
  surname = Column(String(25), nullable=False)
  secondSurname = Column(String(25), default="")
  birthdate = Column(Date, nullable=False)
  
  user = relationship("User", back_populates="employee", uselist=False, cascade="all, delete-orphan")

class User(Base):
  __tablename__ = "User"
  
  idUser = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username = Column(String(25), nullable=False)
  password = Column(String(25), nullable=False)
  role = Column(Enum("Administrador", "Colaborador"), nullable=False)
  ciEmployee = Column(Integer, ForeignKey("Employee.ciEmployee", ondelete="CASCADE"))
  
  closings = relationship("Closing", back_populates="user")
  employee = relationship("Employee", back_populates="user", uselist=False)
  sales = relationship("Sale", back_populates="user")
  recovery = relationship("Recovery", back_populates="user", uselist=False)
  products = relationship("UserProduct", back_populates="user")
  
class Client(Base):
  __tablename__ = "Client"
  
  ciClient = Column(String(25), primary_key=True)
  name = Column(String(25), nullable=False)
  surname = Column(String(25), nullable=False)
  secondSurname = Column(String(25))
  documentType = Column(Enum("Jurídico", "Venezolano", "Extranjero", "Gubernamental"), nullable=False)
  
  sales = relationship("Sale", back_populates="client")

class Category(Base):
  __tablename__ = "Category"

  idCategory = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(25), nullable=False)
  description = Column(Text)
  imgPath = Column(String(50), default=None)
  
  products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

class Product(Base):
  __tablename__ = "Product"
  
  idProduct = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(25), nullable=False)
  stock = Column(Integer, nullable=False)
  minStock = Column(Integer, nullable=False)
  cost = Column(DECIMAL(10, 3), nullable=False)
  gain = Column(DECIMAL(10, 3), nullable=False)
  iva = Column(DECIMAL(10, 3), nullable=False)
  description = Column(Text)
  imgPath = Column(String(50), default=None)
  idCategory = Column(Integer, ForeignKey("Category.idCategory", ondelete="CASCADE"))
  
  users = relationship("UserProduct", back_populates="product")
  category = relationship("Category", back_populates="products")
  sales = relationship("SaleProduct", back_populates="product", cascade="all, delete")
  combos = relationship("ProductCombo", back_populates="product", cascade="all, delete")
  
class Closing(Base):
  __tablename__ = "Closing"
  
  idClosing = Column(Integer, primary_key=True, autoincrement=True)
  amount = Column(DECIMAL(10, 3), nullable=False)
  date = Column(DateTime, nullable=False, default=getLocal())
  gain = Column(DECIMAL(10, 3))
  idUser = Column(Integer, ForeignKey("User.idUser"))

  user = relationship("User", back_populates="closings")
  sales = relationship("Sale", back_populates="closing")
  
class Sale(Base):
  __tablename__ = "Sale"
  
  idSale = Column(Integer, primary_key=True, autoincrement=True)
  totalPrice = Column(DECIMAL(10, 3), nullable=False)
  date = Column(DateTime, nullable=False, default=getLocal())
  gain = Column(DECIMAL(10, 3))
  idClosing = Column(Integer, ForeignKey("Closing.idClosing"), default=None)
  idUser = Column(Integer, ForeignKey("User.idUser"))
  ciClient = Column(String(25), ForeignKey("Client.ciClient"))
  
  closing = relationship("Closing", back_populates="sales")
  user = relationship("User", back_populates="sales")
  client = relationship("Client", back_populates="sales")
  combos = relationship("SaleCombo", back_populates="sale", cascade="all, delete")
  products = relationship("SaleProduct", back_populates="sale", cascade="all, delete")
  transactions = relationship("Transaction", back_populates="sale", cascade="all, delete-orphan")
  
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
  date = Column(DateTime, nullable=False, default=getLocal())
  
  user = relationship("User", back_populates="products")
  product = relationship("Product", back_populates="users")
  
class SaleProduct(Base):
  __tablename__ = "SaleProduct"
  
  idSaleProduct = Column(Integer, primary_key=True, autoincrement=True)
  productQuantity = Column(Integer, nullable=False)
  price = Column(DECIMAL(10, 3), nullable=False)
  idSale = Column(Integer, ForeignKey("Sale.idSale", ondelete="SET NULL"))
  idProduct = Column(Integer, ForeignKey("Product.idProduct", ondelete="SET NULL"))
  
  sale = relationship("Sale", back_populates="products")
  product = relationship("Product", back_populates="sales")

class Combo(Base):
  __tablename__ = "Combo"
  
  idCombo = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(25), nullable=False)
  cost = Column(DECIMAL(10, 3), nullable=False, default=0.0)
  price = Column(DECIMAL(10, 3), default=None)
  imgPath = Column(String(50), default=None)
  sales = relationship("SaleCombo", back_populates="combo", cascade="all, delete")
  products = relationship("ProductCombo", back_populates="combo", cascade="all, delete")
  
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
  idSale = Column(Integer, ForeignKey("Sale.idSale", ondelete="SET NULL"))
  price = Column(DECIMAL(10, 3))
  idCombo = Column(Integer, ForeignKey("Combo.idCombo", ondelete="SET NULL"))
  comboQuantity = Column(Integer, nullable=False)
  sale = relationship("Sale", back_populates="combos")
  combo = relationship("Combo", back_populates="sales")
  
class Transaction(Base):
  __tablename__ = "Transaction"
  
  idTransaction = Column(Integer, primary_key=True)
  amountUSD = Column(DECIMAL(10, 3), nullable=True, default=None)
  amountVES = Column(DECIMAL(10, 3), nullable=True, default=None)
  exchangeRate = Column(DECIMAL(10, 3), nullable=False)
  method = Column(Enum(MethodEnum), nullable=False)
  transactionType = Column(Enum("Pago", "Cambio"))
  reference = Column(String(50), nullable=True)
  idSale = Column(Integer, ForeignKey("Sale.idSale", ondelete="CASCADE"))
  
  sale = relationship("Sale", back_populates="transactions")
  
Base.metadata.create_all(engine)