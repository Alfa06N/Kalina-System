from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from DataBase.models import Client
from DataBase.errorHandling import handleDatabaseErrors
from exceptions import DataAlreadyExists

def createClient(db: Session, ciClient: int, name: str, surname: str, secondSurname: str):
  try:
    if getClientById(db, ciClient):
      raise DataAlreadyExists("Ya existe este documento.")
    
    client = Client(
      ciClient=ciClient,
      name=name,
      surname=surname,
      secondSurname=secondSurname,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
  except:
    raise

def getClientById(db:Session, ciClient: int):
  return db.query(Client).filter(Client.ciClient == ciClient).first()

def getClients(db: Session):
  return db.query(Client).order_by(asc(Client.name)).all()

def getClientsOrderById(db: Session):
  return db.query(Client).order_by(desc(Client.ciClient)).all()

def updateClient(db: Session, ciClient: int, name: str, surname: str, secondSurname: str):
  client = db.query(Client).filter(Client.ciClient == ciClient).first()
  
  if client:
    if name:
      client.name = name
    if surname:
      client.surname = surname
    if secondSurname:
      client.secondSurname = secondSurname
    
    db.commit()
    db.refresh(client)
    
  return client

def removeClient(db: Session, client):
  def func():
    db.delete(client)
    db.commit()
    return client
  
  return handleDatabaseErrors(db, func)
  return client