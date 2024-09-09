from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import Combo
from DataBase.errorHandling import handleDatabaseErrors
from exceptions import DataAlreadyExists, DataNotFoundError

def createCombo(db: Session, name: str, imgPath: str = None):
  try:
    if getComboByName(db, name):
      raise DataAlreadyExists("Nombre de combo ya existente")
    
    combo = Combo(
      name=name,
      imgPath=imgPath
    )
    
    def func():
      db.add(combo)
      db.commit()
      
    handleDatabaseErrors(db, func)
    
    db.refresh(combo)
    return combo
  except Exception:
    raise

def getComboById(db: Session, idCombo: int):
  try:
    def func():
      return db.query(Combo).filter(Combo.idCombo == idCombo).first()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getComboByName(db: Session, name: str):
  try:
    def func():
      return db.query(Combo).filter(Combo.name == name).first()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getCombos(db: Session):
  try:
    def func():
      return db.query(Combo).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def updateComboInfo(db: Session, idCombo: int, name: str):
  try:
    if getComboByName(db, name):
      raise DataAlreadyExists("Nombre de combo ya existente")
    else:
      combo = getComboById(db, idCombo)
      
      def func():
        if combo:
          if name:
            combo.name = name
            
          db.commit()
          db.refresh(combo)
          return combo
        else:
          raise DataNotFoundError("No se encontró el combo original")
        
      return handleDatabaseErrors(db, func)
  except Exception:
    raise
      
def removeCombo(db: Session, idCombo: int = None, name: str = None):
  try:
    combo = None
    if idCombo:
      combo = getComboById(db, idCombo)
    elif name:
      combo = getComboByName(db, name)
      
    if combo:
      def func():
        db.delete(combo)
        db.commit()
      handleDatabaseErrors(db, func)
      return combo
    else:
      raise DataNotFoundError("No se encontró el combo original")
  except Exception:
    raise
  
def removeComboByName(db: Session, name: str):
  try:
    combo = getComboByName(db, name)
    
    if combo:
      def func():
        db.delete(combo)
        db.commit()
        
      handleDatabaseErrors(db, func)
      return combo
    else:
      raise DataNotFoundError("No se encontró el combo original")
  except Exception:
    raise
  
def updateComboDetails(db: Session, combo, newPrice):
  try:
    def func():
      newCost = calculateComboCost(combo.products)
      
      if newCost:
        combo.cost = newCost
      if newPrice:
        combo.price = newPrice
        db.commit()
        db.refresh(combo)
        return combo

    return handleDatabaseErrors(db, func)
    
  except Exception:
    raise
  
def calculateComboCost(records):
  try:
    totalCost = 0
    
    for record in records:
      print(record.idProductCombo)
      totalCost += (record.product.cost * record.productQuantity)
      
    return totalCost
  except Exception:
    raise
  
def calculateComboGain(cost, price):
  return round(((price-cost)/cost)*100, 3)