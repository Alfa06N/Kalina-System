from sqlalchemy.orm import Session
from DataBase.models import Product, UserProduct
from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError, DataAlreadyExists
from utils.sessionManager import getCurrentUser
from DataBase.crud.user import getUserByUsername
from DataBase.crud.user_product import registerOperation
from datetime import datetime

def createProduct(db: Session, name: str, description: str, stock: int, minStock: int, cost: float, gain: float, iva: float, idCategory: int ):
  try:
    
    product = Product(
      name=name,
      description=description,
      stock=stock,
      minStock=stock,
      cost=cost,
      gain=gain,
      iva=iva,
      idCategory=idCategory
    )
    
    def func():
      db.add(product)
      db.commit()
    
    handleDatabaseErrors(db, func)
    
    db.refresh(product)
    
    updateProductStock(db, product, product.stock)
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
      return db.query(Product).all()
    
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

def removeProduct(db: Session, idProduct: int):
  try:
    product = getProductById(db, idProduct)
    
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

def calculatePrice(product):
  try: 
    if product:
      price = product.cost + (product.cost*product.iva) + (product.cost*product.gain)
      return round(price, 3) 
    else:
      raise DataNotFoundError(f"Producto no encontrado")
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
    # elif not user:
    #   raise DataNotFoundError(f"No se encontró el usuario {username}")
    
    # def updateProduct():
    #   product.stock += quantityAdded
    #   db.refresh(product)
    
    # handleDatabaseErrors(db, updateProduct)
    
    def createOperation():
      register = registerOperation(
        db=db,
        idUser=user.idUser,
        idProduct=product.idProduct,
        productQuantity=quantityAdded
      )
      db.add(register)
      db.refresh(register)
      
    handleDatabaseErrors(db, createOperation)
    
    db.commit()
    return product
  except Exception:
    raise