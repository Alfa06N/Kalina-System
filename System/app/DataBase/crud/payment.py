from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import Payment, MethodEnum
from exceptions import DataAlreadyExists, DataNotFoundError, InvalidData
from DataBase.crud.sale import getSaleById
from DataBase.errorHandling import handleDatabaseErrors

def createPayment(db: Session, amount: float, method: str, reference: str, idSale: int):
  try:
    if method not in MethodEnum.__members__:
      raise InvalidData(f"Método de pago '{method}' no es válido.")
    
    sale = getSaleById(db, idSale)
    
    if not sale:
      raise DataNotFoundError(f"Venta con id {idSale} no encontrado")
    
    payment = Payment(
      amount=amount,
      method=method,
      reference=reference,
      idSale=sale.idSale
    )
    
    def func():
      db.add(payment)
      db.commit()
      
    handleDatabaseErrors(db, func)
    db.refresh(payment)
    return payment
  except Exception:
    raise
  
def getPayments(db: Session):
  try:
    def func():
      return db.query(Payment).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getPaymentById(db: Session, idPayment: int):
  try:
    def func():
      return db.query(Payment).filter(Payment.idPayment == idPayment).first()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getPaymentsByMethod(db: Session, method: str):
  try:
    def func():
      return db.query(Payment).filter(Payment.method == method).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def removePayment(db: Session, idPayment: int):
  try:
    payment = getPaymentById(db, idPayment)
    
    if not payment:
      raise DataNotFoundError(f"Payment con id {idPayment} no encontrado")
    
    def func():
      db.delete(payment)
      db.commit()
    
    handleDatabaseErrors(db, func)
    return payment  
  except Exception:
    raise