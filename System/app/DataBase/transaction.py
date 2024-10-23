from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import Transaction, MethodEnum
from exceptions import DataAlreadyExists, DataNotFoundError, InvalidData
from DataBase.crud.sale import getSaleById
from DataBase.errorHandling import handleDatabaseErrors
from utils.exchangeManager import getCurrentRate

def createTransaction(db: Session, amountUSD:float, amountVES:float, method:str, transactionType:str, reference:str, idSale:int):
  try:
    if method not in MethodEnum.__members__:
      raise InvalidData(f"Método {method} no válido.")
    
    sale = getSaleById(db, idSale)
    exchangeRate = getCurrentRate()
    
    if not sale:
      raise DataNotFoundError(f"Venta con id {idSale} no encontrado.")
    if not exchangeRate:
      raise DataNotFoundError(f"Establece la tasa de cambio.")
    
    payment = payment(
      amountUSD=amountUSD,
      amountVES=amountVES,
      exchangeRate=exchangeRate,
      method=method,
      transactionType=transactionType,
      reference=reference,
      idSale=idSale,
    )
    
    def func():
      db.add(payment)
      db.commit()
      
    handleDatabaseErrors(db, func)
    db.refresh(payment)
    return payment
  except:
    raise

def getTransactions(db: Session):
  try:
    def func():
      return db.query(Transaction).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getPaymentById(db: Session, idPayment: int):
  try:
    def func():
      return db.query(Transaction).filter(Transaction.idTransaction == idTransaction).first()
    return handleDatabaseErrors(db, func)
  except:
    raise
  
def getTransactionsByMethod(db: Session, method: str):
  try:
    def func():
      return db.query(Transaction).filter(Transaction.method == method).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
    
def getTransactionsByType(db: Session, transactionType: str):
  try:
    def func():
      return db.query(Transaction).filter(Transaction.transactionType == transactionType).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise