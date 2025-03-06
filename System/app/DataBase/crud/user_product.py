from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from DataBase.models import UserProduct
from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError
from utils.dateConversions import getUTC, convertToLocalTz, convertToUTC
from datetime import datetime

def registerOperation(db: Session, idUser: int, idProduct: int, productQuantity: int):
  try:   
    register = UserProduct(
      idUser=idUser,
      idProduct=idProduct, 
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

def getRegisterById(db: Session, idUserProduct: int):
  try:
    def func():
      return db.query(UserProduct).filter(UserProduct.idUserProduct == idUserProduct).first()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getRegisterByUserId(db: Session, idUser: int):
  try:
    def func():
      return db.query(UserProduct).filter(UserProduct.idUser == idUser).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getRegisterByProductId(db: Session, idProduct: int):
  try:
    def func():
      return db.query(UserProduct).filter(UserProduct.idProduct == idProduct).order_by(desc(UserProduct.idUserProduct)).limit(50).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getAllRegisters(db: Session):
  try:
    def func():
      return db.query(UserProduct).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def deleteAllUserProduct(db: Session, idUserProduct: int):
  try:
    def func():
      db.query(UserProduct).delete()
      db.commit()
    
    handleDatabaseErrors(db, func)
    print("Todos los registros de UserProduct han sido eliminados")
    
  except Exception:
    raise
  
def getRegistersByDate(db: Session, localDate: datetime, ascending: bool):
  try:
    startOfDay = localDate.replace(hour=0, minute=0, second=0, microsecond=0)
    endOfDay = localDate.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    utcStart = convertToUTC(startOfDay)
    utcEnd = convertToUTC(endOfDay)
    
    def func():
      if ascending:
        return db.query(UserProduct).filter(
          UserProduct.date >= utcStart,
          UserProduct.date <= utcEnd
        ).order_by(asc(UserProduct.date)).all()
      else:
        return db.query(UserProduct).filter(
          UserProduct.date >= utcStart,
          UserProduct.date <= utcEnd
        ).order_by(desc(UserProduct.date)).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise