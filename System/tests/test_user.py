import pytest
from app.DataBase.crud.user import createUser, getUserById, getUsers, updateUser, removeUser, getUserByUsername
from app.DataBase.models import Base
from app.DataBase.crud.employee import createEmployee, getEmployeeById
from app.config import engine, getDB, test_engine, getTestDB

@pytest.fixture(scope="function")
def db():
  try:
    Base.metadata.create_all(engine)
    with getDB() as db:
      yield db
  finally:
    db.close()
    Base.metadata.drop_all(engine)
    
def createTestData(db):
  employee = createEmployee(
    db=db, 
    ciEmployee=31453119, 
    name="Nicolás Alessandro",
    surname="Alfaro", 
    secondSurname="Guzmán", 
    birthdate="2006-01-19"
  )
  
  createUser(
    db=db,
    username="Alfa06N",
    password="Comida",
    role="Administrador",
    ciEmployee=employee.ciEmployee
  )
  
  employee2 = createEmployee(
    db=db,
    ciEmployee=20450867,
    name="Pedro",
    surname="Gonzales",
    secondSurname="Martin",
    birthdate="1990-04-06"
  )
  
  createUser(
    db=db,
    username="EspantaViejas",
    password="informatico3000",
    role="Colaborador",
    ciEmployee=employee2.ciEmployee
  )
  
@pytest.mark.skip(reason="Ya ha sido verificada")
def test_getUserByUsername(db):
  createTestData(db)
  
  result = getUserByUsername(
    db,
    "Alfa06N"
  )
  
  print(f"Username: {result.username} with id: {result.idUser}. Employee name: {result.employee.name} with document: {result.employee.ciEmployee}.")
  
  employee = getEmployeeById(db, 31453119)
  
  print(f"Employee: {employee.name} with user: {employee.user.username}")
  print(f"User: {result.username} with employee: {result.employee.name}")
  assert result.ciEmployee == 31453119
  
@pytest.mark.skip(reason="Ya ha sido verificada")
def test_updateUser(db):
  try:
    createTestData(db)
    
    # Should return error
    result = updateUser(
      db,
      idUser=2,
      username="PedroGamer",
      password="informatico3000"
    )
    
    newUser = getUserById(db, 2)
    
    assert result.username == newUser.username
  except Exception as e:
    print(f"Error: {e}")

@pytest.mark.skip(reason="Ya ha sido verificada")
def test_removeUser(db):
  createTestData(db)
  
  try:
    removeUser(
      db,
      2,
    )
    
    removeUser(
      db,
      2
    )
    
    assert getUserByUsername(db, "EspantaViejas") == None
  except:
    db.rollback()
    pass