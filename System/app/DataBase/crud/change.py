from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import Change
from exceptions import DataNotFoundError, DataAlreadyExists
from DataBase.errorHandling import handleDatabaseErrors
from DataBase.crud.Sale import getSaleById

def createChange(db: Session, idSale: int, amountReturned: float, method: str):
  try:
    sale = getSaleById(db, 1)
    
    if not sale:
      DataNotFoundError(f"No se encontró venta con id '{idSale}'")
      
    change = Change(
      amountReturned=amountReturned,
      method=method,
      idSale=idSale,
    )
    
    def func():
      db.add(change)
      db.commit()
      
    handleDatabaseErrors(db, func)
    db.refresh(change)
    return change
  except Exception:
    raise
  
def getChangeById(db: Session, idChange: int):
  try:
    def func():
      return db.query(Change).filter(Change.idChange == idChange).first()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise

def getChanges(db: Session):
  try:
    def func():
      return db.query(Change).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def removeChange(db: Session, idChange: int):
  try:
    change = getChangeById(db, idChange)
    
    if not change:
      raise DataNotFoundError(f"Vuelto con id '{idChange}' no encontrado")
    
    def func():
      db.delete(change)
      db.commit()
      
    handleDatabaseErrors(db, func)
    return change
  except Exception:
    raise