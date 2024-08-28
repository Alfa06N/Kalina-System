from sqlalchemy.orm import Session
from DataBase.models import User
from DataBase.crud.employee import getEmployeeById
from DataBase.errorHandling import handleDatabaseErrors
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError

def createUser(db: Session, username: str, password: str, role: str, ciEmployee: int):
  try:
    if not getUserByUsername(db, username):
      user = User(
        username=username,
        password=password,
        role=role,
        ciEmployee=ciEmployee
      )
      
      def func():
        db.add(user)
        db.commit()
        
      handleDatabaseErrors(
        db,
        func
      )
      
      db.refresh(user)
      return user
    else:
      raise Exception("Nombre de usuario no disponible")
  except SQLAlchemyError as e:
    return None
  except Exception as e:
    raise 

def getUserByUsername(db: Session, username: str):
  try:
    def func():
      return db.query(User).filter(User.username == username).first()
    
    return handleDatabaseErrors(
      db,
      func
    )
  except Exception as e:
    raise

def getUserById(db: Session, idUser: int):
  try:
    def func():
      return db.query(User).filter(User.idUser == idUser).first()
      
    return handleDatabaseErrors(
      db,
      func
    )
  except SQLAlchemyError as e:
    return None

def getUsers(db: Session):
  try:
    def func():
      return db.query(User).offset(1).all()
    return handleDatabaseErrors(
      db,
      func
    )
  except Exception:
    raise

def updateUser(db: Session, user, username: str, password: str):
  try:
    if not user.username == username:
      usernameExists = getUserByUsername(db, username)
      if usernameExists:
        raise Exception("Nombre de usuario no disponible")
    def func():
      if user:
        if username:
          user.username = username
        if password:
          user.password = password
          
        db.commit()
        db.refresh(user)
      return user
      
    return handleDatabaseErrors(
      db,
      func
    )
  except Exception as e:
    raise
  
def removeUser(db: Session, idUser: int):
  try:
    user = getUserById(db, idUser)
    
    def func():
      db.delete(user)
      db.commit()
    
    handleDatabaseErrors(
      db,
      func
    )
    
    return user
  except Exception:
    raise
  

def removeUserByUsername(db: Session, username:str):
  try:
    user = getUserByUsername(db, username)
    
    def func():
      db.delete(user)
      db.commit()
    
    handleDatabaseErrors(
      db,
      func
    )
  except:
    raise Exception("Error al eliminar el usuario")
  
def queryUserData(db, username, password):
  from DataBase.crud.user import getUserByUsername
  
  try:
    user = getUserByUsername(db, username)
      
    if user:
      return user.password == password
    else:
      raise DataNotFoundError(f"Usuario no encontrado")
  except DataNotFoundError:   
    raise