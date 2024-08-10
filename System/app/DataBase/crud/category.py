from sqlalchemy.orm import Session
from DataBase.models import Category

from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError

def createCategory(db: Session, name: str, description: str):
  try:
    if not getCategoryByName(db, name): 
      category = Category(
        name=name,
        description=description,
      )
      def func():
        db.add(category)
        db.commit()
      
      handleDatabaseErrors(db, func)
      
      db.refresh(category)
      return category
    else:
      pass
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
    
    handleDatabaseErrors(db, func)
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
  
def getCategories(db: Session, name: str):
  try:
    def func():
      return db.query(Category).all()
    return handleDatabaseErrors(db, func)
  except Exception as e:
    return None
  
def updateCategory(db: Session, idCategory: int, name: str, description: str):
  try:
    categoryExists = getCategoryByName(db, name)
    
    if categoryExists:
      raise Exception("Esta categoría ya existe")
    else:
      category = getCategoryById(db, idCategory)
      
      def func():
        if category:
          if name:
            category.name = name
          if description:
            category.description = description
            
          db.commit()
          db.refresh(category)
        return category
      
      handleDatabaseErrors(db, func)
    
  except SQLAlchemy as e:
    return None
  except Exception as e:
    raise
  
def removeCategory(db: Session, idCategory: int):
  try:
    category = getCategoryById(db, idCategory)
    
    def func():
      db.delete(category)
      db.commit()
    
    handleDatabaseErrors(
      db, func
    )
    
    return user
  except Exception as e:
    raise
  
  ##### Eliminar comentarios de excepciones. Ya handleDatabaseErrors lo hace
  
def removeCategoryByName(db: Session, name):
  try:
    category = getCategoryByName(db, name)
    
    def func():
      db.delete(category)
      db.commit()
      
    handleDatabaseErrors(
      db, func
    )
  except Exception as e:
    raise