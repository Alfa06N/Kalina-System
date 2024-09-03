from sqlalchemy.orm import Session
from DataBase.models import Employee
from DataBase.errorHandling import handleDatabaseErrors
from datetime import datetime
from exceptions import DataAlreadyExists

def createEmployee(db: Session, ciEmployee: int, name: str, surname: str, secondSurname: str, birthdate: str):
  try:
    if not getEmployeeById(db, ciEmployee):
      birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
      
      employee = Employee(
        ciEmployee=ciEmployee,
        name=name,
        surname=surname, 
        secondSurname=secondSurname, 
        birthdate=birthdate,
      )
      
      def addEmployee():
        db.add(employee)
        db.commit()
        db.refresh(employee)
      
      handleDatabaseErrors(
        db,
        addEmployee
      )
      return employee
    else:
      raise DataAlreadyExists("Cédula de identidad ya existente")
  except Exception as e:
    db.rollback()
    raise

def getEmployeeById(db: Session, ciEmployee: int):
  def func():
    return db.query(Employee).filter(Employee.ciEmployee == ciEmployee).first()
    
  return handleDatabaseErrors(
    db,
    func
  )
  
def getEmployeeByName(db: Session, name: str):
  def func():
    return db.query(Employee).filter(Employee.name == name).first()
  
  return handleDatabaseErrors(
    db,
    func
  )

def getEmployees(db: Session):
  def func():
    return db.query(Employee).all()
  
  return handleDatabaseErrors(
    db,
    func
  )

def updateEmployee(db: Session, ciEmployee: int, name: str, surname: str, secondSurname: str, birthdate: str):
  employee = db.query(Employee).filter(Employee.ciEmployee == ciEmployee).first()
  
  birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
  
  def updateValues():
    if employee:
      if name:
        employee.name = name
      if surname:
        employee.surname = surname
      if secondSurname:
        employee.secondSurname = secondSurname
      if birthdate:
        employee.birthdate = birthdate
      
  handleDatabaseErrors(
    db,
    updateValues
  )
  
  db.commit()
  db.refresh(employee)
  return employee

def removeEmployee(db: Session, employee):
  try:
    def func():
      db.delete(employee)
    
    handleDatabaseErrors(
      db,
      func
    )
    
    db.commit()
        
    return employee
  except Exception as err:
    raise