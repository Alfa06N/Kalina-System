from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import Transaction, MethodEnum
from exceptions import DataAlreadyExists, DataNotFoundError, InvalidData
from DataBase.crud.sale import getSaleById
from DataBase.errorHandling import handleDatabaseErrors
from utils.exchangeManager import exchangeRateManager
from utils.enumsHelper import getMethodEnum

def createTransactionWithoutCommit(db: Session, amountUSD:float, amountVES:float, method:str, transactionType:str, reference:str, idSale:int):
  try:
    if method not in [m.value for m in MethodEnum]:
      raise InvalidData(f"Método {method} no válido.")

    method = getMethodEnum(method)
    
    sale = getSaleById(db, idSale)
    exchangeRate = exchangeRateManager.getRate()
    
    if not sale:
      raise DataNotFoundError(f"Venta con id {idSale} no encontrado.")
    if not exchangeRate:
      raise DataNotFoundError(f"Establece la tasa de cambio.")
    
    transaction = Transaction(
      amountUSD=amountUSD,
      amountVES=amountVES,
      exchangeRate=exchangeRate,
      method=method,
      transactionType=transactionType,
      reference=reference,
      idSale=idSale,
    )
    
    def func():
      db.add(transaction)
      db.commit()
      
    handleDatabaseErrors(db, func)
    db.refresh(transaction)
    return transaction
  except:
    raise

def createManyWithoutCommit(db: Session, idSale:int, transactions:list=[]):
  try:
    transactionsList = []
    for transaction in transactions:
      amountVES = transaction["amount"] if transaction["currency"] == "Bs" else None
      amountUSD = transaction["amount"] if transaction["currency"] == "$" else None
      
      newTransaction = createTransactionWithoutCommit(
        db=db,
        amountUSD=amountUSD,
        amountVES=amountVES,
        method=transaction["method"],
        transactionType=transaction["transactionType"],
        reference=transaction["reference"],
        idSale=idSale
      )
      
      transactionsList.append(newTransaction)
    
    return transactionsList
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