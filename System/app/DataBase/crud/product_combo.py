from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from DataBase.models import ProductCombo
from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError, DataAlreadyExists
from datetime import datetime
from DataBase.crud.product import getProductById
from DataBase.crud.combo import getComboById

def registerOperation(db: Session, idProduct: int, idCombo: int, productQuantity: int):
  try:
    register = ProductCombo(
      idProduct=idProduct,
      idCombo=idCombo,
      productQuantity=productQuantity,
    )
    
    def func():
      db.add(register)
      db.commit()
      
    handleDatabaseErrors(db, func)
    
    db.refresh(register)
    return register
  except Exception:
    raise

def getRegisterById(db: Session, idProductCombo: int):
  try:
    def func():
      return db.query(ProductCombo).filter(ProductCombo.idProductCombo == idProductCombo).first()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getRegisterByProductId(db: Session, idProduct: int):
  try:
    def func():
      return db.query(ProductCombo).filter(ProductCombo.idProduct == idProduct).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getRegisterByComboId(db: Session, idCombo: int):
  try:
    def func():
      return db.query(ProductCombo).filter(ProductCombo.idCombo == idCombo).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getAllRegisters(db: Session):
  try:
    def func():
      return db.query(ProductCombo).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def updateRegister(db: Session, idProductCombo: int, idProduct: int, idCombo: int, productQuantity: int):
  try:
    register = getRegisterById(db, idProductCombo)
    if not register:
      raise DataNotFoundError(f"El registro original {idProductCombo} no existe")

    def func():
      if idProduct:
        register.idProduct = idProduct
      if idCombo:
        register.idCombo = idCombo
      if productQuantity:
        register.productQuantity = productQuantity
        
    handleDatabaseErrors(db, func)
    db.refresh(register)
    return register
  except Exception:
    raise
  
def removeRegister(db: Session, idProductCombo: int):
  try:
    register = getRegisterById(db, idProductCombo)
    
    if not register:
      raise DataNotFoundError(f"No se encontró el registro original {idProductCombo}")
    
    def func():
      db.delete(register)
      db.commit()
    
    handleDatabaseErrors(db, func)
    return register
  except Exception:
    raise