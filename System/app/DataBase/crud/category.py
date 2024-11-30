from sqlalchemy.orm import Session
from DataBase.models import Category
from sqlalchemy import asc, desc
from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError, DataAlreadyExists
from utils.imageManager import ImageManager

def  createCategory(db: Session, name: str, description: str="", imgPath: str = None):
  try:
    if not getCategoryByName(db, name): 
      category = Category(
        name=name,
        description=description,
        imgPath=imgPath,
      )
      def func():
        db.add(category)
        db.commit()
      
      handleDatabaseErrors(db, func)
      
      db.refresh(category)
      return category
    else:
      raise DataAlreadyExists("Esta categoría ya existe")
  except DataNotFoundError:
    raise
  except SQLAlchemyError as e:
    return None
  except Exception:
    raise
  
def getCategoryByName(db: Session, name: str):
  try:
    def func():
      return db.query(Category).filter(Category.name == name).first()
    
    return handleDatabaseErrors(db, func)
  except Exception as e:
    return None 

def getCategoryById(db: Session, idCategory: str):
  try:
    def func():
      return db.query(Category).filter(Category.idCategory == idCategory).first()
    return handleDatabaseErrors(db, func)
  
  except SQLAlchemy as e:
    return None
  except Exception:
    raise
  
def getCategories(db: Session):
  try:
    def func():
      return db.query(Category).order_by(asc(Category.name)).all()
    return handleDatabaseErrors(db, func)
  except Exception as e:
    return None
  
def updateCategory(db: Session, category, name: str, description: str="", imgPath=None):
  try:
    categoryExists = getCategoryByName(db, name)
    
    if categoryExists and not category.name == name:
      raise DataAlreadyExists("Esta categoría ya existe")
    else:
      imageManager = ImageManager()
      
      def func():
        if category:
          if name:
            category.name = name
          category.description = description
          
          updatedImgPath = imageManager.updateImage(
            idData=category.idCategory, 
            oldImage=category.imgPath,
            newImage=imgPath,
          )
          
          category.imgPath = updatedImgPath
            
          db.commit()
          db.refresh(category)
        return category
      
      return handleDatabaseErrors(db, func)
    
  except DataAlreadyExists:
    raise
  except SQLAlchemy as e:
    return None
  except Exception as e:
    raise
  
def removeCategory(db: Session, category):
  try:
    def func():
      db.delete(category)
      db.commit()
    
    handleDatabaseErrors(
      db, func
    )
    
    return category
  except Exception as e:
    raise
  
def removeCategoryByName(db: Session, name):
  try:
    category = getCategoryByName(db, name)
    
    def func():
      db.delete(category)
      db.commit()
      
    handleDatabaseErrors(
      db, func
    )
    return category
  except Exception as e:
    raise