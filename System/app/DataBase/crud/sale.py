from DataBase.models import Sale
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from exceptions import DataAlreadyExists, DataNotFoundError
from DataBase.errorHandling import handleDatabaseErrors
from datetime import datetime
from utils.sessionManager import getCurrentUser
from DataBase.crud.user import getUserByUsername
from DataBase.crud.sale_combo import createSaleCombo
from DataBase.crud.sale_product import createSaleProduct
from DataBase.crud.product import calculatePrice
from utils.dateConversions import convertToLocalTz, convertToUTC
from sqlalchemy import asc, desc

def createSale(db: Session, totalPrice: float, gain: float, ciClient: int, user):
  try:
    if user:
      sale = Sale(
        totalPrice=totalPrice,
        gain=gain,
        idUser=user.idUser,
        ciClient=ciClient
      )
      
      def func():
        db.add(sale)
        db.commit()
        
      handleDatabaseErrors(db, func)
      
      db.refresh(sale)
      return sale
    else:
      raise DataNotFoundError(f"El usuario recibido no se encontró en el sistema")
  except Exception:
    raise

def getSales(db: Session):
  try:
    def func():
      return db.query(Sale).all()
    
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
  
def sellProduct(db: Session, product, quantity: int, sale):
  try:
    if product.stock < quantity:
      raise ValueError(f"Stock insuficiente para el producto {product.name}")
    
    totalPrice = calculatePrice(product) * quantity
    
    record = createSaleProduct(
      db=db,
      idProduct=product.idProduct,
      idSale=sale.idSale,
      productQuantity=quantity,
      price=totalPrice
    )
    
    def func():
      product.stock -= quantity
      db.commit()
    
    handleDatabaseErrors(db, func)
    
    return record
  except Exception:
    raise
  
def sellCombo(db: Session, combo, quantity: int, sale ):
  try:
    return createSaleCombo(
      db=db,
      idSale=sale.idSale,
      idCombo=combo.idCombo,
      comboQuantity=quantity,
      price=combo.price * quantity
    )
  except Exception:
    raise