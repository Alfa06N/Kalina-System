import pytest 
from app.DataBase.crud.employee import createEmployee, getEmployeeById, updateEmployee, removeEmployee, getEmployees
from app.DataBase.models import Base
from app.config import engine, getDB, getTestDB, test_engine

@pytest.fixture(scope='function')
def db():
  try:
    Base.metadata.create_all(engine)
    with getDB() as db:
      yield db
  finally:
    db.close()
    Base.metadata.drop_all(engine)

def createTestData(db):
  createEmployee(
    db=db, 
    ciEmployee=31453119, 
    name="Nicolás Alessandro",
    surname="Alfaro", 
    secondSurname="Guzmán", 
    birthdate="2006-01-19"
  )
  
  createEmployee(
    db=db,
    ciEmployee=16171570,
    name="Joselin",
    surname="Guzmán",
    secondSurname="Aponte",
    birthdate="1983-08-07",
  )
  
def test_getEmployeeById(db):
  createTestData(db)
  
  result = getEmployeeById(
    db, 
    31453119
  )
  
  assert result.name == "Nicolás Alessandro"
  assert result.ciEmployee == 31453119
  
def test_updateEmployee(db):
  createTestData(db)
  
  result = updateEmployee(
    db=db,
    ciEmployee=31453119,
    name="Nicolás",
    surname="Alfaro",
    secondSurname="Guzmán",
    birthdate="2004-01-19"
  )
  
  updatedEmployee = getEmployeeById(db=db, ciEmployee=31453119)
  assert updatedEmployee.name == "Nicolás"

def test_removeEmployee(db):
  createTestData(db)
  
  removeEmployee(
    db, 
    31453119
  )
  
  employeeDeleted = getEmployeeById(db, 31453119)
  employees = getEmployees(db)
  
  assert employeeDeleted == None
  assert len(employees) == 1