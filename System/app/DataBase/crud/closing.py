from DataBase.models import Closing, Sale, Transaction
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from exceptions import DataAlreadyExists, DataNotFoundError
from DataBase.errorHandling import handleDatabaseErrors
from datetime import datetime, timedelta
from utils.dateConversions import convertToLocalTz, convertToUTC, getLocal, getUTC
from sqlalchemy import asc, desc, and_, func

def getSalesWithoutClosing(db: Session):
  local_today = getLocal() - timedelta(days=1)
  
  startOfDay = local_today.replace(hour=0, minute=0, second=0, microsecond=0)
  endOfDay = local_today.replace(hour=23, minute=59, second=59, microsecond=999999)
  
  utcStart = convertToUTC(startOfDay)
  utcEnd = convertToUTC(endOfDay)
  
  def function():
    return db.query(Sale).filter(
      Sale.date >= utcStart,
      Sale.date <= utcEnd,
      Sale.idClosing == None,
    )
  
  sales = handleDatabaseErrors(db, function)
  
  generalPrice = sum(sale.totalPrice for sale in sales)
  
  totals = getTotalByMethod(db, [sale.idSale for sale in sales])
  return [sale.idSale for sale in sales], generalPrice, totals

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
    if transactionType == "Payment":
      result["payments"][method.value] = data
    else:
      result["changes"][method.value] = data
  
  return result