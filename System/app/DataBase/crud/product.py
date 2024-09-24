from sqlalchemy.orm import Session
from DataBase.models import Product, UserProduct
from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError, DataAlreadyExists
from utils.sessionManager import getCurrentUser
from DataBase.crud.user import getUserByUsername
from DataBase.crud.user_product import registerOperation
from datetime import datetime
from sqlalchemy import asc, desc

def createProduct(db: Session, name: str, description: str, stock: int, minStock: int, cost: float, gain: float, iva: float, idCategory: int, imgPath: str):
  try:
    alreadyExists = getProductByName(db, name)
    
    if alreadyExists:
      raise DataAlreadyExists("Nombre de producto no disponible")
    
    print(f"Antes de crear el producto: {stock} - {minStock}")
    product = Product(
      name=name,
      description=description,
      stock=stock,
      minStock=minStock,
      cost=cost,
      gain=gain,
      iva=iva,
      imgPath=imgPath,
      idCategory=idCategory
    )
    
    def func():
      db.add(product)
      db.commit()
    
    handleDatabaseErrors(db, func)
    
    db.refresh(product)
    print(f"Después de crear el producto: {product.stock} - {product.minStock}")
    return product
  except Exception as e:
    raise
  
def getProductById(db: Session, idProduct: int):
  try:
    def func():
      return db.query(Product).filter(Product.idProduct == idProduct).first()
    
    return handleDatabaseErrors(db, func)
  
  except Exception as e:
    raise
  
def getProductByName(db: Session, name: str):
  try:
    def func():
      return db.query(Product).filter(Product.name == name).first()
    
    return handleDatabaseErrors(db, func)
  
  except Exception as e:
    raise
  
def getProducts(db: Session):
  try:
    def func():
      return db.query(Product).order_by(asc(Product.name)).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def updateProduct(db: Session, idProduct: int, name: str, description: str, minStock: int, cost: float, gain: float, iva: float, idCategory: int):
  try:
    if getProductByName(db, name):
      raise DataAlreadyExists("Nombre de usuario no disponible")   
    else:
      product = getProductById(db, idProduct)
      
      def func():
        if product:
          if name:
            product.name = name
          if description:
            product.description = description
          if minStock:
            product.minStock = minStock
          if cost:
            product.cost = cost
          if gain:
            product.gain = gain
          if iva:
            product.iva = iva
          if idCategory:
            product.idCategory = idCategory
          
          db.commit()
          db.refresh(product)
          return product
        else:
          raise DataNotFoundError("No se encontró el producto original")
      
      return handleDatabaseErrors(db, func)
  except DataAlreadyExists as e:
    raise
  except Exception:
    raise

def updateProductInfo(db: Session, product, name:str, description:str, idCategory:int):
  try:
    if not product:
      raise DataNotFoundError("Producto no encontrado")
    
    def func():
      if name:
        product.name = name
      product.description = description
      if idCategory:
        product.idCategory = idCategory
      db.commit()
    
    handleDatabaseErrors(db, func)
    db.refresh(product)
    return product
  except DataNotFoundError:
    raise
  except Exception as err:
    raise

def removeProduct(db: Session, product):
  try:  
    def func():
      db.delete(product)
      db.commit()
      
    handleDatabaseErrors(db, func)
    
    return product
  except Exception:
    raise
  
def removeProductByName(db: Session, name: str):
  try:
    product = getProductByName(db, idProduct)
    
    def func():
      db.delete(product)
      db.commit()
      
    handleDatabaseErrors(db, func)
    
    return product
  except Exception:
    raise

def calculatePrice(cost, iva, gain):
  try: 
      price = cost + (cost*(iva/100)) + (cost*(gain/100))
      return round(price, 2) 
  except DataNotFoundError as e:
    print(e)
    raise
  except Exception:
    raise
  
def updateProductStock(db: Session, product, quantityAdded: int):
  try:
    username = getCurrentUser()
    user = getUserByUsername(db, username)
    
    if not product:
      raise DataNotFoundError(f"No se encontró el producto {name}")
    elif not user:
      raise DataNotFoundError(f"No se encontró el usuario {username}")
    
    def func():
      product.stock += quantityAdded
      register = registerOperation(
        db=db,
        idUser=user.idUser,
        idProduct=product.idProduct,
        productQuantity=quantityAdded
      )
      db.add(register)
      db.commit()
      return register
    
    
    register = handleDatabaseErrors(db, func)
    db.refresh(product)
    db.refresh(register)
    return product, register
  except Exception:
    db.rollback()
    raise

def updateProductPrices(db: Session, product, cost:float, iva:float, gain:float):
  try:
    if not product:
      raise DataNotFoundError("Producto no encontrado")
    
    def func():
      if cost:
        product.cost = cost
      if iva:
        product.iva = iva
      if gain:
        product.gain = gain
      
      db.commit()
      return product
    
    product = handleDatabaseErrors(db, func)
    db.refresh(product)
    return product
  except Exception as err:
    db.rollback()
    raise