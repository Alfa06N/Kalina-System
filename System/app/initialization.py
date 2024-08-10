from DataBase.models import Base
from config import engine, getDB
# import os

def init_db():
  Base.metadata.create_all(bind=engine)
  
  # Create default user if not exists
  with getDB() as db:
    createDefaultUser(db)

def createDefaultUser(db):
  from DataBase.crud.user import createUser, getUserByUsername
  
  if not getUserByUsername(db, "Alfa"):
    # masterUsername = os.getenv("KS_MASTER_USERNAME")
    # masterPassword = os.getenv("KS_MASTER_PASSWORD")
    createUser(
      db=db,
      username="Alfa",
      password="informatica2024",
      role="Administrador",
      ciEmployee=None
    )
    print("Master User created")