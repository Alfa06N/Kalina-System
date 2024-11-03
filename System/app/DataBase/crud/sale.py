from DataBase.models import Sale
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from exceptions import DataAlreadyExists, DataNotFoundError
from DataBase.errorHandling import handleDatabaseErrors
from datetime import datetime
from utils.sessionManager import getCurrentUser
from DataBase.crud.user import getUserByUsername
from DataBase.crud.product import calculatePrice
from utils.dateConversions import convertToLocalTz, convertToUTC
from sqlalchemy import asc, desc

def createSaleWithoutCommit(db: Session, totalPrice: float, gain: float, ciClient: int, idUser:int):
  try:
    sale = Sale(
      totalPrice=totalPrice,
      gain=gain,
      idUser=idUser,
      ciClient=ciClient
    )
    
    def func():
      db.add(sale)
      db.commit()
    
    handleDatabaseErrors(db, func)
    db.refresh(sale)
    return sale
  except Exception:
    raise

def getSales(db: Session, page:int=1, quantity:int=50):
  try:
    def func():
      offset = (page - 1) * quantity
      
      return db.query(Sale).order_by(desc(Sale.date)).offset(offset).limit(quantity).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getSaleById(db: Session, idSale: int):
  try:
    def func():
      return db.query(Sale).filter(Sale.idSale == idSale).first()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getSaleByDate(db: Session, localDate: datetime, ascending: bool):
  try:
    startOfDay = localDate.replace(hour=0, minute=0, second=0, microsecond=0)
    endOfDay = localDate.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    utcStart = convertToUTC(startOfDay)
    utcEnd = convertToUTC(endOfDay)
    
    def func():
      if ascending:
        return db.query(Sale).filter(
          Sale.date >= utcStart,
          Sale.date <= utcEnd,
        ).order_by(asc(Sale.date)).all()
      else:
        return db.query(Sale).filter(
          Sale.date >= utcStart,
          Sale.date <= utcEnd,
        ).order_by(desc(Sale.date)).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def removeSale(db: Session, idSale: int):
  try:
    sale = getSaleById(db, idSale)
    if not sale:
      raise DataNotFoundError(f"Venta con id '{idSale}' no encontrada")
    
    def func():
      db.delete(sale)
      db.commit()
      
    handleDatabaseErrors(db, func)
    return sale
  except Exception:
    raise
  
def removeAllSales(db: Session):
  try:
    def func():
      db.query(Sale).delete()
      db.commit()
    handleDatabaseErrors(db, func)
    print("Todas las ventas han sido eliminadas")
  except Exception:
    raise

def calculateSaleGain(products:list=[], combos:list=[]):
  try:
    totalGain = 0
    
    for product in products:
      totalGain += product["gain"]
    
    for combo in combos:
      totalGain += combo["gain"]
    
    return totalGain
  except:
    raise