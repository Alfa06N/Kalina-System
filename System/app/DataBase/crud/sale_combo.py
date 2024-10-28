from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import SaleCombo
from DataBase.errorHandling import handleDatabaseErrors
from DataBase.crud.sale_product import updateProductStock
from DataBase.crud.sale import getSaleById
from exceptions import DataNotFoundError, DataAlreadyExists, InvalidData

def createSaleCombo(db: Session, idSale: int, idCombo: int, comboQuantity: int, price: float):
  try:
    record = SaleCombo(
      idSale=idSale,
      idCombo=idCombo,
      comboQuantity=comboQuantity,
      price=price,
    )
    
    def func():
      db.add(record)
      db.commit()
      
    handleDatabaseErrors(db, func)
    db.refresh(record)
    return record
  except Exception:
    raise
  
def createManySaleCombos(db:Session, combos, idSale:int):
  try:
    combosList = []
    for combo in combos:
      saleCombo = createSaleCombo(
        db=db,
        idSale=idSale,
        idCombo=combo["id"],
        comboQuantity=combo["quantity"],
        price=combo["price"],
      )
      
      for product in combo["products"]:
        updateProductStock(
          db=db,
          idProduct=product["id"],
          quantity=product["totalQuantity"],
        )
      combosList.append(saleCombo)
    return combosList
  except:
    raise
  
def getSaleComboById(db: Session, idSaleCombo: int):
  try:
    def func():
      return db.query(SaleCombo).filter(SaleCombo.idSaleCombo == idSaleCombo).first()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getAllSaleCombo(db: Session):
  try:
    def func():
      return db.query(SaleCombo).all()
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def removeAllSaleCombo(db: Session):
  try:
    def func():
      db.query(Sale).delete()
      db.commit()
    handleDatabaseErrors(db, func)
    return True
  except Exception:
    raise