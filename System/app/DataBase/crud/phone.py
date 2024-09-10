from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from exceptions import DataNotFoundError, DataAlreadyExists
from DataBase.models import Phone
from DataBase.crud.employee import getEmployeeById
from DataBase.errorHandling import handleDatabaseErrors

def createPhone(db: Session, area: str, number: str, kind: str, ciEmployee: int):
  try:
    if not getEmployeeById(db, ciEmployee):
      raise DataNotFoundError(f"Empleado propietario del CI '{ciEmployee}' no encontrado")
    
    phone = Phone(
      area=area,
      number=number,
      kind=kind,
      ciEmployee=ciEmployee
    )
    
    def func():
      db.add(phone)
      db.commit()
    
    handleDatabaseErrors(db, func)
    
    db.refresh(phone)
    return phone
  except Exception:
    raise
  
def getPhoneById(db: Session, idPhone: int):
  try:
    def func():
      return db.query(Phone).filter(Phone.idPhone == idPhone).first()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getPhones(db: Session):
  try:
    def func():
      return db.query(Phone).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def getPhoneByIdEmployee(db: Session, ciEmployee:int):
  try:
    def func():
      return db.query(Phone).filter(Phone.ciEmployee == ciEmployee).all()
    
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def updatePhone(db: Session, idPhone: int, area: str, number: str, kind: str,):
  try:
    phone = getPhoneById(db, idPhone)
    
    if not phone:
      raise DataNotFoundError(f"Teléfono con ID {idPhone} no encontrado")

    def func():
      if area:
        phone.area = area
      if number:
        phone.number = number
      if kind:
        phone.kind = kind
        
      db.commit()
      db.refresh(phone)
      return phone
        
    return handleDatabaseErrors(db, func)
  except Exception:
    raise
  
def removePhone(db: Session, idPhone: int):
  try:
    phone = getPhoneById(db, idPhone)
    
    if not phone:
      raise DataNotFoundError(f"Teléfono con ID {idPhone} no encontrado")
    
    def func():
      db.delete(phone)
      db.commit()
    
    handleDatabaseErrors(db, func)
    
    return phone
  except Exception:
    raise