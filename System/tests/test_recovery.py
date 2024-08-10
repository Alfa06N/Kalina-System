import pytest
from app.DataBase.crud.recovery import removeRecovery, createRecovery, getRecoveryByUserId, updateRecovery
from app.DataBase.models import Base
from app.DataBase.crud.employee import createEmployee, getEmployeeById
from app.DataBase.crud.user import createUser, getUserByUsername
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
  
  userOne = createUser(
    db=db,
    username="Alfa06N",
    password="Comida",
    role="Administrador",
    ciEmployee=employee.ciEmployee
  )
  
  createRecovery(
    db=db,
    questionOne="¿Cuál es tu mayor miedo?",
    answerOne="Arañas",
    questionTwo="¿Cuál es tu comida favorita?",
    answerTwo="Cachapa",
    idUser=userOne.idUser
  )
  
  employee2 = createEmployee(
    db=db,
    ciEmployee=20450867,
    name="Pedro",
    surname="Gonzales",
    secondSurname="Martin",
    birthdate="1990-04-06"
  )
  
  userTwo = createUser(
    db=db,
    username="EspantaViejas",
    password="informatico3000",
    role="Colaborador",
    ciEmployee=employee2.ciEmployee
  )
  
  createRecovery(
    db=db,
    questionOne="¿Cuál es tu mayor miedo?",
    answerOne="Alturas",
    questionTwo="¿Cuál es tu comida favorita?",
    answerTwo="Arroz chino",
    idUser=userTwo.idUser
  )
  
def test_getRecoveryByUserId(db):
  createTestData(db)
  
  userOne = getUserByUsername(db, "Alfa06N")
  
  firstQuestion = getRecoveryByUserId(db, userOne.idUser).questionOne
  
  firstAnswer = getRecoveryByUserId(db, userOne.idUser).answerOne
  
  assert "Arañas" == firstAnswer
  
def test_updateRecoveryByUserId(db):
  createTestData(db)
  
  userOne = getUserByUsername(db, "Alfa06N")
  
  updatedRecovery = updateRecovery(
    db=db,
    idUser=userOne.idUser,
    questionOne="Pregunta 1",
    answerOne="Respuesta 1",
    questionTwo="Pregunta 2",
    answerTwo="Respuesta 2",
  )
  
  print(f"New answer 1: {updatedRecovery.answerOne} - Updated answer 1: {userOne.recovery.answerOne}")
  assert userOne.recovery.questionOne == "Pregunta 1"