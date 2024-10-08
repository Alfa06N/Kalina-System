from sqlalchemy import asc, desc
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from DataBase.models import Combo
from DataBase.crud.product import getProductByName
from DataBase.errorHandling import handleDatabaseErrors
from exceptions import DataAlreadyExists, DataNotFoundError
from utils.imageManager import ImageManager

def createCombo(db: Session, name: str, cost:float, price:float, imgPath=None):
  try:
    if getComboByName(db, name):
      raise DataAlreadyExists("Nombre de combo ya existente")
    if getProductByName(db, name):
      raise DataAlreadyExists("Un producto ya posee este nombre")
    
    imageManager = ImageManager()
    
    def func():
      combo = Combo(
        name=name,
        cost=cost,
        price=price,
        imgPath=None,
      )
      db.add(combo)
      db.commit()
      return combo
      
    combo = handleDatabaseErrors(db, func)
    
    db.refresh(combo)
    
    if imgPath:
      combo.imgPath = imageManager.storageImage(combo.idCombo, imgPath)
      db.commit()
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
      return db.query(Combo).order_by(asc(Combo.name)).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def updateComboInfo(db: Session, combo, name: str, price:float, imgPath=None):
  try:
    alreadyExists = getComboByName(db, name)
    if alreadyExists and not alreadyExists == combo:
      raise DataAlreadyExists("Nombre de combo en uso.")
    else:
      combo = combo
      def func():
        if combo:
          if name:
            combo.name = name
          if price:
            combo.price = price
            
          imageManager = ImageManager()  
          combo.imgPath = imageManager.updateImage(
            idData=combo.idCombo,
            oldImage=combo.imgPath,
            newImage=imgPath,
          )
            
          db.commit()
          db.refresh(combo)
          return combo
        else:
          raise DataNotFoundError("No se encontró el combo original")
        
      return handleDatabaseErrors(db, func)
  except Exception:
    raise
      
def removeCombo(db: Session, combo):
  try: 
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