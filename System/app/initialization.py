from DataBase.models import Base, User
from config import engine, getDB
from DataBase.errorHandling import handleDatabaseErrors
# import os

def init_db():
  Base.metadata.create_all(bind=engine)
  
  # Create default user if not exists
  with getDB() as db:
    createDefaultUser(db)

def createDefaultUser(db):
  from DataBase.crud.user import createUser, getUserByUsername
  
  if not getUserByUsername(db, "Alfa"):
    try: 
      user = User(
        username="Alfa",
        password="informatica2024",
        role="Administrador",
      )
      
      def func():
        db.add(user)
        db.commit()
        return user
      
      return handleDatabaseErrors(db, func)
    except Exception as err:
      raise
    print("Master User created")