from DataBase.models import Closing, Sale, Transaction
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from exceptions import DataAlreadyExists, DataNotFoundError
from DataBase.errorHandling import handleDatabaseErrors
from datetime import datetime, timedelta, time
from utils.dateConversions import convertToLocalTz, convertToUTC, getLocal, getUTC
from sqlalchemy import asc, desc, and_, func
from DataBase.crud.sale import getSaleById
from utils.sessionManager import getCurrentUser
from DataBase.crud.user import getUserByUsername

def createClosing(db: Session, sales, generalPrice, totals, gain):
  try:
    if closingExistsToday(db):
      raise DataAlreadyExists("Ya se realizó el cierre de caja del día actual.")
    
    closing = Closing(
      amount=generalPrice,
      gain=gain,
      idUser=getUserByUsername(db, getCurrentUser()).idUser
    )
    
    def func():
      db.add(closing)
      db.commit()
    
    handleDatabaseErrors(db, func)
    db.refresh(closing)
    
    salesObj = [getSaleById(db, sale) for sale in sales]
    for sale in salesObj:
      sale.idClosing = closing.idClosing
    
    db.commit()
    return closing
  except:
    raise
  
def getClosings(db: Session):
  try:
    def func():
      return db.query(Closing).order_by(desc(Closing.idClosing)).all()
    return handleDatabaseErrors(db, func)
  except: 
    raise
  
def getClosingById(db: Session, idClosing: int):
  try:
    def func():
      return db.query(Closing).filter(Closing.idClosing == idClosing).first()
    
    return handleDatabaseErrors(db, func)
  except:
    raise

def closingExistsToday(db: Session) -> bool:
  try:
    local_today = getLocal().date()
    
    startOfDay = datetime.combine(local_today, time.min)  # 00:00:00
    endOfDay = datetime.combine(local_today, time.max)  # 23:59:59.999999

    exists = db.query(Closing).filter(
        Closing.date >= startOfDay,
        Closing.date <= endOfDay
    ).first() is not None

    return exists
  except: 
    raise
  
def getSalesByClosing(db: Session, idClosing):
  
  def function():
    return db.query(Sale).filter(
      Sale.idClosing == idClosing,
    )
  
  sales = handleDatabaseErrors(db, function)
  
  generalPrice = sum(sale.totalPrice for sale in sales)
  
  gain = sum(sale.gain for sale in sales)
  
  products, combos = getProductsBySales(db, sales)
  
  totals = getTotalByMethod(db, [sale.idSale for sale in sales])
  return [sale.idSale for sale in sales], products, combos, generalPrice, totals, gain

def removeClosing(db: Session, idClosing):
  try:
    closing = getSaleById(db, idClosing)
    sales, generalPrice, totals, gain = getSalesByClosing(db, idClosing)
    
    for sale in sales:
      sale = getSaleById(db, sale)
      sale.idClosing = None
    
    def func():
      db.delete(closing)
      db.commit()
      
    handleDatabaseErrors(db, func)
    return closing
  except:
    raise

def getProductsWithoutClosing(db: Session):
  local_today = getLocal()
  
  startOfDay = local_today.replace(hour=0, minute=0, second=0, microsecond=0)
  endOfDay = local_today.replace(hour=23, minute=59, second=59, microsecond=999999)

def getSalesWithoutClosing(db: Session):
  local_today = getLocal()
  
  startOfDay = local_today.replace(hour=0, minute=0, second=0, microsecond=0)
  endOfDay = local_today.replace(hour=23, minute=59, second=59, microsecond=999999)
  
  def function():
    return db.query(Sale).filter(
      Sale.date >= startOfDay,
      Sale.date <= endOfDay,
    )
  
  sales = handleDatabaseErrors(db, function)
  
  generalPrice = sum(sale.totalPrice for sale in sales)
  
  gain = sum(sale.gain for sale in sales)
  
  products, combos = getProductsBySales(db, sales)
  
  totals = getTotalByMethod(db, [sale.idSale for sale in sales])
  return [sale.idSale for sale in sales], products, combos, generalPrice, totals, gain

def getProductsBySales(db, sales):
  try:
    products = {}
    combos = {}
    
    for sale in sales:
      for register in sale.products:
        name = register.product.name
        quantity = register.productQuantity
        
        if name in products:
          products[name] += quantity
        else:
          products[name] = quantity
          
      for register in sale.combos:
        name = register.combo.name
        comboQuantity = register.comboQuantity
            
        if name in combos:
          combos[name] += comboQuantity
        else:
          combos[name] = comboQuantity
          
        combo = register.combo
        
        for register in combo.products:
          name = register.product.name
          quantity = register.productQuantity
          
          if name in products:
            products[name] += quantity * comboQuantity
          else:
            products[name] = quantity * comboQuantity
    
    return products, combos
  except:
    raise

def getTotalByMethod(db: Session, sales):
  totals = (
    db.query(Transaction.method, Transaction.transactionType, func.sum(Transaction.amountUSD).label("totalUSD"), func.sum(Transaction.amountVES).label("totalVES"), func.sum(Transaction.amountVES / Transaction.exchangeRate).label("totalConvertedUSD"),)
    .filter(Transaction.idSale.in_(sales))
    .group_by(Transaction.method, Transaction.transactionType)
    .all()
  )
  
  result = {
    "payments": {},
    "changes": {},
  }
  
  for method, transactionType, totalUSD, totalVES, totalConvertedUSD in totals:
    total = (totalUSD or 0) + (totalConvertedUSD or 0)
    
    data = {
      "USD": totalUSD or 0,
      "VES": totalVES or 0,
      "total": total,
    }
    if transactionType == "Pago":
      result["payments"][method.value] = data
    else:
      result["changes"][method.value] = data
  
  return result