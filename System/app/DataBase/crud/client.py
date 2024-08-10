from sqlalchemy.orm import Session
from models import Client

def createClient(db: Session, ciClient: int, name: str, surname: str, secondSurname: str):
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

def getClientById(db:Session, ciClient: int):
  return db.query(Client).filter(Client.ciClient == ciClient).first()

def getClients(db: Session, skip: int = 0, limit: int = 10):
  return db.query(Client).offset(skip).limit(limit).all()

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

def removeClient(db: Session, ciClient: int):
  client = db.query(Client).filter(Client.ciClient == ciClient).first()
  if Client:
    db.delete(client)
    db.commit()
  return client